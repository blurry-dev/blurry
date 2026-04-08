from unittest import mock

import pytest

from blurry.markdown import BlurryRenderer, get_markdown_instance

MARKDOWN_WITH_HEADINGS = """
# Home

This is the homepage with some sections.

## Section 1

### Subsection 1.1

It's a subsection.

### Subsection 1.2

It's another subsection.

#### Sub-subsection 1.2.1

Now we're nesting.

## Section 2

Look! A section!
"""

markdown = get_markdown_instance()


def test_renderer_headings():
    html, _ = markdown.parse(MARKDOWN_WITH_HEADINGS)
    assert '<h1 id="home">Home</h1>' in html
    assert '<h2 id="section-1">Section 1</h2>' in html
    assert '<h4 id="sub-subsection-121">Sub-subsection 1.2.1</h4>' in html



def test_relative_md_link_existing_file_no_warning(tmp_path, capsys):
    content_dir = tmp_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    source = content_dir / "index.md"
    source.touch()
    target = content_dir / "about.md"
    target.touch()

    r = BlurryRenderer(escape=False)
    r.filepath = source

    with mock.patch("blurry.markdown.get_content_directory", return_value=content_dir):
        r.link("About", "./about.md")

    captured = capsys.readouterr()
    assert "not found" not in captured.err


def test_relative_md_link_missing_file_warns(tmp_path, capsys):
    content_dir = tmp_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    source = content_dir / "index.md"
    source.touch()
    # intentionally NOT creating the target file

    r = BlurryRenderer(escape=False)
    r.filepath = source

    with mock.patch("blurry.markdown.get_content_directory", return_value=content_dir):
        r.link("Ghost", "./ghost.md")

    captured = capsys.readouterr()
    assert "ghost.md" in captured.err


def test_non_md_relative_link_no_warning(tmp_path, capsys):
    content_dir = tmp_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    source = content_dir / "index.md"
    source.touch()

    r = BlurryRenderer(escape=False)
    r.filepath = source

    with mock.patch("blurry.markdown.get_content_directory", return_value=content_dir):
        r.link("file", "./archive.zip")

    captured = capsys.readouterr()
    assert "not found" not in captured.err


def test_absolute_link_no_warning(tmp_path, capsys):
    content_dir = tmp_path / "content"
    content_dir.mkdir(parents=True, exist_ok=True)
    source = content_dir / "index.md"
    source.touch()

    r = BlurryRenderer(escape=False)
    r.filepath = source

    with mock.patch("blurry.markdown.get_content_directory", return_value=content_dir):
        r.link("Example", "https://example.com")

    captured = capsys.readouterr()
    assert "not found" not in captured.err
