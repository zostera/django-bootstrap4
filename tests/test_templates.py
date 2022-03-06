from django.test import TestCase

from .utils import render_template, render_template_with_form


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template_with_form("")
        self.assertEqual(res.strip(), "")

    def test_text_template(self):
        res = render_template_with_form("some text")
        self.assertEqual(res.strip(), "some text")

    def test_bootstrap4_html_template_title(self):
        res = render_template(
            '{% extends "bootstrap4/bootstrap4.html" %}'
            + "{% block bootstrap4_title %}"
            + "test_bootstrap4_title"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap4_title", res)

    def test_bootstrap4_html_template_content(self):
        res = render_template(
            '{% extends "bootstrap4/bootstrap4.html" %}'
            + "{% block bootstrap4_content %}"
            + "test_bootstrap4_content"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap4_content", res)
