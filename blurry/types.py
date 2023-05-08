from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any
from typing import TypeGuard


@dataclass
class MarkdownFileData:
    body: str
    front_matter: dict[str, Any]
    path: Path


class SchemaType(Enum):
    ARTICLE = "Article"
    BLOG_POSTING = "BlogPosting"
    NEWS_ARTICLE = "NewsArticle"
    TECH_ARTICLE = "TechArticle"
    BOOK = "Book"
    AUDIOBOOK = "Audiobook"
    LOCAL_BUSINESS = "LocalBusiness"
    NEWS_MEDIA_ORGANIZATION = "NewsMediaOrganization"
    ORGANIZATION = "Organization"
    PERSON = "Person"


DirectoryFileData = dict[Path, list[MarkdownFileData]]

TemplateContext = dict[str, Any]


def is_str(value: Any) -> TypeGuard[str]:
    if isinstance(value, str):
        return True
    return False
