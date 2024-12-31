+++
"@type" = "WebSite"
name = "Introduction"
abstract = "A Python-powered static site generator with a focus on page speed and SEO."
datePublished = 2023-04-09
+++

# Blurry: A Python-powered static site generator

```shell
$ blurry build
.  .             
|-.| . ..-..-.. .
`-''-'-''  '  '-|
              `-'
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Markdown Plugins    ┃ HTML Plugins ┃ Jinja Plugins ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ blur_blurry_name    │ minify_html  │ body_to_cards │
│ container           │              │ headings      │
│ punctuation         │              │ url_path      │
│ python_code         │              │ blurry_image  │
│ python_code_in_list │              │               │
└─────────────────────┴──────────────┴───────────────┘
Blurring 21 Markdown files and 5 other files
Markdown ━━━━━━━━━━━━━━━━━━━━━━━━━━╸━━━━━━━━━━━━━  67%
Other    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
```

## What is Blurry?

Blurry is a static site generator with a terrible pun of a name: if you're generating static sight, you're making things Blurry.

Blurry brings the concept of schema-first development to static site generators.
Specifically, Blurry uses [Schema.org](https://schema.org/) schema type names as the names for its template files, and schema type properties as Markdown front matter to populate those templates.

## Goals

<div class="flex-grid">

<article>

### 📈 SEO performance

Blurry supports [Schema.org](https://schema.org/) and [Open Graph](https://ogp.me/) with zero configuration.
This enables [rich Google results](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) and [link previews](https://www.opengraph.xyz/) out-of-the-box.

</article>

<article>

### 🏎️ Page speed

While using Blurry doesn't guarantee good page speed, it does solve a number of pain points that tend to slow down page loads.

[Blurry's image handling](../content/images.md) and HTML minification, for instance, can help get you a 100/100 [PageSpeed](https://pagespeed.web.dev/) score if the rest of your site is fast.

</article>

<article>

### ⚙ Minimal configuration

Blurry seeks to use sensible defaults so you can spend less time configuring and more time writing.

A viable Blurry configuration file ([`blurry.toml`](./../configuration/blurry.toml.md)) can be as simple as:

```toml
[blurry]
domain = "johnfraney.ca"
```

</article>

<article>

### 🧹 Semantic HTML

Where applicable, Blurry tries to use semantic HTML elements like `<aside>` over more generic elements like `<div>`.
Using semantic HTML elements also facilities classless CSS styling, which can be useful when styling some Markdown-generated HTML elements, and it can be [good for accessibility](https://developer.mozilla.org/en-US/docs/Learn/Accessibility/HTML), too.

</article>

</div>

## Non-goals

<div class="flex-grid">

<article>

### 🚄 "Gotta go fast!"

While Blurry aims to be performant, build performance is not its top priority.
It's written in Python, so it _may_ not be able to compete on speed with other static site generators like [Hugo](https://gohugo.io/).
Instead, it aims to be _fast_enough_ while optimizing for developer and user experience.

</article>

</div>
