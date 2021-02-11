# Blurry

## Standing on the shoulders of giants

Blurry stitches together high-quality libraries:

- [Mistune](https://mistune.readthedocs.io/en/latest/) to convert Markdown to HTML
- [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) for HTML templating
- [LiveReload](https://livereload.readthedocs.io/en/latest/) for an HTTP server with automatic browser reloading
- [Typer](https://typer.tiangolo.com/) for the CLI interface

# Features

## First-class Schema.org support

- YAML front matter in Markdown files is Schema.org structured data
- Jinja templates are named after Schema.org types (`@type`)
    - Blog, BlogPosting, and WebPage are supported out of the box

For more information on valid front matter, see [Google Search Central's "Structured data type definitions"](https://developers.google.com/search/docs/data-types/article#non-amp).
