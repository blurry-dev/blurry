import asyncio
import concurrent.futures
import dataclasses
import importlib
import json
import mimetypes
import os
import pkgutil
import shutil
import sys
from copy import deepcopy
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment
from livereload import Server
from rich import print
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TaskProgressColumn
from rich.progress import TextColumn

from blurry.async_typer import AsyncTyper
from blurry.cli import print_blurry_name
from blurry.cli import print_plugin_table
from blurry.constants import ENV_VAR_PREFIX
from blurry.images import generate_images_for_srcset
from blurry.markdown import convert_markdown_file_to_html
from blurry.open_graph import open_graph_meta_tags
from blurry.plugins import discovered_html_plugins
from blurry.schema_validation import validate_front_matter_as_schema
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS
from blurry.settings import update_settings
from blurry.sitemap import write_sitemap_file
from blurry.templates import get_jinja_env
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


app = AsyncTyper()


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


def write_html_file(
    filepath: Path,
    file_data_by_directory: dict[Path, list[MarkdownFileData]],
    release: bool,
    jinja_env: Environment,
):
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

    file_data = [
        f for f in file_data_by_directory[filepath.parent] if f.path == filepath
    ][0]
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

    validate_front_matter_as_schema(filepath, front_matter, warning_console)

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


def gather_file_data_by_directory() -> DirectoryFileData:
    # Sort file data by publishedDate/createdDate, descending, if present
    file_data_by_directory: DirectoryFileData = {}
    content_directory = get_content_directory()

    markdown_future_to_path: dict[concurrent.futures.Future, Path] = {}
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for filepath in content_directory.rglob("*.md"):
            # Extract filepath for storing context data and writing out
            relative_filepath = filepath.relative_to(content_directory)

            # Convert Markdown file to HTML
            future = executor.submit(convert_markdown_file_to_html, filepath)
            markdown_future_to_path[future] = relative_filepath

        for future in concurrent.futures.as_completed(markdown_future_to_path):
            body, front_matter = future.result()
            relative_filepath = markdown_future_to_path[future]
            file_data = MarkdownFileData(
                body=body,
                front_matter=front_matter,
                path=relative_filepath,
            )
            parent_directory = relative_filepath.parent
            try:
                file_data_by_directory[parent_directory].append(file_data)
            except KeyError:
                file_data_by_directory[parent_directory] = [file_data]

    concurrent.futures.wait(markdown_future_to_path)

    return sort_directory_file_data_by_date(file_data_by_directory)


@app.command(name="clean")
def clean_build_directory():
    """Removes the build directory for a clean build."""
    update_settings()
    build_directory = get_build_directory()

    try:
        shutil.rmtree(build_directory)
    except FileNotFoundError:
        pass


@app.async_command()
async def build(release=True, clean: bool = False):
    """Generates HTML content from Markdown files."""
    start = datetime.now()

    if release:
        print_blurry_name()
        print_plugin_table()

    update_settings()
    build_directory = get_build_directory()

    if clean:
        clean_build_directory()

    build_directory.mkdir(parents=True, exist_ok=True)

    content_directory = get_content_directory()
    build_directory.mkdir(parents=True, exist_ok=True)
    jinja_env = get_jinja_env()

    os.environ.setdefault(f"{ENV_VAR_PREFIX}BUILD_MODE", "prod" if release else "dev")

    file_data_by_directory = gather_file_data_by_directory()

    markdown_task_count = 0
    non_markdown_task_count = 1  # sitemap

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        transient=True,
    ) as progress:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            markdown_task = progress.add_task("[blue]Markdown")
            other_task = progress.add_task("[blue]Other")

            sitemap_future = executor.submit(write_sitemap_file, file_data_by_directory)
            sitemap_future.add_done_callback(lambda _: progress.advance(other_task))

            for filepath in content_directory.rglob("*"):
                if filepath.is_dir():
                    continue
                if filepath.suffix == ".md":
                    markdown_future = executor.submit(
                        write_html_file,
                        filepath.relative_to(content_directory),
                        file_data_by_directory,
                        release,
                        jinja_env,
                    )
                    markdown_task_count += 1
                    progress.update(markdown_task, total=markdown_task_count)
                    markdown_future.add_done_callback(
                        lambda _: progress.advance(markdown_task)
                    )
                    continue
                other_future = executor.submit(
                    process_non_markdown_file,
                    filepath,
                    file_data_by_directory,
                    jinja_env,
                )
                non_markdown_task_count += 1
                progress.update(other_task, total=non_markdown_task_count)
                other_future.add_done_callback(lambda _: progress.advance(other_task))

            print(
                f"Blurring {markdown_task_count} Markdown files and {non_markdown_task_count} other files"
            )

    end = datetime.now()

    difference = end - start
    print(f"Built site in {difference.total_seconds()} seconds")


async def build_development():
    await build(release=False)


async def reload_local_plugins_and_build():
    """Reloads a project's local modules and performs a dev build"""
    cwd = str(Path.cwd())

    for _, package_name, _ in pkgutil.iter_modules([cwd]):
        try:
            module = sys.modules[package_name]
        except KeyError:
            continue
        importlib.reload(module)

    await build_development()


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    print_blurry_name()
    print_plugin_table()

    update_settings()
    os.environ.setdefault(f"{ENV_VAR_PREFIX}BUILD_MODE", "dev")

    SETTINGS["RUNSERVER"] = True

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(build_development())

    jinja_env = get_jinja_env()

    def handle_changed_jinja_files(filepaths: list[str]):
        file_data_by_directory = gather_file_data_by_directory()
        for filepath in filepaths:
            process_jinja_file(
                Path.cwd() / filepath,
                jinja_env,
                file_data_by_directory,
            )

    def handle_changed_markdown_files(filepaths: list[str]):
        file_data_by_directory = gather_file_data_by_directory()
        content_directory = get_content_directory()
        for filepath in filepaths:
            write_html_file(
                filepath=(Path.cwd() / filepath).relative_to(content_directory),
                file_data_by_directory=file_data_by_directory,
                release=False,
                jinja_env=jinja_env,
            )

    livereload_server = Server()
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*.jinja", handle_changed_jinja_files
    )
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*.md",
        handle_changed_markdown_files,
    )
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*",
        lambda: event_loop.create_task(build_development()),
        ignore=lambda filepath: any(
            [
                filepath.endswith(".md"),
                filepath.endswith(".jinja"),
                Path(filepath).is_dir(),
            ]
        ),
    )
    livereload_server.watch(
        f"{SETTINGS['TEMPLATES_DIRECTORY_NAME']}/**/*",
        lambda: event_loop.create_task(build_development()),
        ignore=lambda filepath: Path(filepath).is_dir(),
    )
    livereload_server.watch(
        "./**/*.py",
        lambda: event_loop.create_task(reload_local_plugins_and_build()),
    )
    livereload_server.watch(
        "blurry.toml", lambda: event_loop.create_task(build_development())
    )
    livereload_server.serve(
        host=SETTINGS["DEV_HOST"], port=SETTINGS["DEV_PORT"], root=get_build_directory()
    )


def main():
    app()
