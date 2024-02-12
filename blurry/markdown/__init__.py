from copy import deepcopy
from pathlib import Path
from typing import Any
from typing import TypeAlias
from typing import TypeGuard

import json
from pyld import jsonld

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
                return render_video(src, absolute_path, extension, title=text)

            # Tailor srcset and sizes to image width
            with Image(filename=str(absolute_path)) as img:
                image_width = img.width
                image_height = img.height
                attributes["width"] = image_width
                attributes["height"] = image_height

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

SCHEMA_ORG = json.loads('{ "@vocab": "https://schema.org/" }')
def jsonld_document_loader(secure=False, fragments=[], **kwargs):
    """
    Create a Requests document loader.

    Can be used to setup extra Requests args such as verify, cert, timeout,
    or others.

    :param secure: require all requests to use HTTPS (default: False).
    :param fragments: the fragments of schema loaded as dicts
    :param **kwargs: extra keyword args for Requests get() call.

    :return: the RemoteDocument loader function.
    """
    from pyld.jsonld import JsonLdError

    def loader(ignored, options={}):
        """
        Retrieves JSON-LD from the dicts provided as fragments.

        :param ignored: this positional paramter is ignored, because the tomls fragments are side loaded

        :return: the RemoteDocument.
        """
        fragments_str = []
        for fragment in fragments:
            if not fragment.get('@context'):
                fragment['@context'] = SCHEMA_ORG
            fragments_str.append(json.dumps(fragment))
            # print("==========================")
            # print(json.dumps(fragment, indent=2))

        result = '[' + ','.join(fragments_str) + ']'
        # print(">>>>>>>>> ",result)

        doc = {
                'contentType': 'application/ld+json',
                'contextUrl': None,
                'documentUrl': None,
                'document': result
            }
        return doc

    return loader

def add_inferred_schema(local_front_matter: dict, filepath: Path) -> dict:
    CONTENT_DIR = get_content_directory()

    # Add inferred/computed/relative values
    local_front_matter.update({"url": content_path_to_url(filepath.relative_to(CONTENT_DIR))})

    # Add inferred/computed/relative values
    # https://schema.org/image
    # https://schema.org/thumbnailUrl
    if image := front_matter.get("image"):
        image_copy = deepcopy(image)
        relative_image_path = get_relative_image_path_from_image_property(image_copy)
        image_path = resolve_relative_path_in_markdown(relative_image_path, filepath)
        front_matter["image"] = update_image_with_url(image_copy, image_path)
        front_matter["thumbnailUrl"] = image_path_to_thumbnailUrl(image_path)

    return local_front_matter

def resolve_front_matter(state: dict, filepath: Path) -> tuple[dict[str, Any], str]:
    if SETTINGS.get("FRONT_MATTER_RESOLUTION") == "merge":
        try:
            global_schema = dict(SETTINGS.get("SCHEMA_DATA", {}))
            if not global_schema.get('@context'):
                global_schema['@context'] = SCHEMA_ORG

            local_schema = state.env.get("front_matter", {})
            top_level_type = local_schema.get("@type", None)
            if not local_schema.get('@context'):
                local_schema['@context'] = SCHEMA_ORG
            local_schema = add_inferred_schema(local_schema, filepath)
            jsonld.set_document_loader(jsonld_document_loader(fragments=[global_schema, local_schema]))
            front_matter: dict[str, Any] = jsonld.compact("ignore", SCHEMA_ORG)
        except Exception as e:
            print("merging front matter failed:", e)
            raise e
    else:
        # Seed front_matter with schema_data from config file
        front_matter: dict[str, Any] = dict(SETTINGS.get("SCHEMA_DATA", {}))
        front_matter.update(state.env.get("front_matter", {}))
        front_matter = add_inferred_schema(front_matter, filepath)

        top_level_type = None
    return front_matter, top_level_type

def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict[str, Any], str]:
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
        raise Exception(f"Expected html to be a string but got: {top_level_type(html)}")

    # Post-process HTML
    html = remove_lazy_loading_from_first_image(html)

    front_matter, top_level_type = resolve_front_matter(state, filepath)
    return html, front_matter, top_level_type


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
