from django.forms.utils import flatatt
from django.utils.html import format_html

from django_bootstrap4.text import text_value
from django_bootstrap4.utils import get_url_attrs


def render_script_tag(url):
    """Build a script tag."""
    return render_tag("script", get_url_attrs(url, attr_name="src"))


def render_link_tag(url):
    """Build a link tag."""
    attrs = get_url_attrs(url, attr_name="href")
    attrs["rel"] = "stylesheet"
    return render_tag("link", attrs=attrs, close=False)


def render_tag(tag, attrs=None, content=None, close=True):
    """Render an HTML tag."""
    attrs_string = flatatt(attrs) if attrs else ""
    builder = "<{tag}{attrs}>{content}"
    content_string = text_value(content)
    if content_string or close:
        builder += "</{tag}>"
    return format_html(builder, tag=tag, attrs=attrs_string, content=content_string)
