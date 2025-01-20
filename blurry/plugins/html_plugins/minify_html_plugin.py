import minify_html as minify_html_rs

from blurry.types import TemplateContext


def minify_html(html: str, _: TemplateContext, release: bool) -> str:
    if release:
        # Minify HTML and CSS
        html = minify_html_rs.minify(  # pyright: ignore
            html,
            do_not_minify_doctype=True,
            keep_html_and_head_opening_tags=True,
            minify_css=True,
            minify_js=True,
        )
    return html
