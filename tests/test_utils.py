from pathlib import Path, PurePath

import pytest

from blurry.utils import convert_content_path_to_directory_in_build
from blurry.utils import convert_relative_path_in_markdown_to_relative_build_path
from blurry.constants import BUILD_DIR


@pytest.mark.parametrize(
    "path_in, expected_build_path",
    [
        ("cool-post.md", "cool-post"),
        ("nested/post.md", "nested/post"),
        ("index.md", ""),
    ],
)
def test_convert_content_path_to_build_path(path_in, expected_build_path):
    path = Path(path_in)
    path_out = convert_content_path_to_directory_in_build(path)
    assert path_out == (BUILD_DIR / Path(expected_build_path))


@pytest.mark.parametrize(
    "path_in, expected_html_path",
    [
        ("./cool-post.md", "../cool-post"),
        ("../home.md", "../../home"),
        ("../index.md", "../../"),
        ("./image.png", "../image.png"),
    ],
)
def test_convert_content_path_to_html_path(path_in, expected_html_path):
    html_path = convert_relative_path_in_markdown_to_relative_build_path(path_in)
    assert html_path == expected_html_path