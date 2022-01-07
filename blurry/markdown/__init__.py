from pathlib import Path
from typing import Any
from typing import Type
from typing import TypeGuard

import mistune
from mistune.plugins import PLUGINS
from mistune.util import escape_html
from wand.image import Image

from .container import blurry_container
from .front_matter import blurry_front_matter
from blurry.constants import CONTENT_DIR
from blurry.images import add_image_width_to_path
from blurry.images import generate_sizes_string
from blurry.images import generate_srcset_string
from blurry.images import get_widths_for_image_width
from blurry.images import THUMBNAIL_WIDTH
from blurry.settings import SETTINGS
from blurry.utils import content_path_to_url
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
        attributes: dict[str, str] = {
            "alt": escape_html(alt),
            "src": src,
            "loading": "lazy",
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

            if img_extension in [".webp", ".gif"]:
                source_tag = ""
            else:
                image_widths = get_widths_for_image_width(image_width)

                attributes["sizes"] = generate_sizes_string(image_widths)
                attributes["srcset"] = generate_srcset_string(src, image_widths)
                avif_srcset = generate_srcset_string(
                    src.replace(img_extension, ".avif"), image_widths
                )
                source_tag = '<source srcset="{}" sizes="{}" loading="lazy" />'.format(
                    avif_srcset, attributes["sizes"]
                )

        attributes_str = " ".join(
            f'{name}="{value}"' for name, value in attributes.items()
        )

        return f'<picture loading="lazy">{source_tag}<img {attributes_str} /></picture>'

    def link(self, link: str, text: str | None = None, title: str | None = None) -> str:
        if link.startswith("."):
            link = convert_relative_path_in_markdown_to_relative_build_path(link)
        return super().link(link, text, title)


def is_blurry_renderer(
    renderer: mistune.HTMLRenderer,
) -> TypeGuard[Type[BlurryRenderer]]:
    return isinstance(renderer, BlurryRenderer)


renderer = BlurryRenderer(escape=False)
markdown = mistune.Markdown(
    renderer,
    plugins=[
        PLUGINS["table"],
        PLUGINS["task_lists"],
        PLUGINS["strikethrough"],
        PLUGINS["abbr"],
        PLUGINS["footnotes"],
        PLUGINS["url"],
        PLUGINS["def_list"],
        blurry_front_matter,
        blurry_container,
    ],
)


def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict[str, Any]]:
    state: dict[str, Any] = {}
    # Add filepath to the renderer to resolve relative paths
    if not is_blurry_renderer(markdown.renderer):
        raise Exception(
            f"Markdown renderer is not BlurryRenderer {repr(markdown.renderer)}"
        )
    markdown.renderer.filepath = filepath
    html = markdown.read(str(filepath), state)

    # Seed front_matter with schema_data from config file
    front_matter: dict[str, Any] = dict(SETTINGS.get("SCHEMA_DATA", {}))
    front_matter.update(state.get("front_matter", {}))

    # Add inferred/computed/relative values
    front_matter.update({"url": content_path_to_url(filepath.relative_to(CONTENT_DIR))})
    if image := front_matter.get("image"):
        front_matter["image"] = content_path_to_url(filepath.parent / Path(image))
        front_matter["thumbnailUrl"] = content_path_to_url(
            filepath.parent / add_image_width_to_path(Path(image), THUMBNAIL_WIDTH)
        )
    return html, front_matter
