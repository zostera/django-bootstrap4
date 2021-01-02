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
            "href": "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
            "integrity": "sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2",
            "crossorigin": "anonymous",
        },

        # The complete URL to the Bootstrap JavaScript file
        "javascript_url": {
            "url": "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.min.js",
            "integrity": "sha384-w1Q4orYjBQndcko6MimVbzY0tgp4pWB4lZ7lr30WKz0vr/aWKhXdBNmNb5D92v7s",
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

        # The URL to the Popper.js JavaScript file (slim)
        "popper_url": {
            "url": "https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js",
            "integrity": "sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN",
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
