+++
"@type" = "WebPage"
name = "Configuration: settings"
+++

# Configuration: settings

The setting hierarchy is:

1. Blurry's defaults
2. The [`blurry.toml` configuration file](./blurry.toml.md)
3. [Environment variables](./environment-variables.md)

```python
class Settings(TypedDict):
    BUILD_DIRECTORY_NAME: str
    CONTENT_DIRECTORY_NAME: str
    TEMPLATES_DIRECTORY_NAME: str

    DEV_HOST: str
    DEV_PORT: int
    DOMAIN: str
    IMAGE_WIDTHS: list[int]
    MAXIMUM_IMAGE_WIDTH: int
    THUMBNAIL_WIDTH: int
    USE_HTTP: bool
    RUNSERVER: bool
    FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX: str


SETTINGS: Settings = {
    "BUILD_DIRECTORY_NAME": "build",
    "CONTENT_DIRECTORY_NAME": "content",
    "TEMPLATES_DIRECTORY_NAME": "templates",
    "DEV_HOST": "127.0.0.1",
    "DEV_PORT": 8000,
    "DOMAIN": "example.com",
    "IMAGE_WIDTHS": [360, 640, 768, 1024, 1366, 1600, 1920],
    "MAXIMUM_IMAGE_WIDTH": 1920,
    "THUMBNAIL_WIDTH": 250,
    "USE_HTTP": False,
    "RUNSERVER": False,
    "FRONTMATTER_NON_SCHEMA_VARIABLE_PREFIX": "~",
}
```
