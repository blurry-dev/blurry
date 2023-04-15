import htmlmin

from blurry.types import TemplateContext
from blurry.utils import minify_style_tags


def minify_html(html: str, _: TemplateContext, release: bool) -> str:
    if release:
        # Minify HTML and CSS
        html = htmlmin.minify(html, remove_empty_space=True)
        html = minify_style_tags(html)
    return html
