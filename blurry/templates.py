import jinjax
from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape

from blurry.plugins import discovered_jinja_extensions
from blurry.plugins import discovered_jinja_filter_plugins
from blurry.settings import get_templates_directory
from blurry.settings import SETTINGS


def get_jinja_env() -> Environment:
    """
    Returns a Jinja environment complete with JinjaX and any installed Jinja extensions and filters.
    """
    templates_directory = get_templates_directory()
    jinja_env = Environment(
        loader=FileSystemLoader(templates_directory),
        autoescape=select_autoescape(
            list(
                {
                    SETTINGS["MARKDOWN_FILE_JINJA_TEMPLATE_EXTENSION"].lstrip("."),
                    "html",
                    "xml",
                }
            )
        ),
        extensions=[
            jinja_extension.load() for jinja_extension in discovered_jinja_extensions
        ],
    )
    for filter_plugin in discovered_jinja_filter_plugins:
        try:
            jinja_env.filters[filter_plugin.name] = filter_plugin.load()
        except AttributeError:
            print(
                f"Could not load Jinja filter plugin: {filter_plugin.name}. "
                "Possibly because {filter_plugin.value} is not a valid object reference."
            )

    jinja_env.add_extension(jinjax.JinjaX)
    catalog = jinjax.Catalog(jinja_env=jinja_env)
    catalog.add_folder(templates_directory / "components")

    return jinja_env
