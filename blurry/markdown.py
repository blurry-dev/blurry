from typing import Any
import mistune
from mistune.scanner import escape_html
from pathlib import Path
from docdata.yamldata import get_data

from blurry.utils import convert_relative_path_in_markdown_to_relative_build_path


class BlurryRenderer(mistune.HTMLRenderer):
    """Renderer that converts relative content URLs to build URLs."""

    def image(self, src, alt="", title=None):
        if src.startswith("."):
            src = convert_relative_path_in_markdown_to_relative_build_path(src)
        return super().image(src, alt, title)

    def link(self, link, text=None, title=None):
        if link.startswith("."):
            link = convert_relative_path_in_markdown_to_relative_build_path(link)
        return super().link(link, text, title)


def parse_front_matter(_, s: str, state: dict) -> tuple[str, dict]:
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md: mistune.Markdown) -> None:
    md.before_parse_hooks.append(parse_front_matter)


renderer = BlurryRenderer(escape=False)
markdown = mistune.Markdown(renderer, plugins=[plugin_front_matter])


def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict]:
    state: dict[str, Any] = {}
    html = markdown.read(str(filepath), state)
    front_matter: dict[str, Any] = state.get("front_matter", {})
    return html, front_matter
