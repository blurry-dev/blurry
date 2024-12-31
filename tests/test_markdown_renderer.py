from blurry.markdown import markdown

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


def test_renderer_headings():
    html, _ = markdown.parse(MARKDOWN_WITH_HEADINGS)
    assert '<h1 id="home">Home</h1>' in html
    assert '<h2 id="section-1">Section 1</h2>' in html
    assert '<h4 id="sub-subsection-121">Sub-subsection 1.2.1</h4>' in html
