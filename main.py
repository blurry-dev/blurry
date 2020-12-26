from typing import Any

import mistune
import os
from docdata.yamldata import get_data
from formic import FileSet
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

PATH = os.path.dirname(os.path.abspath(__file__))
BUILD_DIR = os.path.join(PATH, "build")
TEMPLATE_DIR = os.path.join(PATH, "templates")


env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(["html", "xml"]),
)


def parse_front_matter(md, s, state):
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md):
    md.before_parse_hooks.append(parse_front_matter)


renderer = mistune.HTMLRenderer(escape=False)
markdown = mistune.Markdown(renderer, plugins=[plugin_front_matter])


def convert_markdown_file_to_html(filename: str) -> tuple[str, dict]:
    state: dict[str, Any] = {}
    html = markdown.read(filename, state)
    front_matter: dict[str, Any] = state.get("front_matter", {})
    return html, front_matter


def build_site():
    template = env.get_template("post.html")
    for filepath in FileSet(include="content/**.md"):
        # Convert Markdown file to HTML
        body, front_matter = convert_markdown_file_to_html(filepath)
        # TODO: add additional variables, like word count
        html = template.render(body=body, **front_matter)

        # Write file
        filename_without_extension = os.path.splitext(os.path.basename(filepath))[0]
        post_directory = os.path.join(BUILD_DIR, filename_without_extension)
        os.makedirs(post_directory, exist_ok=True)
        post_filepath = os.path.join(post_directory, "index.html")
        with open(post_filepath, "w") as buffer:
            buffer.write(html)


def start_livereload():
    livereload_server = Server()
    livereload_server.watch("content/**.md", build_site)
    livereload_server.watch("templates/**", build_site)
    livereload_server.serve(port="8000", root=BUILD_DIR)


if __name__ == "__main__":
    start_livereload()
