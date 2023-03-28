from re import Match

from mistune import InlineParser
from mistune import InlineState
from mistune import Markdown

BLURRY_PATTERN = r"Blurry"
NAME = "blurry_name"


def parse_blurry_name(_: InlineParser, m: Match, state: InlineState):
    text = m.group(0)
    state.append_token({"type": NAME, "raw": text})
    return m.end()


def render_blurry_name(_, text: str):
    return f'<span class="blurry">{text}</span>'


def blur_blurry_name(md: Markdown):
    md.inline.register(NAME, BLURRY_PATTERN, parse_blurry_name, before="link")
    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register(NAME, render_blurry_name)
