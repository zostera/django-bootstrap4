from django.core.checks import Warning, registry
from django.test import SimpleTestCase

from bootstrap4.apps import check_bootstrap4_settings
from bootstrap4.bootstrap import get_bootstrap_setting


class CheckBootstrap4SettingsTestCase(SimpleTestCase):
    def test_registered(self):
        """The check runs as part of manage.py check."""
        self.assertIn(check_bootstrap4_settings, registry.registry.get_checks())

    def test_known_settings_are_silent(self):
        with self.settings(BOOTSTRAP4={"include_jquery": True, "horizontal_label_class": "col-md-4"}):
            self.assertEqual(check_bootstrap4_settings(None), [])

    def test_empty_settings_are_silent(self):
        with self.settings(BOOTSTRAP4={}):
            self.assertEqual(check_bootstrap4_settings(None), [])

    def test_every_default_is_accepted(self):
        """No default key warns about itself."""
        from bootstrap4.bootstrap import BOOTSTRAP4_DEFAULTS

        with self.settings(BOOTSTRAP4=dict(BOOTSTRAP4_DEFAULTS)):
            self.assertEqual(check_bootstrap4_settings(None), [])

    def test_unknown_key_warns(self):
        with self.settings(BOOTSTRAP4={"no_such_setting": "value"}):
            warnings = check_bootstrap4_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0], Warning)
        self.assertEqual(warnings[0].id, "bootstrap4.W001")
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP4['no_such_setting'] has no effect: not a django-bootstrap4 setting; it is ignored.",
        )

    def test_removed_setting_warns_with_its_own_hint(self):
        with self.settings(BOOTSTRAP4={"base_url": "/static/bootstrap/"}):
            warnings = check_bootstrap4_settings(None)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(
            warnings[0].msg,
            "BOOTSTRAP4['base_url'] has no effect: dropped in 0.0.8, use `css_url` and `javascript_url`.",
        )

    def test_one_warning_per_unknown_key(self):
        with self.settings(BOOTSTRAP4={"theme_url": "/theme.css", "base_url": "/static/", "nope": 1}):
            warnings = check_bootstrap4_settings(None)
        self.assertEqual(len(warnings), 2)
        self.assertIn("base_url", warnings[0].msg)
        self.assertIn("nope", warnings[1].msg)

    def test_use_i18n_is_not_reported_but_is_overwritten(self):
        """use_i18n is a real key, so it is silent here, but the user's value never survives."""
        with self.settings(BOOTSTRAP4={"use_i18n": True}, USE_I18N=False):
            self.assertEqual(check_bootstrap4_settings(None), [])
            self.assertFalse(get_bootstrap_setting("use_i18n"))
