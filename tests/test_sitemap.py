from datetime import date
from pathlib import Path

from blurry.sitemap import generate_sitemap_for_file_data_list
from blurry.types import MarkdownFileData

blog_path = Path("blog")
directory_file_data = [
    MarkdownFileData(
        front_matter=dict(datePublished=date(2021, 1, 1), url="/blog/a-post-1/"),
        body="",
        path=blog_path / "a-post-1",
    ),
    MarkdownFileData(
        front_matter=dict(datePublished=date(2021, 3, 1), url="/blog/b-post-3/"),
        body="",
        path=blog_path / "b-post-3",
    ),
    MarkdownFileData(
        front_matter=dict(dateCreated=date(2021, 2, 1), url="/blog/c-post-2/"),
        body="",
        path=blog_path / "c-post-2",
    ),
    MarkdownFileData(
        front_matter=dict(
            dateCreated=date(2022, 1, 10),
            dateModified=date(2022, 1, 13),
            url="/blog/c-post-4/",
        ),
        body="",
        path=blog_path / "c-post-4",
    ),
]


def test_generate_sitemap_for_file_data_list():
    sitemap_content = generate_sitemap_for_file_data_list(
        file_data_list=directory_file_data
    )
    assert sitemap_content.startswith('<?xml version="1.0" encoding="UTF-8"?>')
    assert sitemap_content.endswith("</urlset>")
    assert (
        "<url><loc>/blog/c-post-4/</loc><lastmod>2022-01-13</lastmod></url>"
        in sitemap_content
    )
