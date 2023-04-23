from typing import Any
from typing import Literal

from blurry.types import SchemaType


META_TAG_TEMPLATE = '<meta property="og:{property}" content="{content}" />'

OpenGraphType = Literal["article", "book", "profile", "website"]


schema_type_to_open_graph_type: dict[SchemaType, OpenGraphType] = {
    SchemaType.ARTICLE: "article",
    SchemaType.BLOG_POSTING: "article",
    SchemaType.NEWS_ARTICLE: "article",
    SchemaType.TECH_ARTICLE: "article",
    SchemaType.BOOK: "book",
    SchemaType.AUDIOBOOK: "book",
    SchemaType.LOCAL_BUSINESS: "profile",
    SchemaType.NEWS_MEDIA_ORGANIZATION: "profile",
    SchemaType.ORGANIZATION: "profile",
    SchemaType.PERSON: "profile",
}


def open_graph_type_from_schema_type(schema_type_str: str) -> OpenGraphType:
    try:
        return schema_type_to_open_graph_type[SchemaType(schema_type_str)]
    except ValueError:
        return "website"


def open_graph_meta_tags(schema_data: dict[str, Any]) -> str:
    open_graph_properties = {}
    if type := schema_data.get("@type"):
        open_graph_properties["type"] = open_graph_type_from_schema_type(type)
    if headline := schema_data.get("headline"):
        open_graph_properties["title"] = headline
    if url := schema_data.get("url"):
        open_graph_properties["url"] = url
    if abstract := schema_data.get("abstract"):
        open_graph_properties["description"] = abstract
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
