========
Settings
========

The django-bootstrap4 has some pre-configured settings.

They can be modified by adding a dict variable called ``BOOTSTRAP4`` in your ``settings.py`` and customizing the values ​​you want;

The ``BOOTSTRAP4`` dict variable contains these settings and defaults:


.. code:: django

    # Default settings
    BOOTSTRAP4 = {

        # The complete URL to the Bootstrap CSS file
        # Note that a URL can be either a string,
        # e.g. "https://stackpath.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css",
        # or a dict like the default value below.
        "css_url": {
            "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/css/bootstrap.min.css",
            "integrity": "sha384-zCbKRCUGaJDkqS1kPbPd7TveP5iyJE0EjAuZQTgFLD2ylzuqKfdKlfG/eSrtxUkn",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap bundle JavaScript file
        "javascript_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.6.1/dist/js/bootstrap.bundle.min.js",
            "integrity": "sha384-fQybjgWLrvvRgtW6bFlB7jaZrFsaBXjsOMm/tB9LTS58ONXgqbR9W8oWht/amnpF",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap CSS theme file (None means no theme)
        "theme_url": None,

        # The URL to the jQuery JavaScript file (full)
        "jquery_url": {
            "url": "https://code.jquery.com/jquery-3.5.1.min.js",
            "integrity": "sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2",
            "crossorigin": "anonymous",
        },

        # The URL to the jQuery JavaScript file (slim)
        "jquery_slim_url": {
            "url": "https://code.jquery.com/jquery-3.5.1.slim.min.js",
            "integrity": "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj",
            "crossorigin": "anonymous",
        },

        # Put JavaScript in the HEAD section of the HTML document (only relevant if you use bootstrap4.html)
        'javascript_in_head': False,

        # Include jQuery with Bootstrap JavaScript False|falsy|slim|full (default=False)
        # False - means tag bootstrap_javascript use default value - `falsy` and does not include jQuery)
        'include_jquery': False,

        # Label class to use in horizontal forms
        'horizontal_label_class': 'col-md-3',

        # Field class to use in horizontal forms
        'horizontal_field_class': 'col-md-9',

        # Set placeholder attributes to label if no placeholder is provided
        'set_placeholder': True,

        # Class to indicate required (better to set this in your Django form)
        'required_css_class': '',

        # Class to indicate error (better to set this in your Django form)
        'error_css_class': 'is-invalid',

        # Class to indicate success, meaning the field has valid input (better to set this in your Django form)
        'success_css_class': 'is-valid',

        # Renderers (only set these if you have studied the source and understand the inner workings)
        'formset_renderers':{
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

Unused settings
---------------

A key in ``BOOTSTRAP4`` that this package does not read is ignored. That is a problem
when a setting used to exist and was removed: the key goes on looking effective while
doing nothing.

A system check reports those keys, so they show up in ``manage.py check``, in
``runserver`` and in CI:

.. code:: text

    ?: (bootstrap4.W001) BOOTSTRAP4['base_url'] has no effect: dropped in 0.0.8,
    use `css_url` and `javascript_url`.

If you deliberately keep extra keys in the dict, silence it with::

    SILENCED_SYSTEM_CHECKS = ["bootstrap4.W001"]

``use_i18n`` fails in a different way and the check cannot report it. It is a real key,
so it is accepted, but ``get_bootstrap_setting`` overwrites it with Django's own
``USE_I18N`` on every read. Setting it in ``BOOTSTRAP4`` has no effect either. Set
``USE_I18N`` instead.

Validation classes on bound forms
---------------------------------

``success_css_class`` defaults to ``is-valid``, and it is applied to every field of a
bound form that has no errors. A form is bound as soon as it is given data, so a GET
filter form rendered straight after a page load shows a green tick on every field,
before the user has entered anything.

That is the intended default, and Bootstrap 4 itself
`advises against server side validation state <https://getbootstrap.com/docs/4.6/components/forms/#validation>`_.
Turn it off per tag::

    {% bootstrap_form filter.form bound_css_class='' %}

Or project wide::

    BOOTSTRAP4 = {
        'success_css_class': '',
    }

``bound_css_class`` is the template tag parameter, ``success_css_class`` the setting it
reads. The same applies to ``error_css_class``, which defaults to ``is-invalid``.
