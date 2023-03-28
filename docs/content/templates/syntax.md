+++
"@type" = "WebPage"
name = "Templates: syntax"
+++

# Templates: syntax

## Overview

Templates are written in [Jinja](https://jinja.palletsprojects.com/), populated with context variables from Markdown files and other sources. See [Templates: context](./context.md) for more information on which context variables are available.

## Naming

Blurry templates should be named after a [Schema.org](https://schema.org/) type.
For example, for a template for a regular web page, the template should be named `WebPage.html` after the [WebPage Schema.org type](https://schema.org/WebPage).

![Schema.org logo](../images/schema.org-logo.png)

Some common types you might use are:

* [WebPage](https://schema.org/WebPage)
* [AboutPage](https://schema.org/AboutPage)
* [ContactPage](https://schema.org/ContactPage)
* [Blog](https://schema.org/Blog)
* [BlogPosting](https://schema.org/BlogPosting)
* [Product](https://schema.org/Product)
* [ProfilePage](https://schema.org/ProfilePage)
* [SoftwareApplication](https://schema.org/SoftwareApplication)

See [the "More specific Types" section of WebPage](https://schema.org/WebPage#subtypes) here for other WebPage subtypes, and [the "More specific Types" section of CreativeWork](https://schema.org/CreativeWork#subtypes) for other common content types.

## Example templates

Here are simple templates that can serve as starting points for your own theme:

`base.html`:

```html
<!doctype html>
<html lang="en-CA">
<head>
    <title>{% block title %}{% endblock %} · {{ sourceOrganization.name }}</title>
    <meta charset="utf-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1.0">
    <meta name="description"
        content="{% block description %}{% endblock %}">
    <link rel="canonical"
        href="{{ url }}">
    {{ open_graph_tags|safe }}
    {{ schema_data_tag|safe }}
</head>
<body>
    <main>{% block body %}{% endblock %}</main>
</body>
</html>
```

`WebPage.html`:

```html
{% extends "base.html" %}

{% block title %}{{ name }}{% endblock %}
{% block description %}{{ abstract }}{% endblock %}

{% block body %}
<article>
  {{ body|safe }}
</article>
{% endblock %}
```
