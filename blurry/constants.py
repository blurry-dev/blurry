from pathlib import Path

ENV_VAR_PREFIX = "BLURRY_"

SETTINGS_FILENAME = "blurry.toml"

CURR_DIR = Path.cwd()

EFFICIENT_IMAGE_FORMATS = {"WEBP", "AVIF"}
EFFICIENT_IMAGE_SUFFIXES = {".webp", ".avif"}
