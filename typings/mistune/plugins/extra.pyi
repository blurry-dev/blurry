"""
This type stub file was generated by pyright.
"""

__all__ = ['plugin_url', 'plugin_strikethrough']
URL_LINK_PATTERN = ...
def parse_url_link(inline, m, state): # -> tuple[Literal['link'], str | Unknown]:
    ...

def plugin_url(md): # -> None:
    ...

STRIKETHROUGH_PATTERN = ...
def parse_strikethrough(inline, m, state): # -> tuple[Literal['strikethrough'], Unknown]:
    ...

def render_html_strikethrough(text):
    ...

def plugin_strikethrough(md): # -> None:
    ...

