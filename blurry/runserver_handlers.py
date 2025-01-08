from pathlib import Path

from jinja2 import Environment

from blurry.file_processors import process_jinja_file
from blurry.file_processors import write_html_file
from blurry.gather_file_data_by_directory import gather_file_data_by_directory
from blurry.settings import get_content_directory


def handle_changed_jinja_files(filepaths: list[str], jinja_env: Environment):
    file_data_by_directory = gather_file_data_by_directory()
    for filepath in filepaths:
        process_jinja_file(
            Path.cwd() / filepath,
            jinja_env,
            file_data_by_directory,
        )


def handle_changed_markdown_files(filepaths: list[str], jinja_env: Environment):
    file_data_by_directory = gather_file_data_by_directory()
    content_directory = get_content_directory()
    for filepath in filepaths:
        write_html_file(
            filepath=(Path.cwd() / filepath).relative_to(content_directory),
            file_data_by_directory=file_data_by_directory,
            release=False,
            jinja_env=jinja_env,
        )


def rebuild_markdown_files(jinja_env: Environment):
    content_directory = get_content_directory()
    markdown_paths = content_directory.rglob("*.md")
    markdown_files = [str(p) for p in markdown_paths]
    handle_changed_markdown_files(markdown_files, jinja_env)
