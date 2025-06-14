from rich.console import Console
from rich.table import Table
import wand.version

from blurry.plugins import discovered_html_plugins
from blurry.plugins import discovered_jinja_extensions
from blurry.plugins import discovered_jinja_filter_plugins
from blurry.plugins import discovered_markdown_plugins

console = Console()


def print_blurry_name():
    console.print(
        """
.  .             
|-.| . ..-..-.. .
`-''-'-''  '  '-|
              `-'
    """.strip()
    )


def print_plugin_table():
    plugin_table = Table(show_header=True)
    plugin_table.add_column("Markdown Plugins")
    plugin_table.add_column("HTML Plugins")
    plugin_table.add_column("Jinja Plugins")
    plugin_table.add_row(
        "\n".join([p.name for p in discovered_markdown_plugins]),
        "\n".join([p.name for p in discovered_html_plugins]),
        "\n".join(
            [p.name for p in discovered_jinja_filter_plugins]
            + [p.name for p in discovered_jinja_extensions]
        ),
    )

    console.print(plugin_table)


def check_avif_support(console: Console):
    if "AVIF" in wand.version.formats():
        return
    console.print(
        "AVIF support not found. Falling back to WEBP. See https://trac.ffmpeg.org/wiki/Encode/AV1"
    )
