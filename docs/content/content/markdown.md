+++
"@type" = "WebPage"
name = "Content: Markdown"
abstract = "Documentation for Blurry's Markdown handling"
datePublished = 2023-04-09
datePublished = 2023-06-04
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

### Images

See [Content: images](./images.md) for more information.

### Videos

See [Content: videos](./videos.md) for more information.

## Plugins

### Punctuation

Blurry includes a plugin to convert certain punctuation shortcuts into the apporpriate characters.
For example:

- `---` is converted into an em dash (---)
- `--` is converted into an en dash (--)

### Container

Blurry ships with a "Container" plugin, which extends Mistune's [Admonition directive](https://mistune.lepture.com/en/latest/directives.html#admonitions) and is useful for notes, warnings, and other asides.
Its syntax is:

```markdown
:::{info}
I'm an info paragraph!
:::
```

which renders as:

```html
<aside role="note" class="info">
    <p>I'm an info paragraph!</p>
</aside>
```

Supported container names are:

- `attention`
- `caution`
- `danger`
- `error`
- `hint`
- `important`
- `info`
- `note`
- `tip`
- `warning`

:::{tip}
Check out the CSS for this `<aside>` element for an example of how to style these containers.
Pay special attention to the `aside[role="note"]::before` rules.
:::

### Python Source Code

Blurry's Python Source Code plugin makes it easy to insert the source of a Python function, class, or other object into a document as a fenced code block.

For example, to show Blurry's internal `MarkdownFileData` type using the Python Source Code block syntax:

```markdown
@python<blurry.types.MarkdownFileData>
```

will behave the same as:

    ```python
    @dataclass
    class MarkdownFileData:
        body: str
        front_matter: dict[str, Any]
        path: Path
    ```

but the Python source code will update on build if this type changes, unlike copying & pasting the code into a code block.
