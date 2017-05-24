======================
Bootstrap 4 for Django
======================

Write Django as usual, and let ``django-bootstrap4`` make template output into Bootstrap 4 code.


.. image:: https://img.shields.io/travis/zostera/django-bootstrap4/master.svg
    :target: https://travis-ci.org/dyve/django-bootstrap4

.. image:: https://img.shields.io/coveralls/dzostera/django-bootstrap4/master.svg
  :target: https://coveralls.io/r/dyve/django-bootstrap4?branch=master

.. image:: https://img.shields.io/pypi/v/django-bootstrap4.svg
    :target: https://pypi.python.org/pypi/django-bootstrap4
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-bootstrap4.svg
    :target: https://pypi.python.org/pypi/django-bootstrap4
    :alt: Number of PyPI downloads per month


Requirements
------------

- Django >= 1.11 (and compatible Python version)


Installation
------------

1. Install using pip:

   ``pip install django-bootstrap4``

   Alternatively, you can install download or clone this repo and call ``pip install -e .``.

2. Add to INSTALLED_APPS in your ``settings.py``:

   ``'bootstrap4',``

3. In your templates, load the ``bootstrap4`` library and use the ``bootstrap_*`` tags:

This app will soon require Django 1.8+, python 2.7+. Thanks for understanding.


Example template
----------------

   .. code:: Django

    {% load bootstrap4 %}

    {# Display a form #}

    <form action="/url/to/submit/" method="post" class="form">
        {% csrf_token %}
        {% bootstrap_form form %}
        {% buttons %}
            <button type="submit" class="btn btn-primary">Submit</button>
        {% endbuttons %}
    </form>


Documentation
-------------

The full documentation is at http://django-bootstrap4.readthedocs.org/.


Bugs and suggestions
--------------------

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/zostera/django-bootstrap4/issues


License
-------

You can use this under BSD-3-Clause. See `LICENSE
<LICENSE>`_ file for details.


Author
------

Developed and maintained by `Zostera <https://zostera.nl/>`_.

Original author & Development lead: `Dylan Verheul <https://github.com/dyve>`_.

Thanks to everybody that has contributed pull requests, ideas, issues, comments and kind words.

Please see AUTHORS.rst for a list of contributors.
