+++
"@type" = "WebPage"
name = "Content: Plugins"
+++

# Content: Plugins

Blurry ships with some custom [Mistune plugins](https://mistune.lepture.com/en/latest/plugins.html).

## Container

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

## Python Source Code

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
