+++
"@type" = "WebPage"
name = "Content: Markdown"
abstract = "Documentation for Blurry's Markdown handling"
datePublished = 2022-04-09
+++

# Content: Markdown

Content is written in Markdown with [TOML](https://toml.io/en/) front matter.
Specifically, Blurry uses [Mistune](https://mistune.lepture.com/), along with a number of Blurry-specific customizations, to convert Markdown to HTML.

Here's what a basic about page might look like, using the [AboutPage schema type](https://schema.org/AboutPage):

```markdown
+++
"@type" = "AboutPage"
name = "About Blurry"
abstract = "Learn about Blurry, a static site generator build for page speed and SEO"
datePublished = 2023-01-07
image = "../images/blurry-logo.png"
+++

# About Blurry

Regular Markdown content can go here.
```

## Customizations

On top of [Mistune's built-in plugins](https://mistune.lepture.com/en/latest/plugins.html), Blurry ships with a number of Markdown customizations.

### Links

Blurry converts relative file paths in Markdown to absolute paths in the build folder.
For example:

```markdown
[About](./about.md)
```

will be rendered as:

```html
<a href="/about/">About</a>
```

External links are opened in a new tab and have the [`rel="noopener"` attribute](https://developer.mozilla.org/en-US/docs/Web/HTML/Link_types/noopener) for security:

```html
<a href="https://johnfraney.ca/" rel="noopener" target="_blank">John Franey</a>
```

### Punctuation

Blurry includes a plugin to convert certain punctuation shortcuts into the apporpriate characters.
For example:

* `---` is converted into an em dash (---)
* `--` is converted into an en dash (--)
