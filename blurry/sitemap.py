from pathlib import Path

import dpath

from blurry.settings import get_build_directory
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
""".strip()
URL_TEMPLATE = "    <url><loc>{url}</loc>{lastmod_tag}</url>"


def generate_sitemap_for_file_data_list(file_data_list: list[MarkdownFileData]) -> str:
    sitemap_url_data = []
    for file_data in file_data_list:
        lastmod = (
            dpath.values(file_data.front_matter, "**/dateModified")
            or dpath.values(file_data.front_matter, "**/datePublished")
            or dpath.values(file_data.front_matter, "**/dateCreated")
        )
        lastmod_tag = f"<lastmod>{lastmod[0]}</lastmod>" if len(lastmod) else ""
        url = file_data.front_matter.get("url")
        sitemap_url_data.append({"lastmod_tag": lastmod_tag, "url": url})

    sitemap_url_content = "\n".join(
        URL_TEMPLATE.format(url=data["url"], lastmod_tag=data["lastmod_tag"])
        for data in sitemap_url_data
    )
    return SITEMAP_TEMPLATE.format(urls=sitemap_url_content)


async def write_sitemap_file(
    file_data_by_directory: dict[Path, list[MarkdownFileData]]
):
    BUILD_DIR = get_build_directory()
    file_data = []
    for file_data_list in file_data_by_directory.values():
        file_data.extend(file_data_list)

    sitemap = generate_sitemap_for_file_data_list(file_data)
    sitemap_path = BUILD_DIR / "sitemap.xml"
    sitemap_path.write_text(sitemap)
