+++
"@type" = "WebPage"
name = "Plugins: write a Markdown plugin"
abstract = "Documentation for Blurry's Markdown plugins"
datePublished = 2022-04-15
+++

# Plugins: write a Markdown plugin

A Blurry Markdown plugin actually a Mistune plugin.
See the [Mistune plugin docs](https://mistune.lepture.com/en/latest/advanced.html#create-plugins) for more information on writing plugins, and check out the examples of inline and block Markdown plugins below.

## Example: inline plugin

Blurry ships with a simple punctuation plugin, which is a [Mistune inline level plugin](https://mistune.lepture.com/en/latest/advanced.html#block-level-plugin):

@python<blurry.plugins.markdown_plugins.punctuation_plugin>

## Example: block plugin

The Mistune plugin Blurry uses to display Python source code in Markdown is an example of a [Mistune block level plugin](https://mistune.lepture.com/en/latest/advanced.html#block-level-plugin):

@python<blurry.plugins.markdown_plugins.python_code_plugin>
