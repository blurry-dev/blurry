from os import environ
from typing import Any

import toml

from blurry.constants import ENV_VAR_PREFIX
from blurry.constants import IMAGE_WIDTHS

SETTINGS: dict[str, Any] = {
    "DEV_HOST": "127.0.0.1",
    "DEV_PORT": 8000,
    "DOMAIN": "example.com",
    "MAXIMUM_IMAGE_WIDTH": IMAGE_WIDTHS[0],
    "THUMBNAIL_WIDTH": 250,
    "USE_HTTP": False,
    "RUNSERVER": False,
}

try:
    blurry_config = toml.load(open("blurry.toml"))
    user_settings = blurry_config["blurry"]
    for setting, value in user_settings.items():
        SETTINGS[setting.upper()] = value
except FileNotFoundError:
    pass


for key, value in environ.items():
    if not key.startswith(ENV_VAR_PREFIX):
        continue
    setting_name_start_index = len(ENV_VAR_PREFIX) - 1
    settings_key = key[setting_name_start_index:]
    SETTINGS[settings_key] = value
