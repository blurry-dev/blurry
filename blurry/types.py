from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class MarkdownFileData:
    body: str
    front_matter: dict
    path: Path


SchemaType = Literal[
    "Article",
    "BlogPosting",
    "NewsArticle",
    "TechArticle",
    "Book",
    "Audiobook",
    "LocalBusiness",
    "NewsMediaOrganization",
    "Organization",
    "Person",
]
