.. :changelog:

History
-------

Development
+++++++++++


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
