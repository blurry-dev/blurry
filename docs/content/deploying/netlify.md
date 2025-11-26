+++
"@type" = "WebPage"
name = "Deploying: Netlify"
abstract = "Documentation for deploying a Blurry project to Netlify"
datePublished = 2025-11-26
+++

# Deploying: Netlify

![Netlify logo](../images/netlify-logo.png)

As of [version 0.19.0](https://github.com/blurry-dev/blurry/releases/tag/v0.19.0), which changed how AVIFs are generated, Blurry requires no special steps to deploy to Netlify.

The simplest way to deploy a Blurry site to Netlify is to create a `netlify.toml` configuration file:

```toml
[build]
command = "blurry build"
publish = "dist/"
environment = { PYTHON_VERSION = "3.14" }
```

This configuration will work if you manage your dependencies with `pip` (and a `requirements.txt` file) or with [Pipenv](https://pipenv.pypa.io/en/latest/).

:::{note}
As of the time of writing, Netlify supports `pip` and  natively but not [Poetry](https://python-poetry.org/) or [uv](https://docs.astral.sh/uv/).
See [Netlify's "Available software at build time" page](https://docs.netlify.com/build/configure-builds/available-software-at-build-time/) for an up-to-date list.
:::

It's possible to use other package managers, too.
Here's a quick example showing how to use Poetry in Netlify to deploy your Blurry site:

```toml
[build]
command = """
curl -sSL https://install.python-poetry.org | python3 -
poetry install
poetry run blurry build
"""
publish = "dist/"
environment = { PYTHON_VERSION = "3.13" }
```

