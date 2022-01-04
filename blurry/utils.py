import os
from pathlib import Path

from blurry.constants import BUILD_DIR
from blurry.constants import CONTENT_DIR
from blurry.constants import ENV_VAR_PREFIX
from blurry.settings import SETTINGS
from blurry.types import DirectoryFileData


def get_domain_with_scheme():
    if os.environ.get(f"{ENV_VAR_PREFIX}RUNSERVER"):
        host = SETTINGS["DEV_HOST"]
        port = SETTINGS["DEV_PORT"]
        return f"http://{host}:{port}"
    domain = SETTINGS["DOMAIN"]
    return f"https://{domain}"


def convert_content_path_to_directory_in_build(path: Path) -> Path:
    if path.name == "index.md":
        path = path.parent
    else:
        path = path.with_suffix("")
    return BUILD_DIR.joinpath(path)


def convert_relative_path_in_markdown_to_relative_build_path(relative_path: str) -> str:
    if relative_path.startswith("./"):
        relative_path = relative_path[2:]
    if relative_path.endswith("index.md"):
        relative_path = relative_path.replace("index.md", "")
    elif relative_path.endswith(".md"):
        relative_path = relative_path.replace(".md", "")
    return "../" + relative_path


def resolve_relative_path_in_markdown(relative_path: str, markdown_file: Path) -> Path:
    """Converts a relative path in Markdown to an absolute path."""
    parent = markdown_file.parent
    path = parent / Path(relative_path)
    return path.resolve()


def path_to_url_pathname(path: Path) -> str:
    url_pathname = "/" + str(path.relative_to(CONTENT_DIR))
    return url_pathname


def write_index_file_creating_path(directory_path: Path, content: str):
    directory_path.mkdir(parents=True, exist_ok=True)
    filepath = directory_path.joinpath("index.html")
    filepath.write_text(content)


def content_path_to_url(path: Path) -> str:
    build_directory = convert_content_path_to_directory_in_build(path)
    relative_directory = build_directory.relative_to(BUILD_DIR)
    return f"{get_domain_with_scheme()}/{relative_directory}/"


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


def set_runserver_env_var():
    os.environ[f"{ENV_VAR_PREFIX}RUNSERVER"] = "True"
