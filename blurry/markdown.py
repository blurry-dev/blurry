from pathlib import Path
from typing import Any

import mistune
from docdata.yamldata import get_data
from mistune.scanner import escape_html
from wand.image import Image

from blurry.images import generate_sizes_string
from blurry.images import generate_srcset_string
from blurry.images import get_widths_for_image_width
from blurry.utils import convert_relative_path_in_markdown_to_relative_build_path
from blurry.utils import path_to_url_pathname
from blurry.utils import resolve_relative_path_in_markdown


class BlurryRenderer(mistune.HTMLRenderer):
    """Renderer that converts relative content URLs to build URLs."""

    filepath: Path

    def image(self, src: str, alt="", title=None) -> str:
        # Improve images:
        # - Converts relative paths to web server paths
        # - Convert to <picture> tag with AVIF <source>
        # - Adds srcset & sizes attributes
        # - Adds width & height attributes
        src = self._safe_url(src)
        attributes = {
            "alt": escape_html(alt),
            "src": src,
        }
        source_tag = ""

        if title:
            attributes["title"] = escape_html(title)

        # Make local images responsive
        if src.startswith("."):
            # Convert relative path to URL pathname
            absolute_path = resolve_relative_path_in_markdown(src, self.filepath)
            img_extension = absolute_path.suffix
            src = path_to_url_pathname(absolute_path)
            attributes["src"] = src

            # Tailor srcset and sizes to image width
            with Image(filename=str(absolute_path)) as img:
                image_width = img.width
                attributes["width"] = image_width
                attributes["height"] = img.height
            image_widths = get_widths_for_image_width(image_width)

            attributes["sizes"] = generate_sizes_string(image_widths)
            attributes["srcset"] = generate_srcset_string(src, image_widths)
            avif_srcset = generate_srcset_string(
                src.replace(img_extension, ".avif"), image_widths
            )
            source_tag = (
                f'<source srcset="{avif_srcset}" sizes="{attributes["sizes"]}" />'
            )

        attributes_str = " ".join(
            f'{name}="{value}"' for name, value in attributes.items()
        )

        return f"<picture>{source_tag}<img {attributes_str} /></picture>"

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
    # Add filepath to the renderer to resolve relative paths
    markdown.renderer.filepath = filepath
    html = markdown.read(str(filepath), state)
    front_matter: dict[str, Any] = state.get("front_matter", {})
    return html, front_matter
