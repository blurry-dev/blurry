"""
This type stub file was generated by pyright.
"""

from .base import Directive

"""
    TOC directive
    ~~~~~~~~~~~~~

    The TOC directive syntax looks like::

        .. toc:: Title
           :depth: 3

    "Title" and "depth" option can be empty. "depth" is an integer less
    than 6, which defines the max heading level writers want to include
    in TOC.
"""
class DirectiveToc(Directive):
    def __init__(self, depth=...) -> None:
        ...
    
    def parse(self, block, m, state): # -> dict[str, str] | dict[str, Unknown]:
        ...
    
    def reset_toc_state(self, md, s, state): # -> tuple[Unknown, Unknown]:
        ...
    
    def register_plugin(self, md): # -> None:
        ...
    
    def __call__(self, md): # -> None:
        ...
    


def record_toc_heading(text, level, state): # -> dict[str, Unknown]:
    ...

def md_toc_hook(md, tokens, state):
    ...

def render_ast_toc(items, title, depth): # -> dict[str, Unknown]:
    ...

def render_ast_theading(children, level, tid): # -> dict[str, Unknown]:
    ...

def render_html_toc(items, title, depth): # -> str:
    ...

def render_html_theading(text, level, tid):
    ...

def extract_toc_items(md, s): # -> list[tuple[Unknown, str, Unknown]]:
    """Extract TOC headings into list structure of::

        [
          ('toc_1', 'Introduction', 1),
          ('toc_2', 'Install', 2),
          ('toc_3', 'Upgrade', 2),
          ('toc_4', 'License', 1),
        ]

    :param md: Markdown Instance with TOC plugin.
    :param s: text string.
    """
    ...

def render_toc_ul(toc): # -> str:
    """Render a <ul> table of content HTML. The param "toc" should
    be formatted into this structure::

        [
          (toc_id, text, level),
        ]

    For example::

        [
          ('toc-intro', 'Introduction', 1),
          ('toc-install', 'Install', 2),
          ('toc-upgrade', 'Upgrade', 2),
          ('toc-license', 'License', 1),
        ]
    """
    ...

