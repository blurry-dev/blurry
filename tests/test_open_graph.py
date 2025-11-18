import pytest

from blurry.open_graph import open_graph_meta_tags
from blurry.open_graph import open_graph_type_from_schema_type
from blurry.types import SchemaType


@pytest.mark.parametrize(
    "schema_type, open_graph_type",
    [
        (SchemaType.BLOG_POSTING, "article"),
        (SchemaType.NEWS_ARTICLE, "article"),
        ("banana", "website"),
    ],
)
def test_open_graph_type_from_schema_type(schema_type, open_graph_type):
    assert open_graph_type_from_schema_type(schema_type) == open_graph_type


product_schema_data = {
    "@type": "BlogPosting",
    "headline": "My Cool Post",
    "url": "/blog/article-one/",
    "image": "/hey.png",
}
blog_posting_meta_tag_content = """
<meta property="og:type" content="article">
<meta property="og:title" content="My Cool Post">
<meta property="og:url" content="/blog/article-one/">
<meta property="og:image" content="/hey.png">
""".strip()

product_schema_data = {
    "@type": "Product",
    "name": "My Product",
    "url": "/product/",
    "image": "/product.png",
}
blog_posting_meta_tag_content = """
<meta property="og:type" content="website">
<meta property="og:title" content="My Product">
<meta property="og:url" content="/product/">
<meta property="og:image" content="/product.png">
""".strip()


@pytest.mark.parametrize(
    "schema_data, tag_content",
    [
        (product_schema_data, blog_posting_meta_tag_content),
    ],
)
def test_open_graph_meta_tags(schema_data, tag_content):
    assert open_graph_meta_tags(schema_data) == tag_content
