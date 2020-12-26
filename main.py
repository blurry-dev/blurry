from typing import Any

import mistune
import os
from docdata.yamldata import get_data
from formic import FileSet
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server

PATH = os.path.dirname(os.path.abspath(__file__))


env = Environment(
    loader=FileSystemLoader(os.path.join(PATH, "templates")),
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
    meta: dict[str, Any] = state.get("front_matter", {})
    return html, meta


def build_site():
    template = env.get_template("post.html")
    for filepath in FileSet(include="content/**.md"):
        html, meta = convert_markdown_file_to_html(filepath)
        print(template.render(body=html, **meta))


def start_livereload():
    livereload_server = Server()
    for filepath in FileSet(include="content/**.md"):
        livereload_server.watch(filepath, build_site)
    livereload_server.serve(port="8000", root="build")


if __name__ == "__main__":
    start_livereload()
