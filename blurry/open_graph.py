OPEN_GRAPH_TEMPLATE = """
<meta property="og:title" content="{title}" />
<meta property="og:type" content="{type}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{image}" />
<meta property="og:site_name" content="{site_name}" />
"""

META_TAG_TEMPLATE = '<meta property="og:{property}" content="{content}" />'

schema_type_to_open_graph_type = {
    "Article": "article",
    "BlogPosting": "article",
    "NewsArticle": "article",
    "TechArticle": "article",
    "Book": "book",
    "Audiobook": "book",
    "LocalBusiness": "profile",
    "NewsMediaOrganization": "profile",
    "Organization": "profile",
    "Person": "profile",
}


def open_graph_type_from_schema_type(open_graph_type: str) -> str:
    try:
        return schema_type_to_open_graph_type[open_graph_type]
    except KeyError:
        return "website"


def open_graph_meta_tags(schema_data: dict[str, str]) -> str:
    open_graph_properties = {}
    if type := schema_data.get("@type"):
        open_graph_properties["type"] = open_graph_type_from_schema_type(type)
    if headline := schema_data.get("headline"):
        open_graph_properties["title"] = headline
    if url := schema_data.get("url"):
        open_graph_properties["url"] = url
    if image := schema_data.get("image"):
        open_graph_properties["image"] = image
    if audio := schema_data.get("audio"):
        open_graph_properties["audio"] = audio
    if organization := schema_data.get("sourceOrganization"):
        if site_name := organization.get("name"):
            open_graph_properties["site_name"] = site_name
    if video := schema_data.get("video"):
        open_graph_properties["video"] = video
    return "\n".join(
        META_TAG_TEMPLATE.format(property=property, content=content)
        for property, content in open_graph_properties.items()
    )
