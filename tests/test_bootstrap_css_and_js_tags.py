from django_bootstrap4.core import get_bootstrap_setting
from tests.base import BootstrapTestCase


class MediaTestCase(BootstrapTestCase):
    expected_bootstrap_css = (
        '<link href="{url}" integrity="{integrity}" crossorigin="{crossorigin}" rel="stylesheet">'.format(
            **get_bootstrap_setting("css_url")
        )
    )
    expected_bootstrap_js = '<script src="{url}" integrity="{integrity}" crossorigin="{crossorigin}"></script>'.format(
        **get_bootstrap_setting("javascript_url")
    )

    def test_bootstrap_javascript_tag(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_javascript %}"),
            self.expected_bootstrap_js,
        )
        with self.settings(BOOTSTRAP4={"javascript_url": "//example.com/bootstrap.js"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_javascript %}"),
                '<script src="//example.com/bootstrap.js">',
            )

    def test_bootstrap_css_tag(self):
        self.maxDiff = None
        self.assertHTMLEqual(
            self.render("{% bootstrap_css %}"),
            self.expected_bootstrap_css,
        )
        with self.settings(BOOTSTRAP4={"css_url": "//example.com/bootstrap.css"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_css %}"),
                '<link href="//example.com/bootstrap.css" rel="stylesheet">',
            )

    def test_bootstrap_css_tag_with_theme(self):
        with self.settings(BOOTSTRAP4={"theme_url": "//example.com/theme.css"}):
            self.assertHTMLEqual(
                self.render("{% bootstrap_css %}"),
                self.expected_bootstrap_css + '<link rel="stylesheet" href="//example.com/theme.css">',
            )

    def test_bootstrap_setting_filter(self):
        self.assertEqual(self.render('{{ "required_css_class"|bootstrap_setting }}'), "django_bootstrap4-req")
        self.assertEqual(
            self.render('{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}'), "head"
        )
