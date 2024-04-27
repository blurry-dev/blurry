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


schema_data = {"@type": "BlogPosting", "url": "/blog/article-one/", "image": "/hey.png"}
meta_tag_content = """
<meta property="og:type" content="article">
<meta property="og:url" content="/blog/article-one/">
<meta property="og:image" content="/hey.png">
""".strip()


def test_open_graph_meta_tags():
    assert open_graph_meta_tags(schema_data) == meta_tag_content
