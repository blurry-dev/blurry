+++
"@type" = "WebPage"
name = "Plugins: write an HTML plugin"
abstract = "Documentation for Blurry's HTML plugins"
datePublished = 2022-04-15
+++

# Plugins: write an HTML plugin

A Blurry HTML plugin is a callable with three arguments:

| Argument                   | Description                                                                                |
| -------------------------- | ------------------------------------------------------------------------------------------ |
| `html: str`                | the HTML generated from a [Markdown file](../content/markdown.md)                          |
| `context: TemplateContext` | the [template context](../templates/context.md) Blurry uses to populate the Jinja template |
| `release: bool`            | whether Blurry is [building the site in release mode](../commands/build.md)                |

The callable should return an HTML string.

:::{note}
HTML plugins aren't guaranteed to run in a specific order.
Keep an eye on your plugins to ensure that one plugin doesn't undo work done by another.
:::

## Example: Blurry's HTML minification plugin

Blurry minifies HTML and CSS for release builds, and this functionality is provided by a plugin that ships with Blurry:

@python<blurry.plugins.html_plugins.minify_html_plugin>
