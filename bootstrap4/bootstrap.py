# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings

# Default settings

BOOTSTRAP4_DEFAULTS = {
    'base_url': None,  # 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/'
    'css_url': {
        'href': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css',
        'integrity': 'sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm',
        'crossorigin': 'anonymous',
    },
    'theme_url': None,
    'jquery_url': {
        'url': 'https://code.jquery.com/jquery-3.2.1.min.js',
        'integrity': 'sha384-xBuQ/xzmlsLoJpyjoggmTEz8OWUFM0/RC5BsqQBDX2v5cMvDHcMakNTNrHIW2I5f',
        'crossorigin': 'anonymous',
    },
    'jquery_slim_url': {
        'url': 'https://code.jquery.com/jquery-3.2.1.slim.min.js',
        'integrity': 'sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN',
        'crossorigin': 'anonymous',
    },
    'popper_url': {
        'url': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
        'integrity': 'sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q',
        'crossorigin': 'anonymous',
    },
    'javascript_url': {
        'url': 'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js',
        'integrity': 'sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl',
        'crossorigin': 'anonymous',
    },
    'javascript_in_head': False,
    'include_jquery': False,
    'use_i18n': False,
    'horizontal_label_class': 'col-md-3',
    'horizontal_field_class': 'col-md-9',

    'set_placeholder': True,
    'required_css_class': '',
    'error_css_class': 'is-invalid',
    'success_css_class': 'is-valid',
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

    # Update use_i18n
    BOOTSTRAP4['use_i18n'] = i18n_enabled()

    return BOOTSTRAP4.get(name, default)


def bootstrap_url(postfix):
    """
    Prefix a relative url with the bootstrap base url
    """
    return get_bootstrap_setting('base_url') + postfix


def jquery_url():
    """
    Return the full url to jQuery library file to use
    """
    return get_bootstrap_setting('jquery_url')


def jquery_slim_url():
    """
    Return the full url to slim jQuery library file to use
    """
    return get_bootstrap_setting('jquery_slim_url')


def popper_url():
    """
    Return the full url to Popper file
    """
    return get_bootstrap_setting('popper_url')


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


def i18n_enabled():
    """
    Return the projects i18n setting
    """
    return getattr(settings, 'USE_I18N', False)


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
