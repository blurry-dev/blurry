from os import environ
from typing import TypedDict

import toml

from blurry.constants import CURR_DIR
from blurry.constants import ENV_VAR_PREFIX
from blurry.constants import SETTINGS_FILENAME


class Settings(TypedDict):
    AVIF_COMPRESSION_QUALITY: int
    BUILD_DIRECTORY_NAME: str
    CONTENT_DIRECTORY_NAME: str
    MARKDOWN_FILE_JINJA_TEMPLATE_EXTENSION: str
    TEMPLATES_DIRECTORY_NAME: str
    TEMPLATE_SCHEMA_TYPES: dict[str, str]

    DEV_HOST: str
    DEV_PORT: int
    DOMAIN: str
    IMAGE_WIDTHS: list[int]
    MAXIMUM_IMAGE_WIDTH: int
    THUMBNAIL_WIDTH: int
    VIDEO_EXTENSIONS: list[str]
    USE_HTTP: bool
    RUNSERVER: bool
    FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX: str


SETTINGS: Settings = {
    "AVIF_COMPRESSION_QUALITY": 90,
    "BUILD_DIRECTORY_NAME": "dist",
    "CONTENT_DIRECTORY_NAME": "content",
    "TEMPLATES_DIRECTORY_NAME": "templates",
    "DEV_HOST": "127.0.0.1",
    "DEV_PORT": 8000,
    "DOMAIN": "example.com",
    # Sizes adapted from: https://link.medium.com/UqzDeLKwyeb
    "IMAGE_WIDTHS": [360, 640, 768, 1024, 1366, 1600, 1920],
    "MARKDOWN_FILE_JINJA_TEMPLATE_EXTENSION": ".html",
    "MAXIMUM_IMAGE_WIDTH": 1920,
    "THUMBNAIL_WIDTH": 250,
    "VIDEO_EXTENSIONS": ["mp4", "webm", "mkv"],
    "USE_HTTP": False,
    "RUNSERVER": False,
    "FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX": "~",
    "TEMPLATE_SCHEMA_TYPES": {},
}


def update_settings():
    try:
        blurry_config = toml.load(open(SETTINGS_FILENAME))
        user_settings = blurry_config["blurry"]
        for setting, value in user_settings.items():
            SETTINGS[setting.upper()] = value
    except FileNotFoundError:
        pass

    setting_name_start_index = len(ENV_VAR_PREFIX) - 1
    for key, value in environ.items():
        if not key.startswith(ENV_VAR_PREFIX):
            continue
        settings_key = key[setting_name_start_index:]
        SETTINGS[settings_key] = value


def get_build_directory():
    is_dev_build = environ.get(f"{ENV_VAR_PREFIX}BUILD_MODE") == "dev"
    if is_dev_build:
        return CURR_DIR / ".blurry" / SETTINGS["BUILD_DIRECTORY_NAME"]
    return CURR_DIR / SETTINGS["BUILD_DIRECTORY_NAME"]


def get_content_directory():
    return CURR_DIR / SETTINGS["CONTENT_DIRECTORY_NAME"]


def get_templates_directory():
    return CURR_DIR / SETTINGS["TEMPLATES_DIRECTORY_NAME"]
