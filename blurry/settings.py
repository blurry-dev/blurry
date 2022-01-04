from os import environ
from os import getenv
from typing import Any

import toml

from blurry.constants import ENV_VAR_PREFIX
from blurry.constants import IMAGE_WIDTHS

SETTINGS: dict[str, Any] = {
    "DEV_HOST": getenv(f"{ENV_VAR_PREFIX}DEV_HOST", "127.0.0.1"),
    "DEV_PORT": getenv(f"{ENV_VAR_PREFIX}DEV_PORT", 8000),
    "DOMAIN": getenv(f"{ENV_VAR_PREFIX}DOMAIN", "example.com"),
    "MAXIMUM_IMAGE_WIDTH": getenv(
        f"{ENV_VAR_PREFIX}_MAXIMUM_IMAGE_WIDTH", IMAGE_WIDTHS[-1]
    ),
}

try:
    blurry_config = toml.load(open("blurry.toml"))
    SETTINGS.update(blurry_config["blurry"])
except FileNotFoundError:
    pass


for key, value in environ.items():
    if not key.startswith(ENV_VAR_PREFIX):
        continue
    setting_name_start_index = len(ENV_VAR_PREFIX) - 1
    settings_key = key[setting_name_start_index:]
    SETTINGS[settings_key] = value
