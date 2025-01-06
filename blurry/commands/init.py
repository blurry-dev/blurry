import tomllib
from datetime import datetime
from pathlib import Path

from rich.prompt import Prompt

from blurry.settings import get_content_directory
from blurry.settings import get_templates_directory
from blurry.settings import update_settings


BLURRY_CONFIG_TEMPLATE = """
[blurry]
domain = "{domain}"
markdown_file_jinja_template_extension = ".jinja"

[blurry.schema_data.sourceOrganization]
name = "{project_name}"
url = "https://{domain}"
""".strip()

HOMEPAGE_MARKDOWN = """
+++
"@type" = "WebSite"
name = "Home"
abstract = "The homepage of {project_name}, built with Blurry."
datePublished = {date_published}
+++

# Welcome to your new Blurry site

To learn more about how to get started, check out Blurry's quick start docs:

<https://blurry-docs.netlify.app/getting-started/quick-start/>
""".strip()

BASE_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="color-scheme" content="light dark">
    <link
      rel="stylesheet"
      href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css"
    >
    <title>{% block title %}{% endblock %} | {{ sourceOrganization.name }}</title>
    <meta name="description" content="{% block description %}{% endblock %}">
    <link rel="canonical" href="{{ url }}">
    {{ open_graph_tags|safe }}
    {{ schema_type_tag|safe }}
  </head>
  <body>
    <nav class="container">
      <ul>
        <li><strong>{{ sourceOrganization.name }}</strong></li>
      </ul>
      <ul>
        <li><a href="/">Home</a></li>
      </ul>
    </nav>

    <main class="container">
      {% block body %}{% endblock %}
    </main>
  </body>
</html>
"""


WEBSITE_TEMPLATE = """
{% extends "base.jinja" %}

{% block title %}{{ name }}{% endblock %}
{% block description %}{{ abstract }}{% endblock %}

{% block body %}
<article>
  {{ body|safe }}
</article>
{% endblock %}
"""


def initialize_new_project(name: str | None, domain: str | None):
    update_settings()
    blurry_config_file = Path("blurry.toml")
    blurry_template_directory = get_templates_directory()
    blurry_content_directory = get_content_directory()

    if (
        blurry_config_file.exists()
        or blurry_template_directory.exists()
        or blurry_content_directory.exists()
    ):
        print("Blurry project already initialized.")
        return
    name = name or Prompt.ask(
        "What is the name of your company, project, or website?",
    )
    domain = domain or Prompt.ask("What is your website's domain?")

    config_text = BLURRY_CONFIG_TEMPLATE.format(domain=domain, project_name=name)

    try:
        tomllib.loads(config_text)
    except tomllib.TOMLDecodeError as e:
        print(f"Error in configuration file: {e}.")
        print("Please check your input and try again.")
        exit(1)

    blurry_config_file.write_text(config_text)

    # Write template files
    blurry_template_directory.mkdir(exist_ok=True)
    base_template_file = blurry_template_directory / "base.jinja"
    base_template_file.write_text(BASE_TEMPLATE)

    website_template_file = blurry_template_directory / "WebSite.jinja"
    website_template_file.write_text(WEBSITE_TEMPLATE)

    # Write homepage Markdown file
    date_published = datetime.now().strftime("%Y-%m-%d")
    blurry_content_directory.mkdir(exist_ok=True)
    homepage = blurry_content_directory / "index.md"
    homepage.write_text(
        HOMEPAGE_MARKDOWN.format(
            date_published=date_published,
            project_name=name,
        )
    )

    print("Blurry project initialized!")
    print("Run 'blurry runserver' to start the dev server.")
