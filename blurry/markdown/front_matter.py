import re
from pathlib import Path

from mistune import Markdown, BlockState
import toml

TOML_BLOCK_RE = re.compile(
    r"^\+{3}[ \t]*\n(.*?\n)(?:\.{3}|\+{3})[ \t]*\n", re.UNICODE | re.DOTALL
)


def get_data(doc: str) -> tuple[str, dict]:
    """
    Extract frontmatter from Markdown-style text.
    Code adapted from docdata.yamldata:
    https://github.com/waylan/docdata/blob/master/docdata/yamldata.py
    """
    data = {}
    toml_block_match = TOML_BLOCK_RE.match(doc)
    if toml_block_match:
        try:
            data = toml.loads(toml_block_match.group(1))

            if isinstance(data, dict):
                doc = doc[toml_block_match.end() :].lstrip("\n")  # noqa: E203
            else:
                data = {}
        except Exception:
            pass
    return doc, data


def parse_front_matter(_: Markdown, state: BlockState) -> tuple[str, BlockState]:
    filepath = state.env.get("__file__")
    if not isinstance(filepath, str):
        raise Exception(f"Count not find filepath {filepath}")
    file_contents = Path(filepath).read_text()
    markdown_text, front_matter = get_data(file_contents)
    state.env["front_matter"] = front_matter
    return markdown_text, state
