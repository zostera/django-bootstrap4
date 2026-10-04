from django.contrib.messages import constants as message_constants
from django.forms import formset_factory
from django.template import Context, Template
from django.test import TestCase

from bootstrap4.templatetags.bootstrap4 import bootstrap_message_classes, bootstrap_messages

from .forms import TestForm


def render(template, context=None):
    return Template("{% load bootstrap4 %}" + template).render(Context(context or {}))


class MessageClassesTest(TestCase):
    """`bootstrap_message_classes` tolerates objects that are not Django messages."""

    class PlainMessage:
        def __init__(self, level=None, extra_tags=None):
            if level is not None:
                self.level = level
            if extra_tags is not None:
                self.extra_tags = extra_tags

    def test_a_message_with_a_level(self):
        self.assertIn("alert-danger", bootstrap_message_classes(self.PlainMessage(level=message_constants.ERROR)))

    def test_an_unknown_level_falls_back_to_danger(self):
        self.assertIn("alert-danger", bootstrap_message_classes(self.PlainMessage(level=-1)))

    def test_an_object_without_extra_tags(self):
        """Anything without the attribute is treated as having none."""
        self.assertIsInstance(bootstrap_message_classes(self.PlainMessage(level=message_constants.INFO)), str)

    def test_extra_tags_are_kept(self):
        classes = bootstrap_message_classes(self.PlainMessage(level=message_constants.INFO, extra_tags="mine"))
        self.assertIn("mine", classes)

    def test_an_object_without_a_level(self):
        self.assertIsInstance(bootstrap_message_classes(self.PlainMessage(extra_tags="mine")), str)


class UrlTagTest(TestCase):
    """The tags that return a configured URL."""

    def test_jquery_url(self):
        self.assertIn("jquery", render("{% bootstrap_jquery_url %}").lower())

    def test_jquery_slim_url(self):
        self.assertIn("jquery", render("{% bootstrap_jquery_slim_url %}").lower())


class CssAndJavascriptTagTest(TestCase):
    """The asset tags react to the configured URLs."""

    def test_css_without_a_theme(self):
        with self.settings(BOOTSTRAP4={"theme_url": None}):
            self.assertEqual(render("{% bootstrap_css %}").count("<link"), 1)

    def test_css_without_a_css_url(self):
        with self.settings(BOOTSTRAP4={"css_url": None, "theme_url": None}):
            self.assertEqual(render("{% bootstrap_css %}").strip(), "")

    def test_javascript_with_no_javascript_url_configured(self):
        with self.settings(BOOTSTRAP4={"javascript_url": None}):
            self.assertEqual(render("{% bootstrap_javascript %}").strip(), "")


class ErrorTagTest(TestCase):
    """The standalone error tags."""

    def test_form_errors_tag(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIsInstance(render("{% bootstrap_form_errors form %}", {"form": form}), str)

    def test_formset_errors_tag(self):
        formset_class = formset_factory(TestForm, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertIsInstance(render("{% bootstrap_formset_errors formset %}", {"formset": formset}), str)


class ButtonsTagTest(TestCase):
    def test_a_reset_button(self):
        html = render("{% buttons reset='Reset' %}{% endbuttons %}")
        self.assertIn('type="reset"', html)
        self.assertIn("Reset", html)


class MessagesTagTest(TestCase):
    """`bootstrap_messages` accepts a plain dict as well as a Context."""

    def test_with_a_plain_dict(self):
        self.assertIsInstance(bootstrap_messages({"messages": []}), str)

    def test_through_a_template(self):
        self.assertIsInstance(render("{% bootstrap_messages %}"), str)
