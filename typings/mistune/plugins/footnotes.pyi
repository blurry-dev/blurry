"""
This type stub file was generated by pyright.
"""

__all__ = ['plugin_footnotes']
INLINE_FOOTNOTE_PATTERN = ...
DEF_FOOTNOTE = ...
def parse_inline_footnote(inline, m, state): # -> tuple[Literal['text'], Unknown] | tuple[Literal['footnote_ref'], str, Unknown]:
    ...

def parse_def_footnote(block, m, state): # -> None:
    ...

def parse_footnote_item(block, k, i, state): # -> dict[str, Unknown]:
    ...

def md_footnotes_hook(md, result, state):
    ...

def render_ast_footnote_ref(key, index): # -> dict[str, Unknown]:
    ...

def render_ast_footnote_item(children, key, index): # -> dict[str, Unknown]:
    ...

def render_html_footnote_ref(key, index): # -> str:
    ...

def render_html_footnotes(text):
    ...

def render_html_footnote_item(text, key, index):
    ...

def plugin_footnotes(md): # -> None:
    ...

