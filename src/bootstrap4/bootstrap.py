from importlib import import_module

from django.conf import settings

BOOTSTRAP4_DEFAULTS = {
    "css_url": {
        "href": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css",
        "integrity": "sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z",
        "crossorigin": "anonymous",
    },
    "javascript_url": {
        "url": "https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js",
        "integrity": "sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV",
        "crossorigin": "anonymous",
    },
    "theme_url": None,
    "jquery_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.min.js",
        "integrity": "sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2",
        "crossorigin": "anonymous",
    },
    "jquery_slim_url": {
        "url": "https://code.jquery.com/jquery-3.5.1.slim.min.js",
        "integrity": "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj",
        "crossorigin": "anonymous",
    },
    "popper_url": {
        "url": "https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js",
        "integrity": "sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo",
        "crossorigin": "anonymous",
    },
    "javascript_in_head": False,
    "include_jquery": False,
    "use_i18n": False,
    "horizontal_label_class": "col-md-3",
    "horizontal_field_class": "col-md-9",
    "set_placeholder": True,
    "required_css_class": "",
    "error_css_class": "is-invalid",
    "success_css_class": "is-valid",
    "formset_renderers": {"default": "bootstrap4.renderers.FormsetRenderer"},
    "form_renderers": {"default": "bootstrap4.renderers.FormRenderer"},
    "field_renderers": {
        "default": "bootstrap4.renderers.FieldRenderer",
        "inline": "bootstrap4.renderers.InlineFieldRenderer",
    },
}


def get_bootstrap_setting(name, default=None):
    """Read a setting."""
    # Start with a copy of default settings
    BOOTSTRAP4 = BOOTSTRAP4_DEFAULTS.copy()

    # Override with user settings from settings.py
    BOOTSTRAP4.update(getattr(settings, "BOOTSTRAP4", {}))

    # Update use_i18n
    BOOTSTRAP4["use_i18n"] = i18n_enabled()

    return BOOTSTRAP4.get(name, default)


def jquery_url():
    """Return the full url to jQuery library file to use."""
    return get_bootstrap_setting("jquery_url")


def jquery_slim_url():
    """Return the full url to slim jQuery library file to use."""
    return get_bootstrap_setting("jquery_slim_url")


def include_jquery():
    """
    Return whether to include jquery.

    Setting could be False, True|'full', or 'slim'
    """
    return get_bootstrap_setting("include_jquery")


def popper_url():
    """Return the full url to Popper file."""
    return get_bootstrap_setting("popper_url")


def javascript_url():
    """Return the full url to the Bootstrap JavaScript file."""
    return get_bootstrap_setting("javascript_url")


def css_url():
    """Return the full url to the Bootstrap CSS file."""
    return get_bootstrap_setting("css_url")


def theme_url():
    """Return the full url to the theme CSS file."""
    return get_bootstrap_setting("theme_url")


def i18n_enabled():
    """Return the projects i18n setting."""
    return getattr(settings, "USE_I18N", False)


def get_renderer(renderers, **kwargs):
    layout = kwargs.get("layout", "")
    path = renderers.get(layout, renderers["default"])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting("formset_renderers")
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting("form_renderers")
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting("field_renderers")
    return get_renderer(renderers, **kwargs)
