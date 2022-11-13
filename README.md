# Blurry

## Quickstart

### Requirements

- [Python](https://www.python.org/) >= 3.9
- [ImageMagick](https://imagemagick.org/index.php)

### Directory structure

A Blurry project uses a simple directory structure consisting of a `content` directory for [Markdown](https://daringfireball.net/projects/markdown/) site content and a `templates` directory for [Jinja](https://jinja.palletsprojects.com/en/) templates used to generate HTML pages from that Markdown content.
Blurry outputs a built site into a `build` directory.

```
.
├──🗀 build
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

Blurry content files are Markdown files with [TOML](https://toml.io/en/) front matter, which is a common pattern in other static site generators like [Hugo](https://gohugo.io/content-management/front-matter/) and [Jekyll](https://jekyllrb.com/docs/front-matter/).
The front matter should conform to a [Schema.org](https://schema.org/) Type, and the front matter will be available as template context for the Jinja template named after the schema type.
The Markdown content is converted to HTML and is added to the Jinja template context as `body`.

If the [Bacon Ipsum homepage](https://baconipsum.com/) were a blog post, for example, it might look something like this (some metadata omitted for brevity):

```markdown
---
"@type": BlogPosting
headline: Bacon Ipsum!
description: Does your lorem ipsum text long for something a little meatier? Give our generator a try… it’s tasty!
author:
  "@type": "Person"
  givenName: Pete
  familyName: Nelson
---

# Bacon Ipsum

Does your lorem ipsum text long for something a little meatier? Give our generator a try… it’s tasty!
```

The corresponding `BlogPosting.html` file might look like this:

```jinja
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="description" content="{{ description }}">
    <title>{{ headline }}</title>
    <script type="application/ld+json">{{ schema_data|safe }}</script>
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

Then visit <http://localhost:8000> in your browser to see your site.
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
