from dataclasses import dataclass
from pathlib import Path

import htmlmin
import typer
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from livereload import Server

from blurry.constants import BUILD_DIR
from blurry.constants import CONTENT_DIR
from blurry.constants import TEMPLATE_DIR
from blurry.utils import convert_content_path_to_build_directory
from blurry.utils import convert_markdown_file_to_html
from blurry.utils import write_index_file_creating_path

app = typer.Typer()

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
)


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

    for file_data_list in file_data_by_directory.values():
        for file_data in file_data_list:
            extra_context = {}
            # Gather data from other files in this directory if this is an index file
            if str(file_data.path).endswith("index.md"):
                sibling_data = {
                    f.path: f.front_matter
                    for f in file_data_list
                    if f.path != file_data.path
                }
                extra_context["sibling_data"] = sibling_data
            build_folder = convert_content_path_to_build_directory(file_data.path)

            schema_type = file_data.front_matter["@type"]
            template = env.get_template(f"{schema_type}.html")
            html = template.render(
                body=file_data.body, **file_data.front_matter, **extra_context
            )

            if release:
                # Minify HTML
                html = htmlmin.minify(html)

            # Write file
            write_index_file_creating_path(build_folder, html)


def build_development():
    build(release=False)


@app.command()
def runserver():
    """Starts HTTP server with live reloading."""
    livereload_server = Server()
    livereload_server.watch("content/**/*", build_development)
    livereload_server.watch("templates/**/*", build_development)
    livereload_server.serve(port="8000", root=BUILD_DIR)


def main():
    app()
