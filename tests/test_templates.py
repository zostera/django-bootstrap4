from django.test import TestCase

from .utils import render_template, render_template_with_form


class TemplateTest(TestCase):
    def test_empty_template(self):
        self.assertEqual(render_template_with_form("").strip(), "")

    def test_text_template(self):
        self.assertEqual(render_template_with_form("some text").strip(), "some text")

    def test_bootstrap4_html_template_title(self):
        self.assertIn(
            "test_bootstrap4_title",
            render_template(
                (
                    '{% extends "django_bootstrap4/bootstrap4.html" %}'
                    "{% block bootstrap4_title %}"
                    "test_bootstrap4_title"
                    "{% endblock %}"
                )
            ),
        )

    def test_bootstrap4_html_template_content(self):
        self.assertIn(
            "test_bootstrap4_content",
            render_template(
                (
                    '{% extends "django_bootstrap4/bootstrap4.html" %}'
                    "{% block bootstrap4_content %}"
                    "test_bootstrap4_content"
                    "{% endblock %}"
                )
            ),
        )
