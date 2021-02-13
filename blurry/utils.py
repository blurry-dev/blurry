from pathlib import Path

from blurry.constants import BUILD_DIR


def convert_content_path_to_directory_in_build(path: Path) -> Path:
    if str(path).endswith("index.md"):
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


def write_index_file_creating_path(directory_path: Path, content: str):
    directory_path.mkdir(parents=True, exist_ok=True)
    filepath = directory_path.joinpath("index.html")
    filepath.write_text(content)
