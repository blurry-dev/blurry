from urllib.parse import urlparse


def url_path(url: str) -> str:
    url_instance = urlparse(url)
    return url_instance.path
