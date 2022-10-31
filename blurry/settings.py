from os import environ
from typing import TypedDict

import toml

from blurry.constants import CURR_DIR
from blurry.constants import ENV_VAR_PREFIX


class Settings(TypedDict):
    BUILD_DIRECTORY_NAME: str
    DEV_HOST: str
    DEV_PORT: int
    DOMAIN: str
    IMAGE_WIDTHS: list[int]
    MAXIMUM_IMAGE_WIDTH: int
    THUMBNAIL_WIDTH: int
    USE_HTTP: bool
    RUNSERVER: bool


SETTINGS: Settings = {
    "BUILD_DIRECTORY_NAME": "build",
    "DEV_HOST": "127.0.0.1",
    "DEV_PORT": 8000,
    "DOMAIN": "example.com",
    # Sizes adapted from: https://link.medium.com/UqzDeLKwyeb
    "IMAGE_WIDTHS": [360, 640, 768, 1024, 1366, 1600, 1920],
    "MAXIMUM_IMAGE_WIDTH": 1920,
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


def get_build_directory():
    return CURR_DIR / SETTINGS["BUILD_DIRECTORY_NAME"]
