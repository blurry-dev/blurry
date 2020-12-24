from typing import Any

import mistune
from docdata.yamldata import get_data


def parse_front_matter(md, s, state):
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md):
    md.before_parse_hooks.append(parse_front_matter)


renderer = mistune.HTMLRenderer(escape=False)
markdown = mistune.Markdown(
    renderer, plugins=[plugin_front_matter]
)


def convert_markdown_file_to_html(filename: str) -> tuple[str, dict]:
    state: dict[str, Any] = {}
    html = markdown.read(filename, state)
    meta: dict[str, Any] = state.get("front_matter", {})
    return html, meta


if __name__ == "__main__":
    import sys
    html, meta = convert_markdown_file_to_html(sys.argv[1])
    print(meta)
