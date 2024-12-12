+++
"@type" = "WebPage"
name = "Content: dynamic"
abstract = "Documentation for Blurry's dynamic file handling using Jinja"
datePublished = 2024-12-12
+++

# Content: dynamic

When a file in your content directory ends with `.jinja`, Blurry uses [Jinja](https://jinja.palletsprojects.com/en/stable/) to transform that file, giving you lots of flexibility to build dynamic files based on your Markdown content.

Jinja files in your content directory have these context variables available:

- `datetime`: a [Python `datetime` object](https://docs.python.org/3/library/datetime.html#datetime-objects)
- `settings`: see [Configuration: settings](../configuration/settings.md) for more information
- `file_data_by_directory`: see [Templates: context](../templates/context.md) for more information

## Example

For example, say we have blog posts in `/content/blog/`, and we have a `content/blog/feed.xml` file:

```xml
<?xml version="1.0" encoding="UTF-8" ?>
{% with directory="blog", datetime_format="%a, %d %b %Y %H:%M:%S %z", item_count=10 %}
<rss version="2.0">
<channel>
 <title>John Franey | Blog</title>
 <description>John Franey's blog feed</description>
 <link>https://{{ settings.DOMAIN }}/{{ directory }}/feed.xml</link>
 <copyright>{{ datetime.now().strftime('%Y') }} {{ settings.DOMAIN }} All rights reserved</copyright>
 <lastBuildDate>{{ datetime.now().strftime(datetime_format).strip() }}</lastBuildDate>

{% for page in (file_data_by_directory[directory])[0:item_count] %}
 <item>
  <title>{{ page.front_matter.headline }}</title>
  <description>{{ page.front_matter.abstract }}</description>
  <link>{{ page.front_matter.url }}</link>
  <guid isPermaLink="false">{{ page.front_matter.url }}</guid>
  <pubDate>{{ page.front_matter.datePublished.strftime(datetime_format).strip() }}</pubDate>
 </item>
{% endfor %}

</channel>
</rss>
{% endwith %}
```

It will output an RSS feed with the 10 most recent entries in the `blog` directory.
