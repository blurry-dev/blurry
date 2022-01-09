from pathlib import Path

from blurry.constants import BUILD_DIR
from blurry.types import MarkdownFileData

SITEMAP_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<urlset
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9
    http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"
    xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
>
{urls}
</urlset>
"""
URL_TEMPLATE = "    <url><loc>{url}</loc></url>"


def generate_sitemap_for_urls(urls: list[str]) -> str:
    sitemap_url_tags = "\n".join(URL_TEMPLATE.format(url=url) for url in urls)
    return SITEMAP_TEMPLATE.format(urls=sitemap_url_tags)


async def write_sitemap_file(
    file_data_by_directory: dict[Path, list[MarkdownFileData]]
):
    urls: list[str] = []
    for file_data_list in file_data_by_directory.values():
        for file_data in file_data_list:
            urls.append(file_data.front_matter["url"])

    sitemap = generate_sitemap_for_urls(urls)
    sitemap_path = BUILD_DIR / "sitemap.xml"
    sitemap_path.write_text(sitemap)
