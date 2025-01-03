+++
"@type" = "WebPage"
name = "Commands: build"
abstract = "Documentation for Blurry's build command"
datePublished = 2023-04-09
dateModified = 2024-01-03
+++

# Commands: build

## Usage

`build` builds a production-ready version of a Blurry static site.
It outputs the site in the folder specified by the `build_directory_name` [setting](./../configuration/settings.md), which defaults to `./dist/`

To build the site, Blurry:

- Generates responsive image sizes
- Converts images to AVIF
- Generates HTML pages (minified)
- Generates a sitemap

For the given `content` directory contents:

```shell
$ tree content
content
├── commands
│   ├── build.md
│   └── runserver.md
├── configuration
│   ├── blurry.toml.md
│   ├── environment-variables.md
│   └── settings.md
├── content
│   ├── images.md
│   └── markdown.md
├── getting-started
│   ├── introduction.md
│   └── quick-start.md
├── images
│   └── schema.org-logo.png
├── index.md
└── templates
    ├── context.md
    └── syntax.md

7 directories, 13 files
```

the `build` output would look something like:

```shell
$ blurry build
Gathered 14 tasks (sitemap and 13 content files)
Took 0.143583 seconds
```

and the `dist/` directory would look like:

```shell
$ tree dist
dist
├── commands
│   ├── build
│   │   └── index.html
│   └── runserver
│       └── index.html
├── configuration
│   ├── blurry.toml
│   │   └── index.html
│   ├── environment-variables
│   │   └── index.html
│   └── settings
│       └── index.html
├── content
│   ├── images
│   │   └── index.html
│   └── markdown
│       └── index.html
├── getting-started
│   ├── introduction
│   │   └── index.html
│   └── quick-start
│       └── index.html
├── images
│   ├── schema.org-logo-285.avif
│   ├── schema.org-logo-285.png
│   ├── schema.org-logo-354.avif
│   ├── schema.org-logo-354.png
│   ├── schema.org-logo.avif
│   └── schema.org-logo.png
├── index.html
├── sitemap.xml
└── templates
    ├── context
    │   └── index.html
    └── syntax
        └── index.html

18 directories, 19 files
```

## Options

`clean`: cleans the build directory before building.

Usage:

```bash
blurry build --clean
```
