+++
"@type" = "WebPage"
name = "Templates: syntax"
abstract = "Documentation for Blurry's template files and Jinja syntax"
datePublished = 2023-04-09
+++

# Templates: syntax

## Overview

Templates are written in [Jinja](https://jinja.palletsprojects.com/), populated with context variables from Markdown files and other sources.
See [Templates: context](./context.md) for more information on which context variables are available and [Templates: examples](./examples.md) for starter templates with examples of how to use Blurry's context variables.

## Naming

Blurry templates should be named after a [Schema.org](https://schema.org/) type.
For example, for a template for a regular web page, the template should be named `WebPage.html` after the [WebPage Schema.org type](https://schema.org/WebPage).

![Schema.org logo](../images/schema.org-logo.png)

Some common types you might use are:

- [WebSite](https://schema.org/WebSite)
- [WebPage](https://schema.org/WebPage)
- [AboutPage](https://schema.org/AboutPage)
- [ContactPage](https://schema.org/ContactPage)
- [Blog](https://schema.org/Blog)
- [BlogPosting](https://schema.org/BlogPosting)
- [Product](https://schema.org/Product)
- [ProfilePage](https://schema.org/ProfilePage)
- [SoftwareApplication](https://schema.org/SoftwareApplication)

See [the "More specific Types" section of WebPage](https://schema.org/WebPage#subtypes) here for other WebPage subtypes, and [the "More specific Types" section of CreativeWork](https://schema.org/CreativeWork#subtypes) for other common content types.

## Custom template names

If your templates require more granularity than the Schema.org types, you can write templates with custom names and map them to Schema.org types using the `template_schema_types` setting in your [`blurry.toml` configuration file](../configuration/blurry.toml.md):

```toml
[blurry.template_schema_types]
ContextWebPage = 'WebPage'
```
