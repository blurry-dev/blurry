import asyncio
import dataclasses
import json
import mimetypes
import os
import shutil
from collections.abc import Coroutine
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from livereload import Server
from rich import print
from rich.console import Console

from blurry.async_typer import AsyncTyper
from blurry.cli import print_blurry_name
from blurry.cli import print_plugin_table
from blurry.constants import ENV_VAR_PREFIX
from blurry.images import generate_images_for_srcset
from blurry.markdown import convert_markdown_file_to_html
from blurry.open_graph import open_graph_meta_tags
from blurry.plugins import discovered_html_plugins
from blurry.plugins import discovered_jinja_extensions
from blurry.plugins import discovered_jinja_filter_plugins
from blurry.schema_validation import validate_front_matter_as_schema
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import get_templates_directory
from blurry.settings import SETTINGS
from blurry.settings import update_settings
from blurry.sitemap import write_sitemap_file
from blurry.types import DirectoryFileData
from blurry.types import MarkdownFileData
from blurry.types import TemplateContext
from blurry.utils import content_path_to_url
from blurry.utils import convert_content_path_to_directory_in_build
from blurry.utils import format_schema_data
from blurry.utils import sort_directory_file_data_by_date
from blurry.utils import write_index_file_creating_path


def json_converter_with_dates(item: Any) -> None | str:
    if isinstance(item, datetime):
        return item.strftime("%Y-%M-%D")


warning_console = Console(stderr=True, style="bold yellow")

print_blurry_name()
print_plugin_table()


app = AsyncTyper()


def get_jinja_env():
    jinja_env = Environment(
        loader=FileSystemLoader(get_templates_directory()),
        autoescape=select_autoescape(
            list(
                {
                    SETTINGS["MARKDOWN_FILE_JINJA_TEMPLATE_EXTENSION"].lstrip("."),
                    "html",
                    "xml",
                }
            )
        ),
        extensions=[
            jinja_extension.load() for jinja_extension in discovered_jinja_extensions
        ],
    )
    for filter_plugin in discovered_jinja_filter_plugins:
        try:
            jinja_env.filters[filter_plugin.name] = filter_plugin.load()
        except AttributeError:
            print(
                f"Could not load Jinja filter plugin: {filter_plugin.name}. "
                "Possibly because {filter_plugin.value} is not a valid object reference."
            )
    return jinja_env


async def process_non_markdown_file(filepath: Path):
    CONTENT_DIR = get_content_directory()
    mimetype, _ = mimetypes.guess_type(filepath, strict=False)
    relative_filepath = filepath.relative_to(CONTENT_DIR)
    build_filepath = get_build_directory() / relative_filepath
    output_file = Path(build_filepath)
    output_file.parent.mkdir(exist_ok=True, parents=True)

    # Copy file to build directory
    shutil.copyfile(filepath, build_filepath)

    # Create srcset images
    if mimetype in [
        mimetypes.types_map[".jpg"],
        mimetypes.types_map[".png"],
    ]:
        await generate_images_for_srcset(filepath)


async def write_html_file(
    file_data: MarkdownFileData,
    file_data_list: list[MarkdownFileData],
    file_data_by_directory: dict[Path, list[MarkdownFileData]],
    release: bool,
    jinja_env: Environment,
):
    extra_context: TemplateContext = {}
    # Gather data from other files in this directory if this is an index file
    if file_data.path.name == "index.md":
        sibling_pages = [
            {
                "url": content_path_to_url(f.path),
                **f.front_matter,
            }
            for f in file_data_list
            if f.path != file_data.path
        ]
        extra_context["sibling_pages"] = sibling_pages
    folder_in_build = convert_content_path_to_directory_in_build(file_data.path)

    schema_type = file_data.front_matter.get("@type")
    if not schema_type:
        raise ValueError(
            f"Required @type value missing in file or TOML front matter invalid: "
            f"{file_data.path}"
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

    validate_front_matter_as_schema(file_data.path, front_matter, warning_console)

    schema_type_tag = f'<script type="application/ld+json">{schema_data}</script>'

    template_context = {
        "body": file_data.body,
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


@app.async_command()
async def build(release=True):
    """Generates HTML content from Markdown files."""
    update_settings()
    jinja_env = get_jinja_env()
    os.environ.setdefault(f"{ENV_VAR_PREFIX}BUILD_MODE", "prod" if release else "dev")
    CONTENT_DIR = get_content_directory()
    BUILD_DIR = get_build_directory()
    start = datetime.now()
    path = Path(CONTENT_DIR)
    file_data_by_directory: DirectoryFileData = {}
    if not BUILD_DIR.exists():
        BUILD_DIR.mkdir(parents=True)

    markdown_tasks: list[Coroutine] = []
    non_markdown_tasks: list[Coroutine] = []

    for filepath in path.glob("**/*.*"):
        # Handle images and other files
        if filepath.suffix != ".md":
            non_markdown_tasks.append(process_non_markdown_file(filepath))
            continue

        # Handle Markdown files

        # Extract filepath for storing context data and writing out
        relative_filepath = filepath.relative_to(CONTENT_DIR)
        directory = relative_filepath.parent
        if directory not in file_data_by_directory:
            file_data_by_directory[directory] = []

        # Convert Markdown file to HTML
        body, front_matter = convert_markdown_file_to_html(filepath)
        file_data = MarkdownFileData(
            body=body,
            front_matter=front_matter,
            path=relative_filepath,
        )
        file_data_by_directory[directory].append(file_data)

    non_markdown_tasks.append(write_sitemap_file(file_data_by_directory))

    # Sort file data by publishedDate/createdDate, descending, if present
    file_data_by_directory = sort_directory_file_data_by_date(file_data_by_directory)

    for file_data_list in file_data_by_directory.values():
        for file_data in file_data_list:
            markdown_tasks.append(
                write_html_file(
                    file_data,
                    file_data_list,
                    file_data_by_directory,
                    release,
                    jinja_env,
                )
            )

    content_dir_relative = CONTENT_DIR.relative_to(Path.cwd())
    print(f"Blurring {len(markdown_tasks)} Markdown files from: {content_dir_relative}")

    await asyncio.gather(*markdown_tasks)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    for non_markdown_task in non_markdown_tasks:
        await asyncio.to_thread(lambda: loop.run_until_complete(non_markdown_task))

    end = datetime.now()

    difference = end - start
    print(f"Built site in {difference.total_seconds()} seconds")


async def build_development():
    await build(release=False)


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    update_settings()
    os.environ.setdefault(f"{ENV_VAR_PREFIX}BUILD_MODE", "dev")

    SETTINGS["RUNSERVER"] = True

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(build_development())

    livereload_server = Server()
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*",
        lambda: event_loop.create_task(build_development()),
    )
    livereload_server.watch(
        f"{SETTINGS['TEMPLATES_DIRECTORY_NAME']}/**/*",
        lambda: event_loop.create_task(build_development()),
    )
    livereload_server.watch(
        "blurry.toml", lambda: event_loop.create_task(build_development())
    )
    livereload_server.serve(
        host=SETTINGS["DEV_HOST"], port=SETTINGS["DEV_PORT"], root=get_build_directory()
    )


def main():
    app()
