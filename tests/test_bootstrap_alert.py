from django.utils.safestring import mark_safe

from django_bootstrap4.components import render_alert

from .base import BootstrapTestCase


class BootstrapAlertTestCase(BootstrapTestCase):
    def test_bootstrap_alert(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "content" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">content</div>',
        )

    def test_bootstrap_alert_type_invalid(self):
        with self.assertRaises(ValueError):
            self.render('{% bootstrap_alert "content" alert_type="nope" %}')

    def test_bootstrap_alert_dismissible(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "content" %}'),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>content'
                "</div>"
            ),
        )

    def test_bootstrap_alert_html_content(self):
        self.assertEqual(
            self.render('{% bootstrap_alert "foo<br>bar" dismissible=False %}'),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )
        self.assertEqual(
            self.render("{% bootstrap_alert value dismissible=False %}", context={"value": "foo<br>bar"}),
            '<div class="alert alert-info" role="alert">foo&lt;br&gt;bar</div>',
        )
        self.assertEqual(
            self.render("{% bootstrap_alert value|safe dismissible=False %}", context={"value": "foo<br>bar"}),
            '<div class="alert alert-info" role="alert">foo<br>bar</div>',
        )

    def test_render_alert_without_type(self):
        self.assertEqual(
            render_alert("content"),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>content'
                "</div>"
            ),
        )

    def test_render_alert_with_type(self):
        self.assertEqual(
            render_alert("content", alert_type="danger"),
            (
                '<div class="alert alert-danger alert-dismissible fade show" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                "content"
                "</div>"
            ),
        )

    def test_render_alert_with_safe_content(self):
        self.assertEqual(
            render_alert(mark_safe('This is <a href="https://example.com" class="alert-link">a safe link</a>!')),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                'This is <a href="https://example.com" class="alert-link">a safe link</a>!'
                "</div>"
            ),
        )

    def test_render_alert_with_unsafe_content(self):
        self.assertEqual(
            render_alert("This is <b>unsafe</b>!"),
            (
                '<div class="alert alert-info alert-dismissible fade show" role="alert">'
                '<button type="button" class="close" data-dismiss="alert" aria-label="close">&times;</button>'
                "This is &lt;b&gt;unsafe&lt;/b&gt;!"
                "</div>"
            ),
        )
