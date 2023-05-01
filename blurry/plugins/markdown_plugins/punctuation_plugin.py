from re import Match

from mistune import InlineParser
from mistune import InlineState
from mistune import Markdown

EM_DASH_PATTERN = r"---"
EN_DASH_PATTERN = r"--"


def parse_em_dash(_: InlineParser, match: Match, state: InlineState):
    pos = match.end()
    state.append_token({"type": "text", "raw": "—"})
    return pos


def parse_en_dash(_: InlineParser, match: Match, state: InlineState):
    pos = match.end()
    state.append_token({"type": "text", "raw": "–"})
    return pos


def punctuation(md: Markdown):
    md.inline.register("punctuation_em_dash", EM_DASH_PATTERN, parse_em_dash)
    md.inline.register("punctuation_en_dash", EN_DASH_PATTERN, parse_en_dash)
