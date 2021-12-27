# Changelog

## 21.2 (2021-12-27)

- Drop support for Django 4 (#398).
- Drop support for Django 3.1 (EOL, #399).
- Drop support for Python 3.6 (EOL, #399).
- Fix CI.

## 21.1 (2021-11-03)

- Switch to a [CalVer](https://calver.org) YY.MINOR versioning scheme. MINOR is the number of the release in the given year. This is the first release in 2021 using this scheme, so its version is 21.1. The next version this year will be 21.2. The first version in 2022 will be 22.1.
- Add support for Django 4.0 and Python 3.10 (#349).
- Fix faulty example code (#347).

## 3.0.1 (2021-05-01)

- No line break in FileInput in horizontal layout.
- Actually use the bundles JavaScript.

## 3.0.0 (2021-04-09)

- Drop support for Django 3.0, extended support stopped on 2021-04-01).
- Add support for Django 3.2.
- Use bundled Bootstrap JavaScript, no need for separate popper.js. 
- Updated default Bootstrap to 4.6.0.
- Add Dependabot for updates to dependencies.
- Rename AUTHORS.md to AUTHORS, remove authors section from documentation.
- Revert to setuptools for packaging.
- Add Python 3.9 to Travis CI.
- Add docs and tests to sdist.
- Use GitHub Actions for CI.
- Fix example by not installing editable version.

## 2.3.1 (2020-10-16)

- Fix CHANGELOG.

## 2.3.0 (2020-10-11)

- Updated default Bootstrap to 4.5.2.
- Updated CSS/JavaScript URLs to newer versions (thanks @emmceemoore).
- Replace `m2r` with `m2r2` to support Sphinx3.
- Update Sphinx dependency because of security update.
- Use Django 3.1 in `tox` matrix, fix warning in tests.
- Add `tox` to development dependencies.
- Accept importlib-metadata 2.x.x (thanks @dbaty).
- Add Python 3.9 to tox matrix.

## 2.2.0 (2020-07-01)

- Fix coveralls.
- Add Django 3.1 to tox matrix.

## 2.1.1 (2020-06-18)

- Fix date in CHANGELOG.
- Fix typo in pyproject.toml (#222).

## 2.1.0 (2020-06-17)

- Convert HISTORY.rst to Markdown and rename to CHANGELOG.md.
- Convert README.rst, AUTHORS.rst and CONTRIBUTING.rst to Markdown, and change extension to .md.
- Update CONTRIBUTING.md to reflect use of `poetry`.
- Drop contributing.rst from documentation.
- Rename default branch 'master' to 'main'.

## 2.0.1 (2020-06-02)

- Set beautifulsoup4 requirement to \>= 4.8.0 (fixes #216).
- Do not assume all inputs are inside labels (fixes #215).

## 2.0.0 (2020-06-01)

- Use poetry (<https://python-poetry.org/>) for dependency management and packaging.
- Drop support for Python 3.5.
- Fix form-check-{label,input} classes applied too broadly. These should only be applied to labels and inputs found underneath the enclosing widget div for radio and checkbox select, not on the whole document.
- Allow to display radio and checkbox elements inline using the `form-check` classes.

## 1.1.2 (2019-12-13)

- Restructure tox and Makefile.
- Add test for `bootstrap4.__version__`.

## 1.1.1 (2019-12-11)

- Remove tag command from Makefile.
- Reinstate `bootstrap4.__version__` (#186).
- Add test for using a different jQuery version (#184).

## 1.1.0 (2019-12-09)

- Update default Bootstrap to v4.3.1.
- Add support for Python 3.8, Django 3 and Django master.
- Switch to Django `manage.py` for test running.
- Update Makefile commands.
- Update tox configuration.
- Use correct license (BSD-3-Clause).
- Fix typo's in docstrings.
- Update Travis configuration.
- Drop MANIFEST.in, use `setuptools_scm`.
- Stop using `_version.py`, use git tags for versioning.
- Fixed issues with labels and input (#174 and #181).

## 1.0.1 (2019-08-30)

- Fix support for Python 3.5 (#168).
- Set correct Python versions in setup.py.
- Fix `make test` command.

## 1.0.0 (2019-08-30)

- Set default class for buttons to `btn-primary` (#150.
- Drop support for Python 2 and Django 1.11, 2.0 and 2.1 (#155).
- Template tag `bootstrap_field` now allows 3 values for `show_label`: `True`, `False`, `sr-only` and `skip\`. In the case of `False` / `sr-only` the label is hidden but present for screen readers. When `show_label` is set to `skip`, the label is not generated at all.
- Fix validation on input groups (#122).
- No longer duplicate jquery in bootstrap4.html (#139, #140).
- Apply `form-check`, `form-check-label` and `form-check-input` classes to appropriate tags for `RadioSelect` and `CheckboxSelectMultiple` widgets (#141).
- Errors on file inputs are shown (#146).
- Only display non-field errors in form alert block (#161).
- Reinstate `bootstrap4_title` block to `bootstrap4.html` (#156).
- Fix typo in `alert-dismissible` class (#142).
- Honor the `form_group_class` parameter in the `buttons` tag (#162).

## 0.0.8 (2019-03-12)

- Drop support for the `base_url` setting (#105).
- Remove use of \"falsy\" as a string literal (#111).
- Fix javascript inclusion bugs (#71).
- Allow email to have addons (#131).
- Do not mark placeholder text as safe (#135).

## 0.0.7 (2018-08-22)

- Improve alert accessibility (#93.
- Add a new widget: RadioSelectButtonGroup (#103.
- Several fixes and improvements to HTML renderin.
- Switch to explicit Travis test.
- Upgrade Bootstrap to 4.1.1
- Upgrade jQuery to 3.3.1
- Upgrade Popper to 1.14.3
- Fixed `bootstrap4.html` to add jQuery per setting `include_jquery=[False|'full'|'slim']`.
- Adopt Black formatting, see <https://github.com/ambv/black>.

## 0.0.6 (2018-02-14)

- Change form help text element from div to small (#60).
- Upgrade Bootstrap to 4.0.0 (#66).

## 0.0.5 (2018-01-03)

- Drop develop branch, work with master and feature branche.
- Clean up `HISTORY.rst`.
- Upgrade Bootstrap to 4.0.0-beta.3.
- Use `col-4` rather than `col-xs-4` (#54).
- Added pagination alignment options (#56).
- Fixed form field errors and help texts (#39.
- Use django language if `USE_I18N=True` (#53).

## 0.0.4 (2017-10-26)

- Upgrade Bootstrap to 4.0.0-beta.2.
- Fix settings, tags and tests for remote JS and CSS.

## 0.0.3 (2017-09-24)

- Upgraded bootstrap4 to the beta version.

## [0.0.2] - (2017-09-06, not released on PyPI)

- Upgraded jQuery version from CDN to 3.2.1 (#17).
- Added proper pagination layout classes (#19).

## 0.0.1 (2017-06-04)

- First releas.
- Remove `bootstrap_icon`, BS4 no longer has default icons.
- Various changes to get from 3 to 4, started MIGRATE.rst.
- Started `django-bootstrap4` based on `django-bootstrap3`.
- Thanks everybody that contributed to `django-bootstrap3`!
