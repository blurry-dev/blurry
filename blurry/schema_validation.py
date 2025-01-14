import importlib
from collections.abc import MutableMapping
from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import ValidationError
from rich.console import Console

from blurry.settings import SETTINGS


Boolean = Literal["True"] | Literal["False"]


class Thing(BaseModel):
    additionalType: str | None = None
    alternateName: str | None = None
    description: str | None = None
    image: "ImageObject | None" = None
    name: str | None = None


class Person(Thing):
    type_: str = Field(default="Person", alias="@type", frozen=True)
    additionalName: str | None = None
    affiliation: "Organization | None" = None
    email: str | None = None
    familyName: str | None = None
    givenName: str | None = None
    honorificPrefix: str | None = None
    honorificSuffix: str | None = None
    telephone: str | None = None
    worksFor: "Organization | None" = None


class Organization(Thing):
    type_: str = Field(default="Organization", alias="@type", frozen=True)


class CreativeWork(Thing):
    type_: str = Field(default="CreativeWork", alias="@type", frozen=True)
    abstract: str | None = None
    author: Person | Organization | None = None
    creator: Person | Organization | None = None
    dateCreated: datetime | None = None
    dateModified: datetime | None = None
    datePublished: datetime | None = None
    headline: str | None = None


class MediaObject(CreativeWork):
    type_: str = Field(default="MediaObject", alias="@type", frozen=True)
    associatedArticle: "NewsArticle | None" = None
    bitrate: str | None = None
    contentSize: str | None = None
    contentUrl: str | None = None
    url: str | None = None
    embedUrl: str | None = None


class ImageObject(MediaObject):
    type_: str = Field(default="ImageObject", alias="@type", frozen=True)
    caption: MediaObject | str | None = None
    embeddedTextCaption: str | None = None
    # exifData: PropertyValue | Text | None
    representativeOfPage: Boolean | None = None


class WebSite(CreativeWork):
    type_: str = Field(default="WebSite", alias="@type", frozen=True)
    issn: str | None = None


class WebPage(CreativeWork):
    type_: str = Field(default="WebPage", alias="@type", frozen=True)
    # breadcrumb: BreadcrumbList | Text | None
    lastReviewed: datetime | None = None
    # mainContentOfPage: WebPageElement | None
    primaryImageOfPage: ImageObject | None = None
    relatedLink: str | None = None
    reviewedBy: Organization | Person | None = None
    significantLink: str | None = None
    # speakable: SpeakableSpecification | None
    # specialty: Specialty | None


class Article(CreativeWork):
    type_: str = Field(default="Article", alias="@type", frozen=True)
    author: Person | Organization  # pyright: ignore to narrow the type
    datePublished: datetime  # pyright: ignore to narrow the type
    headline: str  # pyright: ignore to narrow the type
    image: ImageObject | str | list[ImageObject | str]  # pyright: ignore to permit Google's recommendation


class NewsArticle(Article):
    type_: str = Field(default="NewsArticle", alias="@type", frozen=True)
    dateline: str | None = None
    printColumn: str | None = None
    printEdition: str | None = None
    printPage: str | None = None
    printSection: str | None = None


class SocialMediaPosting(Article):
    type_: str = Field(default="SocialMediaPosting", alias="@type", frozen=True)
    sharedContent: CreativeWork | None = None


class BlogPosting(SocialMediaPosting):
    type_: str = Field(default="BlogPosting", alias="@type", frozen=True)


# class Review(BaseModel):
#     author: Person | Organization
#     itemReviewed: (
#         Book
#         | Course
#         | CreativeWorkSeason
#         | CreativeWorkSeries
#         | Episode
#         | Event
#         | Game
#         | HowTo
#         | LocalBusiness
#         | MediaObject
#         | Movie
#         | MusicPlaylist
#         | MusicRecording
#         | Organization
#         | Product
#         | Recipe
#         | SoftwareApplication
#     )


def validate_front_matter_as_schema(
    path: Path, schema_variables: MutableMapping, console: Console
):
    """
    Validates schema data using partial Schema.org types based on Google's support for them:
    https://developers.google.com/search/docs/appearance/structured-data/search-gallery
    """
    schematype = schema_variables["@type"]

    if mapped_schematype_ := SETTINGS["TEMPLATE_SCHEMA_TYPES"].get(schematype):
        schematype = mapped_schematype_

    # Get the schema model class from this module
    try:
        module = importlib.import_module("blurry.schema_validation")
    except ModuleNotFoundError:
        console.print(f"{path}: Could not import module.")
        return

    # Validate model and print errors
    try:
        SchemaModel = getattr(module, schematype)
        SchemaModel(**schema_variables)
    except AttributeError:
        console.print(f"{path}: no validation rules available for {schematype}")
    except ValidationError as err:
        for error in err.errors():
            msg = error["msg"]
            loc = error["loc"]
            if len(loc) == 1:
                loc = loc[0]
            console.print(f"{path}: {schematype} schema validation error: {msg}: {loc}")
