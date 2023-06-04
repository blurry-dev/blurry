from blurry.markdown.front_matter import get_data

MARKDOWN_WITH_BASIC_TOML_FRONT_MATTER = """
+++
"@type" = "WebPage"
name = "Introduction"
abstract = "A Python-powered static site generator with a focus on page speed and SEO."
datePublished = 2023-04-09
+++

# Blurry: A Python-powered static site generator

## What is Blurry?

Blurry is a static site generator with a terrible pun of a name...
""".strip()


def test_get_data():
    doc, data = get_data(MARKDOWN_WITH_BASIC_TOML_FRONT_MATTER)
    assert doc.startswith("# Blurry: ")
    assert len(data) == 4
    assert data.get("@type") == "WebPage"
