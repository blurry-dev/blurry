from datetime import date
from pathlib import Path

import pytest

from blurry.constants import BUILD_DIR
from blurry.types import MarkdownFileData
from blurry.utils import convert_content_path_to_directory_in_build
from blurry.utils import convert_relative_path_in_markdown_to_relative_build_path
from blurry.utils import sort_directory_file_data_by_date


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


def test_sort_directory_file_data_by_date():
    blog_path = Path("blog")
    directory_file_data = {
        blog_path: [
            MarkdownFileData(
                front_matter=dict(datePublished=date(2021, 1, 1)),
                body="",
                path=Path("a-post-1"),
            ),
            MarkdownFileData(
                front_matter=dict(datePublished=date(2021, 3, 1)),
                body="",
                path=Path("b-post-3"),
            ),
            MarkdownFileData(
                front_matter=dict(dateCreated=date(2021, 2, 1)),
                body="",
                path=Path("c-post-2"),
            ),
            MarkdownFileData(
                front_matter=dict(),
                body="",
                path=Path("c-post-4"),
            ),
        ]
    }

    sorted_directory_file_data = sort_directory_file_data_by_date(directory_file_data)
    file_data = sorted_directory_file_data[blog_path]
    assert "post-3" in str(file_data[0].path)
    assert "post-2" in str(file_data[1].path)
    assert "post-1" in str(file_data[2].path)
    assert "post-4" in str(file_data[3].path)
