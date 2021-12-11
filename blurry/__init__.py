import asyncio
import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from mimetypes import guess_type
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
from blurry.images import generate_images_for_srcset
from blurry.markdown import convert_markdown_file_to_html
from blurry.open_graph import open_graph_meta_tags
from blurry.sitemap import write_sitemap_file
from blurry.types import MarkdownFileData
from blurry.utils import convert_content_path_to_directory_in_build
from blurry.utils import write_index_file_creating_path

app = typer.Typer()

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR), autoescape=select_autoescape(["html", "xml"])
)


def process_non_markdown_file(filepath: Path):
    mimetype, _ = guess_type(filepath)
    if not mimetype:
        return
    if mimetype.startswith("image"):
        # Create srcset images
        asyncio.run(generate_images_for_srcset(filepath))
    relative_filepath = filepath.relative_to(CONTENT_DIR)
    build_filepath = BUILD_DIR / relative_filepath
    if build_filepath.exists():
        return
    shutil.copyfile(filepath, build_filepath)


def write_html_file(
    file_data: MarkdownFileData, file_data_list: list[MarkdownFileData], release: bool
):
    extra_context = {}
    # Gather data from other files in this directory if this is an index file
    if file_data.path.name == "index.md":
        sibling_data = {
            f.path: f.front_matter for f in file_data_list if f.path != file_data.path
        }
        extra_context["sibling_data"] = sibling_data
    folder_in_build = convert_content_path_to_directory_in_build(file_data.path)

    schema_type = file_data.front_matter["@type"]
    template = env.get_template(f"{schema_type}.html")
    html = template.render(
        body=file_data.body,
        schema_data=json.dumps(file_data.front_matter),
        open_graph_tags=open_graph_meta_tags(file_data.front_matter),
        **file_data.front_matter,
        **extra_context,
    )

    if release:
        # Minify HTML
        html = htmlmin.minify(html)

    # Write file
    write_index_file_creating_path(folder_in_build, html)


@app.command()
def build(release=True):
    """Generates HTML content from Markdown files."""
    path = Path(CONTENT_DIR)
    file_data_by_directory: dict[Path, list[MarkdownFileData]] = {}
    if not BUILD_DIR.exists():
        BUILD_DIR.mkdir()

    with ProcessPoolExecutor() as executor:
        for filepath in path.glob("**/*.*"):
            # Handle images and other files
            if filepath.suffix != ".md":
                executor.submit(process_non_markdown_file, filepath)
                continue

            # Handle Markdown files

            # Extract filepath for storing context data and writing out
            relative_filepath = filepath.relative_to(CONTENT_DIR)
            directory = relative_filepath.parent
            if directory not in file_data_by_directory:
                file_data_by_directory[directory] = []

            # Convert Markdown file to HTML
            body, front_matter = convert_markdown_file_to_html(filepath)
            file_data = MarkdownFileData(body, front_matter, relative_filepath)
            file_data_by_directory[directory].append(file_data)

        executor.submit(write_sitemap_file, file_data_by_directory)

        for file_data_list in file_data_by_directory.values():
            for file_data in file_data_list:
                executor.submit(write_html_file, file_data, file_data_list, release)
        executor.shutdown()


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
