+++
"@type" = "WebPage"
name = "Commands: runserver"
abstract = "Documentation for Blurry's runserver command"
datePublished = 2023-04-09
dateModified = 2024-01-03
+++

# Commands: `runserver`

## Usage

This command is a nod to [Django's command of the same name](https://docs.djangoproject.com/en/latest/ref/django-admin/#runserver).
It starts a development server on `http://127.0.0.1:8000` and live-reloads when source content changes.

`runserver` builds your site, but unlike with the [`build` command](./build.md):

- It is served on `f"http://{DEV_HOST}:{DEV_PORT}"`, which defaults to <http://127.0.0.1:8000/> and can be changed in the [settings](../configuration/settings.md)
- The `RUNSERVER` setting is set to `True`, which can be useful in conditionally rendering analytics or ad tags in [templates](../templates/syntax.md)

## Example

`runserver`'s output looks something like:

```shell
$ blurry runserver
.  .             
|-.| . ..-..-.. .
`-''-'-''  '  '-|
              `-'
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┓
┃ Markdown Plugins    ┃ HTML Plugins ┃ Jinja Plugins ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━┩
│ container           │ minify_html  │ body_to_cards │
│ punctuation         │              │ headings      │
│ python_code         │              │ url_path      │
│ python_code_in_list │              │ blurry_image  │
└─────────────────────┴──────────────┴───────────────┘
[I 250103 10:41:51 server:331] Serving on http://127.0.0.1:8000
[I 250103 10:41:51 handlers:62] Start watching changes
[I 250103 10:41:51 handlers:64] Start detecting changes
Blurring 21 Markdown files and 6 other files
Built site in 2.465286 seconds
```
