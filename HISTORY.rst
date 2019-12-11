.. :changelog:

History
-------

1.1.1 (2019-12-11)
++++++++++++++++++
- Remove tag command from Makefile
- Reinstate `bootstrap4.__version__` (#186)
- Add test for using a different jQuery version (#184)

1.1.0 (2019-12-09)
++++++++++++++++++
- Update default Bootstrap to v4.3.1
- Add support for Python 3.8, Django 3 and Django master
- Switch to Django `manage.py` for test running
- Update Makefile commands
- Update tox configuration
- Use correct license (BSD-3-Clause)
- Fix typo's in docstrings
- Update Travis configuration
- Drop MANIFEST.in, use setuptools_scm
- Stop using _version.py, use git tags for versioning
- Fixed issues with labels and input (#174 and #181)

1.0.1 (2019-08-30)
++++++++++++++++++
- Fix support for Python 3.5 (#168)
- Set correct Python versions in setup.py
- Fix `make test` command

1.0.0 (2019-08-30)
++++++++++++++++++
- Set default class for buttons to `btn-primary` (#150)
- Drop support for Python 2 and Django 1.11, 2.0 and 2.1 (#155)
- Template tag `bootstrap_field` now allows 3 values for `show_label`: `True`, `False` / `'sr-only'` and `'skip'`. In the case of `False` / `'sr-only'` the label is hidden but present for screen readers. When `show_label` is set to `'skip'`, the label is not generated at all.
- Fix validation on input groups (#122)
- No longer duplicate jquery in bootstrap4.html (#139, #140)
- Apply `form-check`, `form-check-label` and `form-check-input` classes to appropriate tags for `RadioSelect` and `CheckboxSelectMultiple` widgets (#141)
- Errors on file inputs are shown (#146)
- Only display non-field errors in form alert block (#161)
- Reinstate `bootstrap4_title` block to `bootstrap4.html` (#156)
- Fix typo in `alert-dismissible` class (#142)
- Honor the `form_group_class` parameter in the `buttons` tag (#162)

0.0.8 (2019-03-12)
++++++++++++++++++
- Drop support for the `base_url` setting (#105)
- Remove use of "falsy" as a string literal (#111)
- Fix javascript inclusion bugs (#71)
- Allow email to have addons (#131)
- Do not mark placeholder text as safe (#135)
- Adopt black

0.0.7 (2018-08-22)
++++++++++++++++++
- Improve alert accessibility (#93)
- Add a new widget: RadioSelectButtonGroup (#103)
- Several fixes and improvements to HTML rendering
- Switch to explicit Travis tests
- Upgrade Bootstrap to 4.1.1
- Upgrade jQuery to 3.3.1
- Upgrade Popper to 1.14.3
- Fixed bootstrap4.html to add jQuery per setting 'include_jquery' [False|True|'full'|'slim']
- Adopt Black formatting, see https://github.com/ambv/black

0.0.6 (2018-02-14)
+++++++++++++++++++
- Change form help text element from div to small (#60)
- Upgrade Bootstrap to 4.0.0 (#66)

0.0.5 (2018-01-03)
++++++++++++++++++
- Drop develop branch, work with master and feature branches
- Clean up history file
- Upgrade Bootstrap to 4.0.0-beta.3
- Use `col-4` rather than `col-xs-4` (#54)
- Added pagination alignment options (#56)
- Fixed form field errors and help texts (#39)
- Use django language if ``USE_I18N=True`` (#53)

0.0.4 (2017-10-26)
++++++++++++++++++
- Upgrade Bootstrap to 4.0.0-beta.2
- Fix settings, tags and tests for remote JS and CSS

0.0.3 (2017-09-24)
++++++++++++++++++
- Upgraded bootstrap4 to the beta version

0.0.2 (2017-09-06, not released on PyPI)
++++++++++++++++++++++++++++++++++++++++
- Upgraded jQuery version from CDN to 3.2.1 (#17)
- Added proper pagination layout classes (#19)

0.0.1 (2017-06-04)
++++++++++++++++++
- First release

Unreleased (2017-04-25)
+++++++++++++++++++++++
- Remove `bootstrap_icon`, BS4 no longer has default icons.
- Various changes to get from 3 to 4, started MIGRATE.rst.
- Started `django-bootstrap4` based on `django-bootstrap3`.
- Thanks everybody that contributed to `django-bootstrap3`!
