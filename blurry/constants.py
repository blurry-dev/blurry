from pathlib import Path

ENV_VAR_PREFIX = "BLURRY_"

CURR_DIR = Path.cwd()
BUILD_DIR = CURR_DIR / "build"
CONTENT_DIR = CURR_DIR / "content"
TEMPLATE_DIR = CURR_DIR / "templates"

# Sizes adapted from: https://link.medium.com/UqzDeLKwyeb
IMAGE_WIDTHS = [1920, 1600, 1366, 1024, 768, 640, 360]
