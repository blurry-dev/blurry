import inspect
import re
from operator import attrgetter

from mistune import Markdown

__all__ = ["python_code", "python_code_in_list"]

PYTHON_CODE_PATTERN = r"[\s]*@(?P<language>[a-z]+)<(?P<path>.+)>"


def parse_python_code(block, match: re.Match, state):
    language = match.group("language")
    path = match.group("path")
    state.append_token(
        {
            "type": "python_code",
            "attrs": {"language": language, "path": path},
        }
    )
    return match.end() + 1


def render_python_code(_, language: str, path: str):
    package_name, reference_path = path.split(".", 1)
    package = __import__(package_name)
    reference = attrgetter(reference_path)(package)
    reference_source = inspect.getsource(reference)
    return f'<pre><code class="language-{language}">{reference_source}</code></pre>'


def python_code(md: Markdown):
    """A mistune plugin to insert Python code."""
    md.block.register(
        "python_code", PYTHON_CODE_PATTERN, parse_python_code, before="list"
    )
    if md.renderer and md.renderer.NAME == "html":
        md.renderer.register("python_code", render_python_code)


def python_code_in_list(md: Markdown):
    """Enable Python code plugin in list."""
    md.block.insert_rule(md.block.list_rules, "python_code", before="list")
