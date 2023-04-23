from blurry.plugins.html_plugins.minify_html_plugin import minify_css
from blurry.plugins.html_plugins.minify_html_plugin import minify_style_tags


def test_minify_css():
    css = """
body {
  color: pink;
}
document {
  background: blue;
}
pre,
code {
  font-family: monospace;
  font-size: 0.9rem;
}
""".strip()
    minified_css = minify_css(css)
    assert minified_css == (
        "body{color:pink;}document{background:blue;}"
        "pre,code{font-family:monospace;font-size:0.9rem;}"
    )


def test_minify_style_tags():
    html = """
<html>
<head>
  <style>
  body {
    color: pink;
  }
  </style>
</head>
<body>
  <style>
  document {
    background: blue;
  }
  </style>
</body>
</html>
""".strip()
    html_with_minified_style_tags = minify_style_tags(html)
    assert (
        html_with_minified_style_tags
        == """
<html><head>
  <style>body{color:pink;}</style>
</head>
<body>
  <style>document{background:blue;}</style>

</body></html>
""".strip()
    )
