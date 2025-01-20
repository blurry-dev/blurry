# Blurry

[![Nox build status](https://github.com/blurry-dev/blurry/actions/workflows/github-actions-nox.yml/badge.svg?branch=main)](https://github.com/blurry-dev/blurry/actions/workflows/github-actions-nox.yml)
[![PyPI package version](https://img.shields.io/pypi/v/blurry-cli.svg)](https://pypi.org/project/blurry-cli/)
[![PyPI Python versions](https://img.shields.io/pypi/pyversions/blurry-cli.svg)](https://pypi.org/project/blurry-cli/)
[![PyPI downloads per month](https://img.shields.io/pypi/dm/blurry-cli.svg)](https://pypi.python.org/pypi/blurry-cli/)
![Package license](https://img.shields.io/github/license/blurry-dev/blurry.svg)

![Blurry logo](https://github.com/blurry-dev/blurry/raw/main/docs/content/favicon.png)

## tl;dr

Blurry is a schema-first, plugin-enabled static site generator.
Markdown front matter directly to [Schema.org types](https://schema.org/docs/full.html), so your content is SEO-friendly and [rich results-ready](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) out of the box.

Blurry also makes your images responsive, supports embedding Python source code in Markdown files, and more.

Check out the docs and try it out!

**Note**: Until v1.0.0, minor versions (0.x.0) may not be backwards compatible.

## Documentation

View the documentation site at <https://blurry-docs.netlify.app/>.

## Contributing

Contributions are welcome!
Check out [the contribution docs](https://github.com/blurry-dev/blurry/blob/main/CONTRIBUTING.md) to get started.

## Security contact information

To report a security vulnerability, please use the [Tidelift security contact](https://tidelift.com/security).
Tidelift will coordinate the fix and disclosure.

## Standing on the shoulders of giants

Blurry blends together high-quality libraries:

- [Mistune](https://mistune.readthedocs.io/) to convert Markdown to HTML
- [Jinja](https://jinja.palletsprojects.com/) for HTML templating
- [JinjaX](https://jinjax.scaletti.dev/) for Jinja components
- [LiveReload](https://livereload.readthedocs.io/) for an HTTP server with automatic browser reloading
- [Typer](https://typer.tiangolo.com/) for its CLI interface
- [ImageMagick](https://imagemagick.org/index.php) to resize and convert images

&copy; 2020-present, John Franey
