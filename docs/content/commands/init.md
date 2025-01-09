+++
"@type" = "WebPage"
name = "Commands: init"
abstract = "The init command for Blurry, a Python static site generator focused on page speed and SEO"
datePublished = 2025-01-08
dateModified = 2025-01-09
+++

# Commands: `init`

## Description

The `init` command creates a new Blurry project in the current directory.
It creates everything you need to start working on your site:

- A `blurry.toml` [configuration file](../configuration/blurry.toml.md)
- A [Markdown file](../content/markdown.md) for your site's homepage in `content/index.md`
- A base [template file](../templates/syntax.md) and a `WebSite` template file for your homepage in `templates/`

## Usage

If run with no options, `blurry init` will prompt for your project's name and domain so they can be used in the new project.

Example:

```shell
$ blurry init
What is the name of your company, project, or website?: Blurry
What is your website's domain?: blurry-dev.netlify.app
Blurry project initialized!
Run 'blurry runserver' to start the dev server.
```

## Options

`name`: Your project's name

`domain`: Your project's domain

Example:

```shell
$ blurry init --name "Blurry" --domain "blurry-docs.netlify.app"
Blurry project initialized!
Run 'blurry runserver' to start the dev server.
```
