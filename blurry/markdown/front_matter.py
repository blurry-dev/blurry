from typing import Any

import mistune
from docdata.yamldata import get_data


def parse_front_matter(_, s: str, state: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def blurry_front_matter(md: mistune.Markdown) -> None:
    md.before_parse_hooks.append(parse_front_matter)
