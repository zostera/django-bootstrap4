from django.test import TestCase
from django.utils.safestring import mark_safe
from django_bootstrap5.components import render_alert, render_button


class AlertsTestCase(TestCase):
    def test_render_alert_without_type(self):
        self.assertEqual(
            render_alert("content"),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                "content"
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                "</div>"
            ),
        )

    def test_render_alert_with_type(self):
        self.assertEqual(
            render_alert("content", alert_type="danger"),
            (
                '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
                "content"
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                "</div>"
            ),
        )

    def test_render_alert_with_safe_content(self):
        self.assertEqual(
            render_alert(mark_safe('This is <a href="https://example.com" class="alert-link">a safe link</a>!')),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                'This is <a href="https://example.com" class="alert-link">a safe link</a>!'
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                "</div>"
            ),
        )

    def test_render_alert_with_unsafe_content(self):
        self.assertEqual(
            render_alert("This is <b>unsafe</b>!"),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                "This is &lt;b&gt;unsafe&lt;/b&gt;!"
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                "</div>"
            ),
        )


class ButtonsTestCase(TestCase):
    def test_button(self):
        self.assertEqual(render_button("button"), '<button class="btn btn-primary">button</button>')

    def test_button_with_illegal_type(self):
        try:
            self.assertEqual(
                render_button("button", button_type="illegal"), '<button class="btn btn-primary">button</button>'
            )
        except ValueError as e:
            self.assertEqual(
                str(e),
                'Parameter "button_type" should be "submit", "reset", "button", "link" or empty ("illegal" given).',
            )
