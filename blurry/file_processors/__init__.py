import asyncio
import dataclasses
import json
import mimetypes
import shutil
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment
from rich.console import Console

from blurry.images import generate_images_for_srcset
from blurry.open_graph import open_graph_meta_tags
from blurry.plugins import discovered_html_plugins
from blurry.schema_validation import validate_front_matter_as_schema
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import get_settings
from blurry.types import MarkdownFileData
from blurry.types import TemplateContext
from blurry.utils import content_path_to_url
from blurry.utils import convert_content_path_to_directory_in_build
from blurry.utils import format_schema_data
from blurry.utils import write_index_file_creating_path


warning_console = Console(stderr=True, style="bold yellow")


def process_non_markdown_file(
    filepath: Path, file_data_by_directory, jinja_env: Environment
):
    # Process Jinja files
    if ".jinja" in filepath.suffixes:
        process_jinja_file(filepath, jinja_env, file_data_by_directory)
        return

    CONTENT_DIR = get_content_directory()
    mimetype, _ = mimetypes.guess_type(filepath, strict=False)
    relative_filepath = filepath.relative_to(CONTENT_DIR)
    output_file = get_build_directory() / relative_filepath

    # Copy file to build directory if it is not already there
    if not output_file.exists():
        output_file.parent.mkdir(exist_ok=True, parents=True)
        shutil.copyfile(filepath, output_file)

    # Create srcset images
    if mimetype in [
        mimetypes.types_map[".jpg"],
        mimetypes.types_map[".png"],
    ]:
        asyncio.run(generate_images_for_srcset(filepath))


def process_jinja_file(filepath: Path, jinja_env: Environment, file_data_by_directory):
    SETTINGS = get_settings()
    build_directory = get_build_directory()
    content_directory = get_content_directory()
    template = jinja_env.get_template(str(filepath.relative_to(content_directory)))
    context = {
        "file_data_by_directory": {
            str(path): data for path, data in deepcopy(file_data_by_directory).items()
        },
        "settings": deepcopy(SETTINGS),
        "datetime": datetime,
    }
    filepath_with_new_extension = filepath.with_suffix(
        filepath.suffix.replace(".jinja", "")
    )
    filepath_in_build = build_directory / filepath_with_new_extension.relative_to(
        content_directory
    )
    html = template.render(dataclasses=dataclasses, **context)
    filepath_in_build.write_text(html)


def json_converter_with_dates(item: Any) -> None | str:
    if isinstance(item, datetime):
        return item.strftime("%Y-%M-%D")


def write_html_file(
    filepath: Path,
    file_data_by_directory: dict[Path, list[MarkdownFileData]],
    release: bool,
    jinja_env: Environment,
):
    SETTINGS = get_settings()
    extra_context: TemplateContext = {}
    # Gather data from other files in this directory if this is an index file
    file_data_list = file_data_by_directory[filepath.parent]
    if filepath.name == "index.md":
        sibling_pages = [
            {
                "url": content_path_to_url(f.path),
                **f.front_matter,
            }
            for f in file_data_list
            if f.path != filepath
        ]
        extra_context["sibling_pages"] = sibling_pages
    folder_in_build = convert_content_path_to_directory_in_build(filepath)

    file_data = [f for f in file_data_list if f.path == filepath][0]
    schema_type = file_data.front_matter.get("@type")
    if not schema_type:
        raise ValueError(
            f"Required @type value missing in file or TOML front matter invalid: "
            f"{filepath}"
        )
    template_extension = SETTINGS["MARKDOWN_FILE_JINJA_TEMPLATE_EXTENSION"]
    template = jinja_env.get_template(f"{schema_type}{template_extension}")

    # Map custom template name to Schema.org type
    if mapped_schema_type := SETTINGS["TEMPLATE_SCHEMA_TYPES"].get(schema_type):
        file_data.front_matter["@type"] = mapped_schema_type

    # Include non-schema variables as top-level context values, removing them from
    # front_matter
    front_matter = file_data.front_matter
    schema_variables: TemplateContext = {}
    template_context: TemplateContext = {}
    non_schema_variable_prefix = SETTINGS["FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX"]
    for key, value in front_matter.items():
        if key.startswith(non_schema_variable_prefix):
            template_context[key.replace(non_schema_variable_prefix, "", 1)] = value
            continue
        schema_variables[key] = value

    schema_data = json.dumps(
        format_schema_data(schema_variables),
        default=json_converter_with_dates,
    )

    validate_front_matter_as_schema(filepath, schema_variables, warning_console)

    schema_type_tag = f'<script type="application/ld+json">{schema_data}</script>'

    template_context = {
        "body": file_data.body,
        "filepath": filepath,
        "schema_data": schema_data,
        "schema_type_tag": schema_type_tag,
        "open_graph_tags": open_graph_meta_tags(file_data.front_matter),
        "build_path": folder_in_build,
        "file_data_by_directory": {
            str(path): data for path, data in deepcopy(file_data_by_directory).items()
        },
        "settings": deepcopy(SETTINGS),
        **schema_variables,
        **deepcopy(extra_context),
        **template_context,
    }

    html = template.render(dataclasses=dataclasses, **template_context)
    for html_plugin in discovered_html_plugins:
        try:
            html = html_plugin.load()(html, template_context, release)
        except Exception as err:
            print(f"Error initializing plugin {html_plugin}: {err}")

    # Write file
    write_index_file_creating_path(folder_in_build, html)
