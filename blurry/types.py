from dataclasses import dataclass
from pathlib import Path


@dataclass
class MarkdownFileData:
    body: str
    front_matter: dict
    path: Path
