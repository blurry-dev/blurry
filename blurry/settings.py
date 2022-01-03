from typing import Any

import toml

from blurry.constants import IMAGE_WIDTHS

SETTINGS: dict[str, Any] = {
    "domain": "example.com",
    "maximum_image_width": IMAGE_WIDTHS[-1],
}

try:
    blurry_config = toml.load(open("blurry.toml"))
    SETTINGS.update(blurry_config["blurry"])
except FileNotFoundError:
    pass
