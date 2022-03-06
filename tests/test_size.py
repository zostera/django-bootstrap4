from django.test import TestCase
from django_bootstrap5.size import get_size_class, parse_size


class SizeTestCase(TestCase):
    def test_parse_size(self):
        self.assertEqual(parse_size("sm"), "sm")
        self.assertEqual(parse_size("md"), "md")
        self.assertEqual(parse_size("lg"), "lg")
        with self.assertRaises(ValueError):
            self.assertEqual(parse_size("xl"), "xl")

    def test_parse_size_default_value(self):
        for empty_value in ["", None, False]:
            self.assertEqual(parse_size(empty_value, "sm"), "sm")
            self.assertEqual(parse_size(empty_value, "md"), "md")
            self.assertEqual(parse_size(empty_value, "lg"), "lg")
        with self.assertRaises(ValueError):
            self.assertEqual(parse_size("", "xl"), "xl")

    def test_get_size_class(self):
        self.assertEqual(get_size_class("sm", prefix="test"), "test-sm")
        self.assertEqual(get_size_class("", default="sm", prefix="test"), "test-sm")
        self.assertEqual(get_size_class("sm", prefix="test", skip="md"), "test-sm")
        self.assertEqual(get_size_class("sm", prefix="test", skip="sm"), "")
