from pathlib import Path
from typing import Any

from blurry.constants import BUILD_DIR
from blurry.markdown import markdown


def convert_content_path_to_build_directory(path: Path) -> Path:
    if str(path).endswith("index.md"):
        path = path.parent
    else:
        path = path.with_suffix("")
    return BUILD_DIR.joinpath(path)


def write_index_file_creating_path(directory_path: Path, content: str):
    directory_path.mkdir(parents=True, exist_ok=True)
    filepath = directory_path.joinpath("index.html")
    filepath.write_text(content)


def convert_markdown_file_to_html(filepath: Path) -> tuple[str, dict]:
    state: dict[str, Any] = {}
    html = markdown.read(str(filepath), state)
    front_matter: dict[str, Any] = state.get("front_matter", {})
    return html, front_matter
