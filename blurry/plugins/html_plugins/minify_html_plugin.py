import re

import htmlmin
from selectolax.parser import HTMLParser

from blurry.types import TemplateContext


def minify_css(css: str) -> str:
    minified_css = css.strip()
    characters_around_which_to_remove_whitespace = ["}", "{", ":", ";", ","]
    for character in characters_around_which_to_remove_whitespace:
        minified_css = re.sub(
            rf"\s*{character}\s*", character, minified_css, flags=re.M
        )

    return minified_css


def minify_style_tags(html: str) -> str:
    parser = HTMLParser(html, use_meta_tags=False)
    style_tags = parser.css("style")
    for style_tag in style_tags:
        css = style_tag.text()
        minified_css = minify_css(css)
        minified_style_tag = HTMLParser(
            f"<style>{minified_css}</style>"
        ).head.child  # type: ignore
        style_tag.replace_with(minified_style_tag)  # type: ignore

    return parser.html or html


def minify_html(html: str, _: TemplateContext, release: bool) -> str:
    if release:
        # Minify HTML and CSS
        html = htmlmin.minify(html, remove_empty_space=True)
        html = minify_style_tags(html)
    return html
