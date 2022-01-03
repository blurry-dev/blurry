from typing import Any

import toml

SETTINGS: dict[str, Any] = {
    "domain": "example.com",
}

try:
    blurry_config = toml.load(open("blurry.toml"))
    SETTINGS.update(blurry_config["blurry"])
except FileNotFoundError:
    pass
