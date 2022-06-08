from django.test import TestCase, override_settings

from bootstrap4.bootstrap import get_bootstrap_setting

from .forms import TestForm
from .utils import render_template_with_form


class MediaTest(TestCase):
    def expected_css(self, tag):
        template = '<link href="{href}" integrity="{integrity}" crossorigin="{crossorigin}" rel="stylesheet">'
        setting = get_bootstrap_setting(tag + "_url")
        return template.format(**setting)

    def expected_js(self, tag):
        template = '<script src="{url}" integrity="{integrity}" crossorigin="{crossorigin}"></script>'
        setting = get_bootstrap_setting(tag + "_url")
        return template.format(**setting)

    def test_bootstrap_jquery(self):
        self.assertHTMLEqual(render_template_with_form("{% bootstrap_jquery %}"), self.expected_js("jquery"))
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery jquery=True %}"), self.expected_js("jquery")
        )
        self.assertHTMLEqual(
            render_template_with_form('{% bootstrap_jquery jquery="full" %}'), self.expected_js("jquery")
        )
        self.assertHTMLEqual(
            render_template_with_form('{% bootstrap_jquery jquery="slim" %}'), self.expected_js("jquery_slim")
        )
        self.assertHTMLEqual(render_template_with_form("{% bootstrap_jquery jquery=False %}"), "")

    @override_settings(BOOTSTRAP4={"jquery_url": {"url": "foo"}})
    def test_bootstrap_jquery_custom_setting_dict(self):
        self.assertHTMLEqual(render_template_with_form("{% bootstrap_jquery %}"), '<script src="foo"></script>')

    @override_settings(BOOTSTRAP4={"jquery_url": "http://example.com"})
    def test_bootstrap_jquery_custom_setting_str(self):
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery %}"), '<script src="http://example.com"></script>'
        )

    def test_bootstrap_javascript_tag(self):
        html = render_template_with_form("{% bootstrap_javascript jquery=True %}")
        # jQuery
        self.assertInHTML(self.expected_js("jquery"), html)
        # Bootstrap
        self.assertInHTML(self.expected_js("javascript"), html)

    def test_bootstrap_css_tag(self):
        html = render_template_with_form("{% bootstrap_css %}").strip()
        self.assertInHTML(self.expected_css("css"), html)
        # Theme
        self.assertInHTML('<link rel="stylesheet" href="//example.com/theme.css">', html)

    def test_bootstrap_setting_filter(self):
        res = render_template_with_form('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), "bootstrap4-req")
        res = render_template_with_form('{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}')
        self.assertEqual(res.strip(), "head")

    def test_bootstrap_required_class(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-req", res)

    def test_bootstrap_error_class(self):
        form = TestForm({})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-err", res)

    def test_bootstrap_bound_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-bound", res)


class JavaScriptTagTest(TestCase):
    def test_bootstrap_javascript_without_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript %}")
        self.assertIn("bootstrap", res)
        self.assertNotIn("jquery", res)

    def test_bootstrap_javascript_with_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=True %}")
        self.assertIn("bootstrap", res)
        self.assertIn("jquery", res)
