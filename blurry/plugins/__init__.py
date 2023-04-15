from importlib.metadata import entry_points

discovered_markdown_plugins = entry_points(group="blurry.markdown_plugins")
discovered_html_plugins = entry_points(group="blurry.html_plugins")
