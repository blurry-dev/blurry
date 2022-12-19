import re
from typing import Type

import mistune


CONTAINER_PATTERN = re.compile(
    r"( {0,3})(:{3,}|~{3,})([^`\n]*)\n" r"(?:|([\s\S]*?)\n)" r"(?: {0,3}\2[~:]* *\n+|$)"
)


def parse_container(inline: mistune.InlineParser, m: re.Match, state):
    kind = m.group(3).strip()
    spaces = m.group(1)
    content = m.group(4) or ""

    if spaces and content:
        _trim_pattern = re.compile("^" + spaces, re.M)
        content = _trim_pattern.sub("", content)

    children = inline.parse(state)
    token = {"type": "container", "children": children}
    if kind:
        token["params"] = (kind,)
    return token


def render_html_container(content: str, kind: str = "") -> str:
    return f'<aside role="note" class="{kind}">{content}</aside>'


def blurry_container(md: Type[mistune.Markdown]) -> None:
    md.block.register(
        "container", CONTAINER_PATTERN, parse_container, before="list"
    )

    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register("container", render_html_container)
