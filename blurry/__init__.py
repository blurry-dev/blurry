from dataclasses import dataclass
from pathlib import Path
from typing import Any

import htmlmin
import mistune
import typer
from docdata.yamldata import get_data
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from livereload import Server

from .utils import write_file_creating_path

app = typer.Typer()

CURR_DIR = Path.cwd()
BUILD_DIR = CURR_DIR / "build"
CONTENT_DIR = CURR_DIR / "content"
TEMPLATE_DIR = CURR_DIR / "templates"


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
)


def parse_front_matter(_, s: str, state: dict) -> tuple[str, dict]:
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md: mistune.Markdown) -> None:
    md.before_parse_hooks.append(parse_front_matter)


renderer = mistune.HTMLRenderer(escape=False)
markdown = mistune.Markdown(renderer, plugins=[plugin_front_matter])


def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict]:
    state: dict[str, Any] = {}
    html = markdown.read(str(filepath), state)
    front_matter: dict[str, Any] = state.get("front_matter", {})
    return html, front_matter


def convert_content_path_to_build_path(path: Path) -> Path:
    return BUILD_DIR.joinpath(path.with_suffix(""))


@dataclass
class MarkdownFileData:
    body: str
    front_matter: dict
    path: Path


@app.command()
def build(release=True):
    """Generates HTML content from Markdown files."""
    # structured_data_by_directory = {}
    path = Path(CONTENT_DIR)
    file_data_by_directory: dict[Path, list[MarkdownFileData]] = {}
    for filepath in path.glob("**/*.md"):
        # Extract filepath for storing context data and writing out
        relative_filepath = filepath.relative_to(CONTENT_DIR)
        directory = relative_filepath.parent
        if directory not in file_data_by_directory:
            file_data_by_directory[directory] = []

        # Convert Markdown file to HTML
        body, front_matter = convert_markdown_file_to_html(filepath)
        file_data = MarkdownFileData(body, front_matter, relative_filepath)
        file_data_by_directory[directory].append(file_data)

    for directory, file_data_list in file_data_by_directory.items():
        directory_file_data = {f.path: f.front_matter for f in file_data_list}

        for file_data in file_data_list:
            sibling_data = directory_file_data.copy()
            del sibling_data[file_data.path]
            build_folder = convert_content_path_to_build_path(file_data.path)

            schema_type = file_data.front_matter["@type"]
            template = env.get_template(f"{schema_type}.html")
            html = template.render(
                body=file_data.body,
                sibling_pages=sibling_data,
                **file_data.front_matter,
            )

            if release:
                # Minify HTML
                html = htmlmin.minify(html)

            # Write file
            write_file_creating_path(build_folder, html)


def build_development():
    build(release=False)


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    livereload_server = Server()
    livereload_server.watch("content/**.md", build_development)
    livereload_server.watch("templates/*", build_development)
    livereload_server.serve(port="8000", root=BUILD_DIR)


def main():
    app()
