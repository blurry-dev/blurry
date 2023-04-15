+++
"@type" = "WebPage"
name = "Templates: examples"
abstract = "Example Jinja templates for your Blurry project"
datePublished = 2022-04-09
+++

# Templates: examples

## Base template

To keep your template files DRY, it's helpful to have a base template that includes any content that's common to every page, like the header, main menu, and footer.
Thanks to [Jinja's template inheritance](https://jinja.palletsprojects.com/en/3.1.x/templates/#template-inheritance), this base template can include "blocks" that can be populated by more specific templates.

Here's a simple base template with blocks for:

- `title`
- `description`
- `body`

```html
<!doctype html>
<html lang="en-CA">
<head>
    <title>{% block title %}{% endblock %} · {{ sourceOrganization.name }}</title>
    <meta charset="utf-8">
    <meta name="viewport"
        content="width=device-width, initial-scale=1">
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

## Basic page template

Here is a basic `WebPage.html` template.
The `title`, `description`, and `body` blocks will populate the base template above.

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

## Homepage with blog preview

This template includes the three most recent pages from the `blog` directory (based on the homepage template of [JohnFraney.ca](https://johnfraney.ca/)):

```html
{% extends "base.html" %}

{% block title %}{{ name }}{% endblock %}
{% block description %}{{ abstract }}{% endblock %}

{% block body %}
{{ body|safe }}

<hr>

<h2>Recent Posts</h2>
<section>
  {% for page in (file_data_by_directory['blog'])[0:3] %}
  <div>
    <h3><a href="{{ page.front_matter.url }}">{{ page.front_matter.headline }}</a></h3>
    <div>
      🗓 <time datetime="{{ page.datePublished }}">{{ page.datePublished }}</time> ·
      🏷 {% for keyword in page.keywords.split(',') %}{{ keyword }}{% if not loop.last %}, {% endif %}{% endfor %}
    </div>
    <p>{{ page.front_matter.abstract }}</p>
    <p><a href="{{ page.front_matter.url }}">Continue reading &rarr;</a></p>
  </div>
  {% endfor %}
</section>
{% endblock %}
```

For more information on the `file_data_by_directory` context variable, see [Templates: context](./context.md).

## Blog index with a list of posts

This is a simple [Blog](https://schema.org/Blog) template (`Blog.html`) with a list of posts sorted newest to oldest:

```html
{% extends "base.html" %}

{% block title %}{{ name }}{% endblock %}
{% block description %}{{ abstract }}{% endblock %}

{% block body %}
{{ body|safe }}

{% if sibling_pages %}
<h2>Posts</h2>

{% for page in sibling_pages|sort(reverse=true, attribute="datePublished") %}
<div>
  <h3><a href="{{ page.url }}">{{ page.headline }}</a></h3>
  <div>
    🗓 <time datetime="{{ page.datePublished }}">{{ page.datePublished }}</time> ·
    🏷 {% for keyword in page.keywords.split(',') %}{{ keyword }}{% if not loop.last %}, {% endif %}{% endfor %}
  </div>
  <p>{{ page.abstract }}</p>
  <p><a href="{{ page.url }}">Continue reading &rarr;</a></p>
</div>
{% if not loop.last %}<hr>{% endif %}
{% endfor %}
{% endif %}

{% endblock %}
```

For more information on the `sibling_pages` context variable, see [Templates: context](./context.md).
