from django.test import TestCase
from django.utils.safestring import mark_safe

from bootstrap4.components import render_alert


class AlertsTest(TestCase):
    def test_render_alert_without_type(self):
        self.assertEqual(
            render_alert("content"),
            (
                '<div class="alert alert-info alert-dismissible" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>content'
                "</div>"
            ),
        )

    def test_render_alert_with_type(self):
        self.assertEqual(
            render_alert("content", alert_type="danger"),
            (
                '<div class="alert alert-danger alert-dismissible" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                "content"
                "</div>"
            ),
        )

    def test_render_alert_with_safe_content(self):
        self.assertEqual(
            render_alert(mark_safe('This is <a href="https://example.com" class="alert-link">a safe link</a>!')),
            (
                '<div class="alert alert-info alert-dismissible" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                'This is <a href="https://example.com" class="alert-link">a safe link</a>!'
                "</div>"
            ),
        )

    def test_render_alert_with_unsafe_content(self):
        self.assertEqual(
            render_alert("This is <b>unsafe</b>!"),
            (
                '<div class="alert alert-info alert-dismissible" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                "This is &lt;b&gt;unsafe&lt;/b&gt;!"
                "</div>"
            ),
        )
