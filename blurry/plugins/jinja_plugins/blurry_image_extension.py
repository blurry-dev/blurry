import mimetypes
from pathlib import Path
from urllib.parse import urlparse

from jinja2_simple_tags import StandaloneTag
from rich.console import Console
from wand.exceptions import BlobError
from wand.image import Image

from blurry.images import add_image_width_to_path
from blurry.settings import get_build_directory
from blurry.utils import build_path_to_url

warning_console = Console(stderr=True, style="bold yellow")


class BlurryImage(StandaloneTag):
    safe_output = True
    tags = {"blurry_image"}

    def render(self, *args, **kwargs):
        (image_url, width) = args
        image_content_path: str = "." + urlparse(image_url).path
        image_path = get_build_directory() / image_content_path

        try:
            with Image(filename=str(image_path)) as image:
                image_width = image.width
                image_height = image.height
                image_mimetype = image.mimetype
        except BlobError:
            warning_console.print(f"Could not find image: {image_path}")
            return ""

        attributes = {
            "width": image_width,
            "height": image_height,
        }
        for attribute_key in kwargs:
            if attribute_key in ["width", "height"]:
                warning_console.print(
                    f"blurry_image: Received {attribute_key} in template {self.template} but this attribute is dynamic. Skipping."
                )
                continue
            attributes[attribute_key] = kwargs.get(attribute_key)

        if width:
            image_path = add_image_width_to_path(image_path, width)

        if image_mimetype in [
            mimetypes.types_map[".jpg"],
            mimetypes.types_map[".png"],
        ]:
            image_path = Path(str(image_path).replace(image_path.suffix, ".avif"))

        if not image_path.exists():
            warning_console.print(
                f"blurry_image: Could not find {image_path}. Skipping."
            )
            return ""

        attributes["src"] = build_path_to_url(image_path)

        if "alt" not in attributes:
            warning_console.print(
                f"blurry_image: alt attribute missing for image in {self.template}. "
                "This can negatively affect accessibility. "
                "Use an empty alt tag if an image is only for show."
            )

        attributes_str = " ".join(
            f'{name}="{value}"' for name, value in attributes.items()
        )

        return f"<img {attributes_str}/>"
