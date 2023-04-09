# Blurry

![build](https://github.com/blurry-dev/blurry/actions/workflows/github-actions-nox.yml/badge.svg?branch=main)
[![PyPI](https://img.shields.io/pypi/v/blurry-cli.svg)](https://pypi.org/project/blurry-cli/)
![PyPI](https://img.shields.io/pypi/pyversions/blurry-cli.svg)
![PyPI](https://img.shields.io/github/license/blurry-dev/blurry.svg)

## Documentation

View the documentation at <https://blurry-docs.netlify.app/>

## Quickstart

### Requirements

- [Python](https://www.python.org/) >= 3.10
- [ImageMagick](https://imagemagick.org/index.php)

### Directory structure

A Blurry project uses a simple directory structure consisting of a `content` directory for [Markdown](https://daringfireball.net/projects/markdown/) site content and a `templates` directory for [Jinja](https://jinja.palletsprojects.com/en/) templates used to generate HTML pages from that Markdown content.
Blurry outputs a built site into a `dist` directory.

```text
.
├──🗀 dist
├──🗀 content
│  ├──🗎 index.md
│  └──🗀 posts
└──🗀 templates
   ├──🗎 base.html
   ├──🗎 Blog.html
   └──🗎 BlogPosting.html
```

Blurry's directory structure is used as the website's navigation structure.

### Content

Blurry content files are Markdown files with front matter, which is a common pattern in other static site generators like [Hugo](https://gohugo.io/content-management/front-matter/) and [Jekyll](https://jekyllrb.com/docs/front-matter/).
Blurry's front matter is written in [TOML](https://toml.io/en/).
The front matter should conform to a [Schema.org](https://schema.org/) Type, and the front matter will be available as template context for the Jinja template named after the schema type.
The Markdown content is converted to HTML and is added to the Jinja template context as `body`.

If the [Bacon Ipsum homepage](https://baconipsum.com/) were a blog post, for example, it might look something like this (some front matter omitted for brevity):

Let's look at the homepage for Table to Markdown, a site using Blurry in production:

```markdown
+++
"@type" = "WebApplication"
name = "Home"
abstract = "Table to Markdown is a simple Markdown table generator that converts tables from spreadsheet applications and websites into well-formatted Markdown tables."
+++

# Easy Markdown Tables with Table to Markdown

<div class="custom-element-container">
  <table-converter></table-converter>
</div>

## A beginner's guide to Markdown

In the [original Markdown spec](https://daringfireball.net/projects/markdown/), John Gruber describes Markdown as "a text-to-HTML conversion tool for web writers."
```

:::{info}
The Table to Markdown homepage includes a small amount of HTML in its Markdown content, including the `<table-converter>` [Web Component](https://developer.mozilla.org/en-US/docs/Web/Web_Components).

Web Components are a great way to sprinkle interactivity into a Markdown-based website.
:::

The corresponding `BlogPosting.html` file might look like this:

```jinja
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="description" content="{{ description }}">
    <title>{{ headline }}</title>
    {{ schema_type_tag|safe }}
    {{ open_graph_tags|safe }}
</head>

<body>
  {{ body|safe }}

  <p>Published by: {{ author.givenName }} {{ author.familyName }}</p>
</body>
</html>
```

### Commands

Blurry can build a static site to prepare for deployment, or it can be run as a server with live reload.

To build for production, run:

```bash
blurry build
```

To start the development server, run:

```bash
blurry runserver
```

Then visit <http://127.0.0.1:8000> in your browser to see your site.
The site is rebuilt when files in the `templates` and `content` directories are saved.

## Features

### First-class Schema.org support

- Front matter in Markdown files is Schema.org structured data
- Jinja templates are named after Schema.org types (`@type`)
  - Blog, BlogPosting, and WebPage are supported out of the box

For more information on valid front matter, see [Google Search Central's "Structured data type definitions"](https://developers.google.com/search/docs/data-types/article#non-amp).

## Standing on the shoulders of giants

Blurry stitches together high-quality libraries:

- [Mistune](https://mistune.readthedocs.io/) to convert Markdown to HTML
- [Jinja](https://jinja.palletsprojects.com/) for HTML templating
- [LiveReload](https://livereload.readthedocs.io/) for an HTTP server with automatic browser reloading
- [Typer](https://typer.tiangolo.com/) for its CLI interface
- [ImageMagick](https://imagemagick.org/index.php) to resize and convert images
