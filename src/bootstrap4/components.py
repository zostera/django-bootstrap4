from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

from bootstrap4.utils import render_tag

from .text import text_value


def render_alert(content, alert_type=None, dismissible=True):
    """Render a Bootstrap alert."""
    button = ""
    if not alert_type:
        alert_type = "info"
    css_classes = ["alert", "alert-" + text_value(alert_type)]
    if dismissible:
        css_classes.append("alert-dismissible")
        close = _("close")
        button = f'<button type="button" class="close" data-dismiss="alert" aria-label="{close}">&times;</button>'
    button_placeholder = "__BUTTON__"
    return mark_safe(
        render_tag(
            "div",
            attrs={"class": " ".join(css_classes), "role": "alert"},
            content=mark_safe(button_placeholder) + text_value(content),
        ).replace(button_placeholder, button)
    )
