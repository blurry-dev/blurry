from typing import Any, Dict, Tuple
from dataclasses import dataclass

import htmlmin
import mistune
import typer
from docdata.yamldata import get_data
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from pathlib import Path

from .utils import write_file_creating_path

app = typer.Typer()

CURR_DIR = Path.cwd()
BUILD_DIR = CURR_DIR / "build"
CONTENT_DIR = CURR_DIR / "content"
TEMPLATE_DIR = CURR_DIR / "templates"


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def parse_front_matter(_, s: str, state: dict) -> Tuple[str, dict]:
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md: mistune.Markdown) -> None:
    md.before_parse_hooks.append(parse_front_matter)


renderer = mistune.HTMLRenderer(escape=False)
markdown = mistune.Markdown(renderer, plugins=[plugin_front_matter])


def convert_markdown_file_to_html(filepath: Path) -> Tuple[str, dict]:
    state: Dict[str, Any] = {}
    html = markdown.read(str(filepath), state)
    front_matter: Dict[str, Any] = state.get("front_matter", {})
    return html, front_matter


def convert_content_path_to_build_path(content_path: Path) -> Path:

    return content_path


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
        if directory not in filepath:
            file_data_by_directory[directory] = []

        # Convert Markdown file to HTML
        body, front_matter = convert_markdown_file_to_html(filepath)
        file_data = MarkdownFileData(body, front_matter, relative_filepath)
        file_data_by_directory[directory].append(file_data)
        # TODO: create a separate loop that compiles the templates.

        # TODO: gather context for files in this directory
        build_folder = BUILD_DIR.joinpath(relative_filepath.with_suffix(""))

        schema_type = front_matter["@type"]
        template = env.get_template(f"{schema_type}.html")
        html = template.render(body=body, **front_matter)

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
