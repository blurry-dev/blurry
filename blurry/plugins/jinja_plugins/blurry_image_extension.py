import mimetypes
from urllib.parse import urlparse

from jinja2_simple_tags import StandaloneTag
from rich.console import Console
from PIL import Image

from blurry.images import add_image_width_to_path
from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.utils import build_path_to_url

warning_console = Console(stderr=True, style="bold yellow")


class BlurryImage(StandaloneTag):
    safe_output = True
    tags = {"blurry_image"}

    def render(self, *args, **kwargs):
        if len(args) == 2:
            (image_url, width) = args
        else:
            image_url = args[0]
            width = None

        image_relative_pathname = "." + urlparse(image_url).path
        image_content_path = get_content_directory() / image_relative_pathname
        image_path = get_build_directory() / image_relative_pathname

        try:
            with Image.open(image_content_path) as image:
                image_width, image_height = image.size
                image_mimetype = image.get_format_mimetype()
        except Exception:
            warning_console.print(f"Could not find image: {image_content_path}")
            return ""

        attributes = {
            "width": str(image_width),
            "height": str(image_height),
        }
        for attribute_key in kwargs:
            if attribute_key in ["width", "height"]:
                warning_console.print(
                    f"blurry_image: Received {attribute_key} in template {self.template} but this attribute is dynamic. Skipping."
                )
                continue
            attribute_value = kwargs.get(attribute_key)
            if attribute_value is not None:
                attributes[attribute_key] = attribute_value

        if width:
            image_path = add_image_width_to_path(image_path, width)

        if image_mimetype in [
            mimetypes.types_map[".jpg"],
            mimetypes.types_map[".png"],
        ]:
            image_path = image_path.with_suffix(".avif")

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

        return f"<img {attributes_str}>"
