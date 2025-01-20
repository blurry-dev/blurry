from blurry.plugins.markdown_plugins.python_code_plugin import render_python_code


def test_render_python_code_within_module():
    language = "python"
    path = "blurry.types.MarkdownFileData"

    fenced_code_block = render_python_code(None, language, path)
    assert "body: str" in fenced_code_block
    assert "SchemaType" not in fenced_code_block


def test_render_module_code():
    language = "python"
    path = "blurry.plugins.html_plugins.minify_html_plugin"

    code = render_python_code(None, language, path)
    assert "import minify_html as minify_html_rs" in code
    assert "return html" in code
