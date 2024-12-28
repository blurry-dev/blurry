+++
"@type" = "WebPage"
name = "Configuration: settings"
abstract = "Documentation for Blurry's available settings"
datePublished = 2023-04-09
+++

# Configuration: settings

## Reslution hierarchy

The setting hierarchy is:

1. Blurry's defaults
2. The [`blurry.toml` configuration file](./blurry.toml.md)
3. [Environment variables](./environment-variables.md)

## Available settings

See the `Settings` type for Blurry's available settings:

@python<blurry.settings.Settings>

The default values are visible at <https://github.com/blurry-dev/blurry/blob/main/blurry/settings.py>
