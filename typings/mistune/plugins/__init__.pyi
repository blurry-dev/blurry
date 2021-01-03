"""
This type stub file was generated by pyright.
"""

from .extra import plugin_strikethrough, plugin_url
from .footnotes import plugin_footnotes
from .table import plugin_table
from .task_lists import plugin_task_lists

PLUGINS = { 'url': plugin_url,'strikethrough': plugin_strikethrough,'footnotes': plugin_footnotes,'table': plugin_table,'task_lists': plugin_task_lists }