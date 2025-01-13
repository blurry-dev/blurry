from pathlib import Path
from unittest.mock import MagicMock

from rich.console import Console

from blurry.markdown.front_matter import get_data
from blurry.schema_validation import validate_front_matter_as_schema

MARKDOWN_WITH_VALID_TOML_FRONT_MATTER = """
+++
"@type" = "WebPage"
name = "Introduction"
abstract = "A Python-powered static site generator with a focus on page speed and SEO."
datePublished = 2023-04-09
+++

# Blurry: A Python-powered static site generator
""".strip()


def test_validate_front_matter_as_schema_with_valid_front_matter():
    _, front_matter = get_data(MARKDOWN_WITH_VALID_TOML_FRONT_MATTER)
    path = Path("pages/intro.md")
    test_console = Console()
    test_console.print = MagicMock()
    validate_front_matter_as_schema(path, front_matter, test_console)
    assert not test_console.print.called


MARKDOWN_WITH_EXTRA_VALUE_IN_TOML_FRONT_MATTER = """
+++
"@type" = "WebPage"
name = "Introduction"
abstract = "A Python-powered static site generator with a focus on page speed and SEO."
datePublished = 2023-04-09
extra_value = true
+++

# Blurry: A Python-powered static site generator
""".strip()


def test_validate_front_matter_as_schema_with_extra_value():
    _, front_matter_with_extra_value = get_data(
        MARKDOWN_WITH_EXTRA_VALUE_IN_TOML_FRONT_MATTER
    )
    path = Path("pages/intro.md")
    test_console = Console()
    test_console.print = MagicMock()
    validate_front_matter_as_schema(path, front_matter_with_extra_value, test_console)
    test_console.print.assert_called_with(
        "pages/intro.md: WebPage schema validation error: extra fields not permitted: ('extra_value',)"
    )
