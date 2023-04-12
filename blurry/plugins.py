import htmlmin
from importlib.metadata import entry_points

from blurry.types import TemplateContext
from blurry.utils import minify_style_tags

discovered_mistune_plugins = entry_points(group="blurry.mistune_plugins")
discovered_html_plugins = entry_points(group="blurry.html_plugins")


def minify_html(html: str, _: TemplateContext, release: bool) -> str:
    if release:
        # Minify HTML and CSS
        html = htmlmin.minify(html, remove_empty_space=True)
        html = minify_style_tags(html)
    return html
