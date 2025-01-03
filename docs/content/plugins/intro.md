+++
"@type" = "WebPage"
name = "Plugins: intro"
abstract = "Documentation for Blurry's plugin architecture"
datePublished = 2023-04-15
dateModified = 2024-01-03
+++

# Plugins: intro

:::{info}
This documentation covers how to write and register Blurry plugins.
For documentation about custom [Mistune](https://mistune.lepture.com/en/latest/) plugins that Blurry ships with out-of-the-box, see [Content: Markdown](../content/markdown.md).
:::

Blurry ships with a simple plugin infrastructure that makes it easy to write and register plugins that change how Blurry processes Markdown and HTML.

## How to write a plugin

See the docs for the type of plugin you'd like to write:

- [Plugins: write a Markdown plugin](./write-a-markdown-plugin.md)
- [Plugins: write an HTML plugin](./write-an-html-plugin.md)
- [Plugins: write a Jinja filter plugin](./write-a-jinja-filter-plugin.md)
- [Plugins: write a Jinja extension plugin](./write-a-jinja-extension-plugin.md)

## How to register a plugin

Plugins are registered using [Python entry points](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-package-metadata).

To register your plugin, add it as an entry point in one of the following entry point groups in your package's configuration file (e.g., `pyproject.toml` or `setup.py`):

- `blurry.html_plugins` for plugins that modify the HTML Blurry generates from Markdown files
- `blurry.markdown_plugins` for plugins that add Markdown functionality via [Mistune plugins](https://mistune.lepture.com/en/latest/advanced.html#create-plugins)

## Examples

For a simple example of a Markdown plugin, see Blurry's own punctuation plugin: <https://github.com/blurry-dev/blurry/blob/main/blurry/plugins/markdown_plugins/punctuation_plugin.py>.

Blurry [dogfoods](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) its own plugin architecture, so you can use the Blurry source code as an example of writing a Blurry Plugin.
See which plugins are registered in [Blurry's `pyproject.toml` file](https://github.com/blurry-dev/blurry/blob/main/pyproject.toml).
