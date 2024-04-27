from importlib.metadata import entry_points

discovered_markdown_plugins = entry_points(group="blurry.markdown_plugins")
discovered_html_plugins = entry_points(group="blurry.html_plugins")
discovered_jinja_filter_plugins = entry_points(group="blurry.jinja_filter_plugins")
discovered_jinja_extensions = entry_points(group="blurry.jinja_extensions")
