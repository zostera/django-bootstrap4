from django import get_version
from django.template import engines
from django.test import TestCase

DJANGO_VERSION = get_version()


def html_39x27(html):
    """
    Return HTML string with &#39; (Django < 3) instead of &#x27; (Django >= 3).

    See https://docs.djangoproject.com/en/dev/releases/3.0/#miscellaneous
    """
    if DJANGO_VERSION < "3":
        return html.replace("&#x27;", "&#39;")
    return html


class BootstrapTestCase(TestCase):
    """TestCase with render function for template code."""

    def render(self, text, context=None, load_bootstrap=True):
        """Return rendered result of template with given context."""
        prefix = "{% load django_bootstrap5 %}" if load_bootstrap else ""
        template = engines["django"].from_string(f"{prefix}{text}")
        return template.render(context or {})
