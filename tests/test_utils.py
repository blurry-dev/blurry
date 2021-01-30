from pathlib import Path

import pytest

from blurry import convert_content_path_to_build_directory
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
    path_out = convert_content_path_to_build_directory(path)
    assert path_out == (BUILD_DIR / Path(expected_build_path))
