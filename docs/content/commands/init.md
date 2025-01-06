+++
"@type" = "WebPage"
name = "Commands: init"
abstract = "Documentation for Blurry's build command"
datePublished = 2025-01-07
+++

# Commands: init

## Description

The `init` command creates a new Blurry project in the current directory.
It creates everything you need to start working on your site:

- A `blurry.toml` [configuration file](../configuration/blurry.toml.md)
- A [Markdown file](../content/markdown.md) for your site's homepage in `content/index.md`
- A base [template file](../templates/syntax.md) and a `WebSite` template file for your homepage in `templates/`

## Usage

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
