from pathlib import Path

from selectolax.parser import HTMLParser

from blurry.settings import get_build_directory
from blurry.settings import get_content_directory
from blurry.settings import SETTINGS
from blurry.types import DirectoryFileData


def get_domain_with_scheme():
    if SETTINGS.get("RUNSERVER"):
        host = SETTINGS["DEV_HOST"]
        port = SETTINGS["DEV_PORT"]
        return f"http://{host}:{port}"
    domain = SETTINGS["DOMAIN"]
    protocol = "http" if SETTINGS.get("USE_HTTP") else "https"
    return f"{protocol}://{domain}"


def convert_content_path_to_directory_in_build(path: Path) -> Path:
    BUILD_DIR = get_build_directory()
    if path.name == "index.md":
        path = path.parent
    else:
        path = path.with_suffix("")
    return BUILD_DIR.joinpath(path)


def convert_relative_path_in_markdown_file_to_pathname(
    content_directory: Path, filepath: Path, relative_path: str
) -> str:
    directory = filepath.parent
    pathname_start = directory.relative_to(content_directory)

    while relative_path.startswith(prefix := "../"):
        pathname_start = pathname_start.parent
        relative_path = relative_path[len(prefix) :]
    if relative_path.startswith(prefix := "./"):
        relative_path = relative_path[len(prefix) :]
    if relative_path.endswith("index.md"):
        relative_path = relative_path.replace("index.md", "")
    elif relative_path.endswith(".md"):
        relative_path = relative_path.replace(".md", "") + "/"

    pathname_prefix = str(pathname_start).removeprefix(".")

    pathname = f"{pathname_prefix}/{relative_path}"

    if not pathname.startswith("/"):
        pathname = f"/{pathname}"

    return pathname


def resolve_relative_path_in_markdown(relative_path: str, markdown_file: Path) -> Path:
    """Converts a relative path in Markdown to an absolute path."""
    parent = markdown_file.parent
    path = parent / Path(relative_path)
    return path.resolve()


def path_to_url_pathname(path: Path) -> str:
    CONTENT_DIR = get_content_directory()
    url_pathname = "/" + str(path.relative_to(CONTENT_DIR))
    return url_pathname


def write_index_file_creating_path(directory_path: Path, content: str):
    directory_path.mkdir(parents=True, exist_ok=True)
    filepath = directory_path.joinpath("index.html")
    filepath.write_text(content)


def content_path_to_url_pathname(path: Path) -> str:
    BUILD_DIR = get_build_directory()
    if path.suffix == ".md":
        build_directory = convert_content_path_to_directory_in_build(path)
        relative_directory = build_directory.relative_to(BUILD_DIR)
        # Handle root page
        if str(relative_directory) == ".":
            return "/"
        return f"/{relative_directory}/"

    return path_to_url_pathname(path)


def content_path_to_url(path: Path) -> str:
    domain_with_scheme = get_domain_with_scheme()
    pathname = content_path_to_url_pathname(path)
    return f"{domain_with_scheme}{pathname}"


def build_path_to_url(path: Path) -> str:
    BUILD_DIR = get_build_directory()
    pathname = "/" + str(path.relative_to(BUILD_DIR))
    return f"{get_domain_with_scheme()}{pathname}"


def sort_directory_file_data_by_date(
    directory_file_data: DirectoryFileData,
) -> DirectoryFileData:
    for path, file_data in directory_file_data.items():
        file_data.sort(
            key=lambda page: str(page.front_matter.get("datePublished", ""))
            or str(page.front_matter.get("dateCreated", ""))
            or "0000-00-00",
            reverse=True,
        )
        directory_file_data[path] = file_data

    return directory_file_data


def format_schema_data(schema_data: dict) -> dict:
    formatted_schema_data = {"@context": "https://schema.org"}
    formatted_schema_data.update(schema_data)
    return formatted_schema_data


def remove_lazy_loading_from_first_image(html: str) -> str:
    parser = HTMLParser(html, use_meta_tags=False)
    if not parser.body or not parser.body.html:
        raise Exception("Could not parse HTML")
    first_img_tag = parser.css_first("img")
    if not first_img_tag:
        return html
    updated_tag = first_img_tag
    try:
        del updated_tag.attrs["loading"]  # type: ignore
        first_img_tag.replace_with(HTMLParser(updated_tag.html).body.child)  # type: ignore
    except KeyError:
        pass
    return parser.body.html
