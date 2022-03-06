from django.test import TestCase

from django_bootstrap4.text import text_concat, text_value


class TextTestCase(TestCase):
    def test_text_value(self):
        self.assertEqual(text_value(""), "")
        self.assertEqual(text_value(" "), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator="="), "1=2")
        self.assertEqual(text_concat(None, 2, separator="="), "2")
