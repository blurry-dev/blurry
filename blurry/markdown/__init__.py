from pathlib import Path
from typing import Any
from typing import Type
from typing import TypeGuard

import mistune
from mistune import BlockState
from mistune.plugins.abbr import abbr
from mistune.plugins.def_list import def_list
from mistune.plugins.footnotes import footnotes
from mistune.plugins.formatting import strikethrough
from mistune.plugins.table import table
from mistune.plugins.task_lists import task_lists
from mistune.plugins.url import url
from mistune.util import escape
from wand.image import Image

from .front_matter import parse_front_matter
from .renderer_functions.render_video import render_video
from blurry.images import add_image_width_to_path
from blurry.images import generate_sizes_string
from blurry.images import generate_srcset_string
from blurry.images import get_widths_for_image_width
from blurry.plugins import discovered_markdown_plugins
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS
from blurry.types import is_str
from blurry.utils import build_path_to_url
from blurry.utils import content_path_to_url
from blurry.utils import convert_relative_path_in_markdown_to_relative_build_path
from blurry.utils import path_to_url_pathname
from blurry.utils import remove_lazy_loading_from_first_image
from blurry.utils import resolve_relative_path_in_markdown

CONTENT_DIR = get_content_directory()
THUMBNAIL_WIDTH = SETTINGS.get("THUMBNAIL_WIDTH")


class BlurryRenderer(mistune.HTMLRenderer):
    """Renderer that converts relative content URLs to build URLs."""

    filepath: Path

    def image(self, alt, url, title=None) -> str:
        # Improve images:
        # - Converts relative paths to web server paths
        # - Convert to <picture> tag with AVIF <source>
        # - Adds srcset & sizes attributes
        # - Adds width & height attributes
        src = self.safe_url(url)

        attributes: dict[str, str] = {
            "alt": alt,
            "src": src,
            "loading": "lazy",
        }
        source_tag = ""

        # Make local images responsive
        if src.startswith("."):
            # Convert relative path to URL pathname
            absolute_path = resolve_relative_path_in_markdown(src, self.filepath)
            extension = absolute_path.suffix.removeprefix(".")
            src = path_to_url_pathname(absolute_path)
            attributes["src"] = src

            if extension.lower() in SETTINGS.get("VIDEO_EXTENSIONS"):
                return render_video(src, absolute_path, extension, title=alt)

            # Tailor srcset and sizes to image width
            with Image(filename=str(absolute_path)) as img:
                image_width = img.width
                attributes["width"] = image_width
                attributes["height"] = img.height

            if extension in ["webp", "gif"]:
                source_tag = ""
            else:
                image_widths = get_widths_for_image_width(image_width)

                attributes["sizes"] = generate_sizes_string(image_widths)
                attributes["srcset"] = generate_srcset_string(src, image_widths)
                avif_srcset = generate_srcset_string(
                    src.replace(extension, "avif"), image_widths
                )
                source_tag = '<source srcset="{}" sizes="{}" />'.format(
                    avif_srcset, attributes["sizes"]
                )

        attributes_str = " ".join(
            f'{name}="{value}"' for name, value in attributes.items()
        )

        return (
            f"<figure>"
            f"<picture>{source_tag}<img {attributes_str} /></picture>"
            f'<figcaption>{attributes["alt"]}</figcaption>'
            f"</figure>"
        )

    def link(self, text, url, title: str | None = None) -> str:
        link_is_relative = url.startswith(".")
        if link_is_relative:
            url = convert_relative_path_in_markdown_to_relative_build_path(url)

        if text is None:
            text = url
        attrs = {
            "href": self.safe_url(url),
        }
        if title:
            attrs["title"] = escape(title)
        if not link_is_relative:
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener"

        attrs_string = " ".join(
            f'{attribute}="{value}"' for attribute, value in attrs.items()
        )

        return f"<a {attrs_string}>{text}</a>"


def is_blurry_renderer(
    renderer: mistune.HTMLRenderer,
) -> TypeGuard[Type[BlurryRenderer]]:
    return isinstance(renderer, BlurryRenderer)


renderer = BlurryRenderer(escape=False)
markdown = mistune.Markdown(
    renderer,
    plugins=[
        abbr,
        def_list,
        footnotes,
        strikethrough,
        table,
        task_lists,
        url,
    ]
    + [plugin.load() for plugin in discovered_markdown_plugins],
)


def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict[str, Any]]:
    if not markdown.renderer:
        raise Exception("Blurry markdown renderer not set on Mistune Markdown instance")

    BUILD_DIR = get_build_directory()
    # Add filepath to the renderer to resolve relative paths
    if not is_blurry_renderer(markdown.renderer):
        raise Exception(
            f"Markdown renderer is not BlurryRenderer {repr(markdown.renderer)}"
        )
    markdown.renderer.filepath = filepath
    initial_state = BlockState()
    initial_state.env["__file__"] = str(filepath)  # type: ignore
    markdown_text, state = parse_front_matter(markdown, state=initial_state)
    html, state = markdown.parse(markdown_text, state=state)

    if not is_str(html):
        raise Exception(f"Expected html to be a string but got: {type(html)}")

    # Post-process HTML
    html = remove_lazy_loading_from_first_image(html)

    # Seed front_matter with schema_data from config file
    front_matter: dict[str, Any] = dict(SETTINGS.get("SCHEMA_DATA", {}))
    front_matter.update(state.env.get("front_matter", {}))

    # Add inferred/computed/relative values
    front_matter.update({"url": content_path_to_url(filepath.relative_to(CONTENT_DIR))})
    if image := front_matter.get("image"):
        image_path = filepath.parent / Path(image)
        front_matter["image"] = content_path_to_url(image_path)
        # Add thumbnail URL, using the full image if the thumbnail doesn't exist
        thumbnail_image_path = add_image_width_to_path(image_path, THUMBNAIL_WIDTH)
        thumbnail_image_build_path = BUILD_DIR / thumbnail_image_path.relative_to(
            CONTENT_DIR
        )
        if thumbnail_image_build_path.exists():
            front_matter["thumbnailUrl"] = build_path_to_url(thumbnail_image_build_path)
        else:
            front_matter["thumbnailUrl"] = front_matter["image"]
    return html, front_matter
