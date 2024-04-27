from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import TypeAlias
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
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS
from blurry.types import is_str
from blurry.utils import content_path_to_url
from blurry.utils import convert_relative_path_in_markdown_file_to_pathname
from blurry.utils import path_to_url_pathname
from blurry.utils import remove_lazy_loading_from_first_image
from blurry.utils import resolve_relative_path_in_markdown


# https://schema.org/ImageObject
ImageObject: TypeAlias = dict


class BlurryRenderer(mistune.HTMLRenderer):
    """Renderer that converts relative content URLs to build URLs."""

    filepath: Path

    def image(self, text, url, title=None) -> str:
        # Improve images:
        # - Converts relative paths to web server paths
        # - Convert to <picture> tag with AVIF <source>
        # - Adds srcset & sizes attributes
        # - Adds width & height attributes
        src = self.safe_url(url)

        attributes: dict[str, str] = {
            "alt": text,
            "src": src,
            "loading": "lazy",
        }
        if title:
            attributes["title"] = title

        source_tag = ""

        # Make local images responsive
        if src.startswith("."):
            # Convert relative path to URL pathname
            absolute_path = resolve_relative_path_in_markdown(src, self.filepath)
            extension = absolute_path.suffix.removeprefix(".")
            src = path_to_url_pathname(absolute_path)
            attributes["src"] = src

            if extension.lower() in SETTINGS.get("VIDEO_EXTENSIONS"):
                return render_video(src, absolute_path, extension, title=title)

            # Tailor srcset and sizes to image width
            with Image(filename=str(absolute_path)) as img:
                image_width = img.width
                image_height = img.height
                # The .animated property doesn't always detect animated .webp images
                # and .webp is optimized enough not to benefit much from .avif
                image_is_animated = img.animation or extension.lower() == "webp"
                attributes["width"] = image_width
                attributes["height"] = image_height

            if image_is_animated:
                attributes_str = " ".join(
                    f'{name}="{value}"' for name, value in attributes.items()
                )
                return f"<img {attributes_str} >"

            image_widths = get_widths_for_image_width(image_width)

            attributes["sizes"] = generate_sizes_string(image_widths)
            attributes["srcset"] = generate_srcset_string(src, image_widths)
            avif_srcset = generate_srcset_string(
                src.replace(extension, "avif"), image_widths
            )
            source_tag = '<source srcset="{}" sizes="{}" type="image/avif" />'.format(
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
        CONTENT_DIR = get_content_directory()
        link_is_relative = url.startswith(".")
        if link_is_relative:
            url = convert_relative_path_in_markdown_file_to_pathname(
                content_directory=CONTENT_DIR, filepath=self.filepath, relative_path=url
            )

        if text is None:
            text = url
        attrs = {
            "href": self.safe_url(url),
        }
        if title:
            attrs["title"] = escape(title)
        if link_is_relative:
            attrs["rel"] = "noreferrer"
        else:
            attrs["target"] = "_blank"
            attrs["rel"] = "noopener"

        attrs_string = " ".join(
            f'{attribute}="{value}"' for attribute, value in attrs.items()
        )

        return f"<a {attrs_string}>{text}</a>"


def is_blurry_renderer(
    renderer: mistune.HTMLRenderer,
) -> TypeGuard[type[BlurryRenderer]]:
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
    CONTENT_DIR = get_content_directory()
    if not markdown.renderer:
        raise Exception("Blurry markdown renderer not set on Mistune Markdown instance")

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
    # https://schema.org/image
    # https://schema.org/thumbnailUrl
    front_matter.update({"url": content_path_to_url(filepath.relative_to(CONTENT_DIR))})
    if image := front_matter.get("image"):
        image_copy = deepcopy(image)
        relative_image_path = get_relative_image_path_from_image_property(image_copy)
        image_path = resolve_relative_path_in_markdown(relative_image_path, filepath)
        front_matter["image"] = update_image_with_url(image_copy, image_path)
        front_matter["thumbnailUrl"] = image_path_to_thumbnailUrl(image_path)
    return html, front_matter


def image_path_to_thumbnailUrl(image_path: Path):
    THUMBNAIL_WIDTH = SETTINGS.get("THUMBNAIL_WIDTH")
    thumbnail_image_path = add_image_width_to_path(image_path, THUMBNAIL_WIDTH)
    return content_path_to_url(thumbnail_image_path)


def get_relative_image_path_from_image_property(image: str | ImageObject) -> str:
    if isinstance(image, ImageObject):
        return image["contentUrl"]
    return image


def update_image_with_url(image: str | ImageObject, image_path: Path):
    image_url = content_path_to_url(image_path)
    if isinstance(image, str):
        return image_url
    if isinstance(image, ImageObject):
        image["contentUrl"] = image_url
        return image
