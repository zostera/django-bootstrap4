from django.test import TestCase

from bootstrap4.bootstrap import get_bootstrap_setting


class SettingsTest(TestCase):
    def test_settings(self):
        self.assertIsNone(get_bootstrap_setting('SETTING_DOES_NOT_EXIST'))
        self.assertEqual('not none', get_bootstrap_setting('SETTING_DOES_NOT_EXIST', 'not none'))
        # Override a setting
        with self.settings(BOOTSTRAP4={'SETTING_DOES_NOT_EXIST': 'exists now'}):
            self.assertEqual(get_bootstrap_setting('SETTING_DOES_NOT_EXIST'), 'exists now')
