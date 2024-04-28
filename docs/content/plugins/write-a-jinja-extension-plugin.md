+++
"@type" = "WebPage"
name = "Plugins: write a Jinja extension plugin"
abstract = "Documentation for Blurry's Jinja extension plugins"
datePublished = 2024-04-28
+++

# Plugins: write an Jinja extension plugin

Blurry makes it easy to add [custom Jinja extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/) to your site.
What is a Jinja extension?
From the Jinja docs:

> Jinja supports extensions that can add extra filters, tests, globals or even extend the parser. The main motivation of extensions is to move often used code into a reusable class like adding support for internationalization.

With [custom extensions](https://jinja.palletsprojects.com/en/3.1.x/extensions/#module-jinja2.ext) you can add custom tags to Jinja, like Blurry's `{% blurry_image %}` tag.

## Example: `{% blurry_image %}`

This tag finds the optimized version of an image at the specified URL, and optionally of the specified size.
You can find it in Blurry's source code in `blurry/plugins/jinja_plugins/blurry_image_extension.py`.

Under the hood the extension uses [`jinja2-simple-tags`](https://github.com/dldevinc/jinja2-simple-tags) to simplify the process of writing a custom extension.

To use a custom Jinja extension you've developed, add the appropriate plugin syntax to your project's `pyproject.toml` file:

```toml
[tool.poetry.plugins."blurry.jinja_extensions"]
stars = "{{ yourproject.your_extension_file }}:YourExtension"
```
