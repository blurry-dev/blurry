import re
import unicodedata
from urllib.parse import urlparse

from selectolax.lexbor import LexborHTMLParser


def url_path(url: str) -> str:
    url_instance = urlparse(url)
    return url_instance.path


def slugify(value):
    """
    Convert spaces to hyphens.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Also strip leading and trailing whitespace.
    Adapted from: https://github.com/django/django/blob/92053acbb9160862c3e743a99ed8ccff8d4f8fd6/django/utils/text.py
    """
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"[^\w\s-]", "", value, flags=re.U).strip().lower()
    return re.sub(r"[-\s]+", "-", value, flags=re.U)


def headings(html: str, max_level: int = 2):
    tree = LexborHTMLParser(html)
    heading_list: list = []

    for node in tree.css("body *"):
        if node.tag in {"h2", "h3", "h4", "h5", "h6"}:
            level = int(node.tag[-1])
            if level > max_level:
                continue
            text = node.text()
            heading_list.append(
                {
                    "level": level,
                    "text": text,
                    "id": slugify(text),
                }
            )

    return heading_list
