+++
"@type" = "WebPage"
name = "Plugins: write a Jinja filter plugin"
abstract = "Documentation for Blurry's Jinja filter plugins"
datePublished = 2024-02-29
+++

# Plugins: write an Jinja filter plugin

Blurry makes it easy to add [custom Jinja filters](https://jinja.palletsprojects.com/en/3.1.x/api/#custom-filters) to your site.
What is a Jinja filter?
From the Jinja docs:

> Filters are Python functions that take the value to the left of the filter as the first argument and produce a new value. Arguments passed to the filter are passed after the value.
>
> For example, the filter `{{ 42|myfilter(23) }}` is called behind the scenes as myfilter(42, 23).

## Example: "stars"

This function outputs a number of Unicode stars corresponding to the input, rounding to the nearest half-star.

```python
import math

STAR_EMPTY = "☆"
STAR_FILLED = "★"
STAR_HALF_FILLED = "⯪"


def float_to_stars(num: float, max: int = 5) -> str:
    whole_stars = math.floor(num) * STAR_FILLED
    part_star = STAR_HALF_FILLED if num - len(whole_stars) > 0 else ""
    non_empty_stars = f"{whole_stars}{part_star}"

    return f"{non_empty_stars:{STAR_EMPTY}{'<'}{max}}"
```

To use it, add the appropriate plugin syntax to your `pyproject.toml` file:

```toml
[tool.poetry.plugins."blurry.jinja_filter_plugins"]
stars = "{{ yourproject }}:float_to_stars"
```
