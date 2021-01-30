import mistune
from docdata.yamldata import get_data


def parse_front_matter(_, s: str, state: dict) -> tuple[str, dict]:
    markdown_text, front_matter = get_data(s)
    state["front_matter"] = front_matter
    return markdown_text, state


def plugin_front_matter(md: mistune.Markdown) -> None:
    md.before_parse_hooks.append(parse_front_matter)


renderer = mistune.HTMLRenderer(escape=False)
markdown = mistune.Markdown(renderer, plugins=[plugin_front_matter])
