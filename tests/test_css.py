from django.test import TestCase

from django_bootstrap4.css import merge_css_classes


class MergeCssClassesTestCase(TestCase):
    def test_merge(self):
        css_classes = "one two"
        css_class = "three four"

        classes = merge_css_classes(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = merge_css_classes(css_class, css_classes)
        self.assertEqual(classes, "three four one two")

    def test_merge_no_parameters(self):
        self.assertEqual(merge_css_classes(), "")

    def test_merge_empty_parameters(self):
        self.assertEqual(merge_css_classes("", None), "")
        self.assertEqual(merge_css_classes("", "foo", "bar", None), "foo bar")

    def test_merge_non_string_parameters(self):
        self.assertEqual(merge_css_classes("", False), "False")
