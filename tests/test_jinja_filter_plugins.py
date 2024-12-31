import pytest

from blurry.plugins.jinja_plugins.filters import headings
from blurry.plugins.jinja_plugins.filters import slugify
from blurry.plugins.jinja_plugins.filters import url_path

html = """
<!DOCTYPE html>
<html lang="en">

<head>
    <title>Getting started: quick start | Blurry</title>
</head>

<body>
<main>
        
<h1>Blurry: A Python-powered static site generator</h1>
<h2>What is Blurry?</h2>
<p>Blurry is a static site generator with a terrible pun of a name: if you're generating static sight, you're making things Blurry.</p>
<p>Blurry brings the concept of schema-first development to static site generators.
Specifically, Blurry uses <a href="https://schema.org/" target="_blank" rel="noopener">Schema.org</a> schema type names as the names for its template files, and schema type properties as Markdown front matter to populate those templates.</p>
<h2>Goals</h2>
<h3>SEO performance</h3>
<p>Blurry supports <a href="https://schema.org/" target="_blank" rel="noopener">Schema.org</a> and <a href="https://ogp.me/" target="_blank" rel="noopener">Open Graph</a> with zero configuration.
This enables <a href="https://developers.google.com/search/docs/appearance/structured-data/search-gallery" target="_blank" rel="noopener">rich Google results</a> and <a href="https://www.opengraph.xyz/" target="_blank" rel="noopener">link previews</a> out-of-the-box.</p>
<h3>Page speed</h3>
<p>While using Blurry doesn't guarantee good page speed, it does solve a number of pain points that tend to slow down page loads.</p>
<p><a href="/content/images/" rel="noreferrer">Blurry's image handling</a> and HTML minification, for instance, can help get you a 100/100 <a href="https://pagespeed.web.dev/" target="_blank" rel="noopener">PageSpeed</a> score if the rest of your site is fast.</p>
<h3>Minimal configuration</h3>
<p>Blurry seeks to use sensible defaults so you can spend less time configuring and more time writing.
A viable Blurry configuration file (<a href="/../configuration/blurry.toml/" rel="noreferrer"><code>blurry.toml</code></a>) can be as simple as:</p>
<pre><code class="language-toml hljs language-ini"><span class="hljs-section">[blurry]</span>
<span class="hljs-attr">domain</span> = <span class="hljs-string">"johnfraney.ca"</span>
</code></pre>
<h3>Semantic HTML</h3>
<p>Where applicable, Blurry tries to use semantic HTML elements like <code>&lt;aside&gt;</code> over more generic elements like <code>&lt;div&gt;</code>.
Using semantic HTML elements also facilities classless CSS styling, which can be useful when styling some Markdown-generated HTML elements, and it can be <a href="https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML" target="_blank" rel="noopener">good for accessibility</a>, too.</p>
<h2>Non-goals</h2>
<h3>"Gotta go fast!"</h3>
<p>While Blurry aims to be performant, build performance is not its top priority.
It's written in Python, so it may not be able to compete on speed with other static site generators like <a href="https://gohugo.io/" target="_blank" rel="noopener">Hugo</a>.
Instead, it aims to be <em>fast enough</em> while taking advantage of the Python ecosystem.</p>
    </main>
</body>
</html>"""


def test_headings_filter_defaults():
    heading_list = headings(html)
    assert heading_list == [
        {"level": 2, "text": "What is Blurry?", "id": "what-is-blurry"},
        {"level": 2, "text": "Goals", "id": "goals"},
        {"level": 2, "text": "Non-goals", "id": "non-goals"},
    ]


def test_headings_filter_max_level():
    heading_list = headings(html, max_level=3)
    assert heading_list == [
        {"level": 2, "text": "What is Blurry?", "id": "what-is-blurry"},
        {"level": 2, "text": "Goals", "id": "goals"},
        {"level": 3, "text": "SEO performance", "id": "seo-performance"},
        {"level": 3, "text": "Page speed", "id": "page-speed"},
        {"level": 3, "text": "Minimal configuration", "id": "minimal-configuration"},
        {"level": 3, "text": "Semantic HTML", "id": "semantic-html"},
        {"level": 2, "text": "Non-goals", "id": "non-goals"},
        {"level": 3, "text": '"Gotta go fast!"', "id": "gotta-go-fast"},
    ]


@pytest.mark.parametrize(
    "title, slug",
    [
        ["Non-goals", "non-goals"],
        ['"Gotta go fast!"', "gotta-go-fast"],
        ["That's blasé", "thats-blasé"],
        ["Sub-subsection 1.2.1", "sub-subsection-121"],
    ],
)
def test_slugify(title, slug):
    assert slugify(title) == slug


def test_url_path():
    url = "http://127.0.0.1:8000/getting-started/quickstart/"
    assert url_path(url) == "/getting-started/quickstart/"
