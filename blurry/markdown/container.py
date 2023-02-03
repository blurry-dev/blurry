from mistune.directives import Admonition
from mistune.directives.admonition import render_admonition_content
from mistune.directives.admonition import render_admonition_title


class Container(Admonition):
    """Custom admonition directive using an <aside> HTML element"""

    SUPPORTED_NAMES = {
        "attention",
        "caution",
        "danger",
        "error",
        "hint",
        "important",
        "info",
        "note",
        "tip",
        "warning",
    }

    def __call__(self, directive, md):
        for name in self.SUPPORTED_NAMES:
            directive.register(name, self.parse)

        if md.renderer.NAME == "html":
            md.renderer.register("admonition", render_admonition)
            md.renderer.register("admonition_title", render_admonition_title)
            md.renderer.register("admonition_content", render_admonition_content)


def render_admonition(self, text, name, **attrs):
    _cls = attrs.get("class", "")
    class_attribute = f"{name} {_cls}".strip()
    return f'<aside role="note" class="{class_attribute}">{text}</aside>'


def render_admonition_title(self, text):
    return ""
