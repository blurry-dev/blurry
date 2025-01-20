from blurry.plugins.html_plugins.minify_html_plugin import minify_html


def test_minify_html():
    html = """
<!DOCTYPE html>
<html
  lang="en"
>
<head>
    <title>Title</title>
    <style>
    body {
    color: pink;
    }
    </style>
</head>
<body>
    <h1>Hi!</h1>
</body>
</html>
""".strip()
    minified_html = minify_html(html, {}, release=True)
    assert (
        minified_html
        == """
<!doctype html><html lang=en><head><title>Title</title><style>body{color:pink}</style><body><h1>Hi!</h1>
""".strip()
    )
