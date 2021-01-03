from typing import Any, Dict, Tuple

import htmlmin
import mistune
import os
import typer
from docdata.yamldata import get_data
from formic import FileSet
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

app = typer.Typer()

PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(PATH, "build")
TEMPLATE_DIR = os.path.join(PATH, "templates")


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


def convert_markdown_file_to_html(filename: str) -> Tuple[str, dict]:
    state: Dict[str, Any] = {}
    html = markdown.read(filename, state)
    front_matter: Dict[str, Any] = state.get("front_matter", {})
    return html, front_matter


def write_file_creating_path(directory_path: str, content: str):
    os.makedirs(directory_path, exist_ok=True)
    filepath = os.path.join(directory_path, "index.html")
    with open(filepath, "w") as buffer:
        buffer.write(content)


@app.command()
def build(release=True):
    """Generates HTML content from Markdown files."""
    structured_data_by_directory = {}
    for filepath in FileSet(include="content/**.md", exclude=["content/**index.md"]):
        # Extract filepath for storing context data and writing out
        filename_without_extension = os.path.splitext(os.path.basename(filepath))[0]
        relative_directory = os.path.join(BUILD_DIR, filename_without_extension)

        # Convert Markdown file to HTML
        body, front_matter = convert_markdown_file_to_html(filepath)

        # TODO: gather context for files in this directory
        template = env.get_template(front_matter["@type"])
        html = template.render(body=body, **front_matter)

        if release:
            # Minify HTML
            html = htmlmin.minify(html)

        # Write file
        write_file_creating_path(relative_directory, html)


def build_development():
    build(release=False)


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    livereload_server = Server()
    livereload_server.watch("content/**.md", build_development)
    livereload_server.watch("templates/*", build_development)
    livereload_server.serve(port="8000", root=BUILD_DIR)


if __name__ == "__main__":
    app()
