from blurry.markdown.python_code_plugin import render_python_code


def test_render_python_code():
    language = "python"
    path = "blurry.types.MarkdownFileData"

    fenced_code_block = render_python_code(None, language, path)
    assert "body: str" in fenced_code_block
    assert "SchemaType" not in fenced_code_block
