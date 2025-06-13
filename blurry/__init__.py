import asyncio
import concurrent.futures
import importlib
import os
import pkgutil
import sys
from datetime import datetime
from pathlib import Path

from livereload import Server
from rich import print
from rich.console import Console
from rich.progress import BarColumn
from rich.progress import Progress
from rich.progress import TaskProgressColumn
from rich.progress import TextColumn

from blurry.async_typer import AsyncTyper
from blurry.cli import check_avif_support, print_blurry_name
from blurry.cli import print_plugin_table
from blurry.commands.clean import clean_build_directory
from blurry.commands.init import initialize_new_project
from blurry.commands.version import print_blurry_version
from blurry.constants import ENV_VAR_PREFIX
from blurry.file_processors import process_non_markdown_file
from blurry.file_processors import write_html_file
from blurry.gather_file_data_by_directory import gather_file_data_by_directory
from blurry.runserver_handlers import handle_changed_jinja_files
from blurry.runserver_handlers import handle_changed_markdown_files
from blurry.runserver_handlers import rebuild_markdown_files
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import get_settings
from blurry.settings import update_settings
from blurry.sitemap import write_sitemap_file
from blurry.templates import get_jinja_env


warning_console = Console(stderr=True, style="bold yellow")


app = AsyncTyper(no_args_is_help=True)


@app.command(name="clean")
def clean_command():
    clean_build_directory()


@app.command(name="init")
def init_command(name: str | None = None, domain: str | None = None):
    initialize_new_project(name, domain)


@app.command(name="version")
def version_command():
    print_blurry_version()


@app.async_command()
async def build(release=True, clean: bool = False):
    """Generates HTML content from Markdown files."""
    start = datetime.now()

    if release:
        update_settings()
        print_blurry_name()
        print_plugin_table()
        check_avif_support(console=warning_console)

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

                    def on_markdown_file_processed(future: concurrent.futures.Future):
                        progress.advance(markdown_task)
                        if exception := future.exception():
                            print(f"{filepath}: could not process file - {exception}")

                    markdown_future = executor.submit(
                        write_html_file,
                        filepath.relative_to(content_directory),
                        file_data_by_directory,
                        release,
                        jinja_env,
                    )
                    markdown_task_count += 1
                    progress.update(markdown_task, total=markdown_task_count)
                    markdown_future.add_done_callback(on_markdown_file_processed)
                    continue
                other_future = executor.submit(
                    process_non_markdown_file,
                    filepath,
                    file_data_by_directory,
                    jinja_env,
                )
                non_markdown_task_count += 1
                progress.update(other_task, total=non_markdown_task_count)

                def on_non_markdown_file_processed(future: concurrent.futures.Future):
                    progress.advance(other_task)
                    if exception := future.exception():
                        print(f"{filepath}: could not process file - {exception}")

                other_future.add_done_callback(on_non_markdown_file_processed)

            print(
                f"Blurring {markdown_task_count} Markdown files and {non_markdown_task_count} other files"
            )

    end = datetime.now()

    difference = end - start
    print(f"Built site in {difference.total_seconds()} seconds")


async def reload_local_plugins_and_build():
    """Reloads a project's local modules and performs a dev build"""
    cwd = str(Path.cwd())

    for _, package_name, _ in pkgutil.iter_modules([cwd]):
        try:
            module = sys.modules[package_name]
        except KeyError:
            continue
        importlib.reload(module)

    await build(release=False)


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    print_blurry_name()
    print_plugin_table()
    check_avif_support(console=warning_console)

    SETTINGS = get_settings()
    os.environ.setdefault(f"{ENV_VAR_PREFIX}BUILD_MODE", "dev")

    SETTINGS["RUNSERVER"] = True

    event_loop = asyncio.get_event_loop()
    event_loop.create_task(build(release=False))

    jinja_env = get_jinja_env()

    livereload_server = Server()
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*.jinja",
        lambda filepaths: handle_changed_jinja_files(filepaths, jinja_env),
    )
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*.md",
        lambda filepaths: handle_changed_markdown_files(filepaths, jinja_env),
    )
    livereload_server.watch(
        f"{SETTINGS['CONTENT_DIRECTORY_NAME']}/**/*",
        lambda: event_loop.create_task(build(release=False)),
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
        lambda: rebuild_markdown_files(jinja_env),
        ignore=lambda filepath: Path(filepath).is_dir(),
    )
    livereload_server.watch(
        "./**/*.py",
        lambda: event_loop.create_task(reload_local_plugins_and_build()),
    )
    livereload_server.watch(
        "blurry.toml", lambda: event_loop.create_task(build(release=False))
    )
    livereload_server.serve(
        host=SETTINGS["DEV_HOST"], port=SETTINGS["DEV_PORT"], root=get_build_directory()
    )


def main():
    app()
