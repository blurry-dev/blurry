from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape
from blurry.plugins import discovered_jinja_extensions
from blurry.plugins import discovered_jinja_filter_plugins
from blurry.settings import get_templates_directory
from blurry.settings import SETTINGS


def get_jinja_env():
    jinja_env = Environment(
        loader=FileSystemLoader(get_templates_directory()),
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
    return jinja_env
