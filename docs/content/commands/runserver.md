+++
"@type" = "WebPage"
name = "Commands: runserver"
abstract = "Documentation for Blurry's runserver command"
datePublished = 2022-04-09
+++

# Commands: `runserver`

This command is a nod to [Django's command of the same name](https://docs.djangoproject.com/en/latest/ref/django-admin/#runserver).
It starts a development server on `http://127.0.0.1:8000` and live-reloads when source content changes.

`runserver` builds your site, but unlike with the [`build` command](./build.md):

* It is served on `f"http://{DEV_HOST}:{DEV_PORT}"`, which defaults to <http://127.0.0.1:8000/> and can be changed in the [settings](../configuration/settings.md)
* The `RUNSERVER` setting is set to `True`, which can be useful in conditionally rendering analytics or ad tags in [templates](../templates/syntax.md)

Its output looks something like:

```shell
$ blurry runserver
[I 230108 15:47:36 server:335] Serving on http://127.0.0.1:8000
[I 230108 15:47:36 handlers:62] Start watching changes
[I 230108 15:47:36 handlers:64] Start detecting changes
Gathered 14 tasks (sitemap and 13 content files)
Took 0.119001 seconds
```
