from django.test import TestCase
from django.utils.safestring import mark_safe

from bootstrap4.components import render_alert
from bootstrap4.exceptions import BootstrapError
from bootstrap4.forms import render_button


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


class ButtonsTest(TestCase):
    def test_button(self):
        self.assertEqual(render_button("button"), '<button class="btn btn-primary">button</button>')

    def test_button_with_illegal_type(self):
        try:
            self.assertEqual(
                render_button("button", button_type="illegal"), '<button class="btn btn-primary">button</button>'
            )
        except BootstrapError as e:
            self.assertEqual(
                str(e),
                'Parameter "button_type" should be "submit", "reset", "button", "link" or empty ("illegal" given).',
            )
