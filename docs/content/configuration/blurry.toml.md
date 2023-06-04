+++
"@type" = "WebPage"
name = "Configuration: blurry.toml"
abstract = "Documentation for Blurry's blurry.toml configuration file"
datePublished = 2023-04-09
+++

# blurry.toml

Blurry's configuration file is `blurry.toml`, written in [TOML](https://toml.io/en/).
It is comprised of two main parts: `[blurry]` for specifying Blurry setting values and `[blurry.schema_data]` for specifying global schema data for Markdown files.

Here's a real-world example:

```toml
[blurry]
domain = "blurry.johnfraney.ca"
maximum_image_width = 750
thumbnail_width = 285

[blurry.schema_data.author]
name = "John Franey"
url = "https://johnfraney.ca/"

[blurry.schema_data.sourceOrganization]
name = "Blurry"
```

## `[blurry]`

This is where you can override Blurry's [default settings](./settings.md).
Setting names in `blurry.toml` are case-insensitive, so you can write them in uppercase (`DOMAIN = "..."`) or lowercase (`domain = "..."`).

## `[blurry.schema_data]`

Values under `[blurry.schema_data]` will be used as default front matter values for each Markdown file, and it's especially useful for global schema properties, like [`sourceOrganization`](https://schema.org/sourceOrganization).
