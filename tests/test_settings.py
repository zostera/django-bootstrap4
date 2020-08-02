from django.test import TestCase, override_settings

from bootstrap4.bootstrap import get_bootstrap_setting, include_jquery, jquery_slim_url, jquery_url


class SettingsTest(TestCase):
    def test_get_bootstrap_setting(self):
        self.assertIsNone(get_bootstrap_setting("SETTING_DOES_NOT_EXIST"))
        self.assertEqual("not none", get_bootstrap_setting("SETTING_DOES_NOT_EXIST", "not none"))
        # Override a setting
        with self.settings(BOOTSTRAP4={"SETTING_DOES_NOT_EXIST": "exists now"}):
            self.assertEqual(get_bootstrap_setting("SETTING_DOES_NOT_EXIST"), "exists now")

    def test_jquery_url(self):
        self.assertEqual(
            jquery_url(),
            {
                "url": "https://code.jquery.com/jquery-3.5.1.min.js",
                "integrity": "sha384-ZvpUoO/+PpLXR1lu4jmpXWu80pZlYUAfxl5NsBMWOEPSjUn/6Z/hRTt8+pR6L4N2",
                "crossorigin": "anonymous",
            },
        )

    @override_settings(
        BOOTSTRAP4={
            "jquery_url": {
                "url": "https://example.com/jquery.js",
                "integrity": "we-want-a-different-jquery",
                "crossorigin": "anonymous",
            },
        }
    )
    def test_jquery_url_from_settings(self):
        self.assertEqual(
            jquery_url(),
            {
                "url": "https://example.com/jquery.js",
                "integrity": "we-want-a-different-jquery",
                "crossorigin": "anonymous",
            },
        )

    def test_jquery_slim_url(self):
        self.assertEqual(
            jquery_slim_url(),
            {
                "url": "https://code.jquery.com/jquery-3.5.1.slim.min.js",
                "integrity": "sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj",
                "crossorigin": "anonymous",
            },
        )

    def test_include_jquery(self):
        self.assertEqual(include_jquery(), False)
        with self.settings(BOOTSTRAP4={"include_jquery": False}):
            self.assertEqual(include_jquery(), False)
        with self.settings(BOOTSTRAP4={"include_jquery": True}):
            self.assertEqual(include_jquery(), True)
        with self.settings(BOOTSTRAP4={"include_jquery": "full"}):
            self.assertEqual(include_jquery(), "full")
        with self.settings(BOOTSTRAP4={"include_jquery": "slim"}):
            self.assertEqual(include_jquery(), "slim")
