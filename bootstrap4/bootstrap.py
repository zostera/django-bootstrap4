# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings

# Default settings

BOOTSTRAP4_DEFAULTS = {
    'base_url': None,  # '//maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/'
    'css_url': {
        'href': "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css",
        'integrity': "sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ",
        'crossorigin': "anonymous",
    },
    'theme_url': None,
    'jquery_url': {
        'url': 'https://code.jquery.com/jquery-3.1.1.slim.min.js',
        'integrity': 'sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n',
        'crossorigin': 'anonymous',
    },
    'tether_url': {
        'url': "https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js",
        'integrity': "sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb",
        'crossorigin': "anonymous",

    },
    'javascript_url': {
        'url': "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js",
        'integrity': "sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn",
        'crossorigin': "anonymous",
    },
    'javascript_in_head': False,
    'include_jquery': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',

    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'has-error',
    'success_css_class': 'has-success',
    'formset_renderers': {
        'default': 'bootstrap4.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap4.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap4.renderers.FieldRenderer',
        'inline': 'bootstrap4.renderers.InlineFieldRenderer',
    },
}


def get_bootstrap_setting(name, default=None):
    """
    Read a setting
    """
    # Start with a copy of default settings
    BOOTSTRAP4 = BOOTSTRAP4_DEFAULTS.copy()

    # Override with user settings from settings.py
    BOOTSTRAP4.update(getattr(settings, 'BOOTSTRAP4', {}))

    return BOOTSTRAP4.get(name, default)


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bootstrap_setting('base_url') + postfix


def jquery_url():
    """
    Return the full url to jQuery file to use
    """
    return get_bootstrap_setting('jquery_url')


def tether_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    return get_bootstrap_setting('tether_url')


def javascript_url():
    """
    Return the full url to the Bootstrap JavaScript file
    """
    url = get_bootstrap_setting('javascript_url')
    return url if url else bootstrap_url('js/bootstrap.min.js')


def css_url():
    """
    Return the full url to the Bootstrap CSS file
    """
    url = get_bootstrap_setting('css_url')
    return url if url else bootstrap_url('css/bootstrap.min.css')


def theme_url():
    """
    Return the full url to the theme CSS file
    """
    return get_bootstrap_setting('theme_url')


def get_renderer(renderers, **kwargs):
    layout = kwargs.get('layout', '')
    path = renderers.get(layout, renderers['default'])
    mod, cls = path.rsplit(".", 1)
    return getattr(import_module(mod), cls)


def get_formset_renderer(**kwargs):
    renderers = get_bootstrap_setting('formset_renderers')
    return get_renderer(renderers, **kwargs)


def get_form_renderer(**kwargs):
    renderers = get_bootstrap_setting('form_renderers')
    return get_renderer(renderers, **kwargs)


def get_field_renderer(**kwargs):
    renderers = get_bootstrap_setting('field_renderers')
    return get_renderer(renderers, **kwargs)
