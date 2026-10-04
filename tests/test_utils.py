from django.template import Context, Template, TemplateSyntaxError, Variable
from django.test import TestCase

from bootstrap4.utils import handle_var, remove_css_class, render_link_tag


class HandleVarTest(TestCase):
    """`handle_var` resolves a template value to a Python one."""

    def test_a_quoted_string_is_unquoted(self):
        self.assertEqual(handle_var('"hello"', Context({})), "hello")
        self.assertEqual(handle_var("'hello'", Context({})), "hello")

    def test_a_variable_is_resolved_from_the_context(self):
        self.assertEqual(handle_var("name", Context({"name": "value"})), "value")

    def test_an_unresolvable_variable_falls_back_to_the_string(self):
        self.assertEqual(handle_var("missing", Context({})), "missing")

    def test_a_template_variable_object_is_resolved(self):
        self.assertEqual(handle_var(Variable("name"), Context({"name": "value"})), "value")


class ParseTokenContentsTest(TestCase):
    """`parse_token_contents` splits a tag's arguments, via the tag that uses it."""

    def render(self, template, context=None):
        return Template("{% load bootstrap4 %}" + template).render(Context(context or {}))

    def test_a_keyword_value_is_resolved_from_the_context(self):
        self.assertIn("Send", self.render("{% buttons submit=label %}{% endbuttons %}", {"label": "Send"}))

    def test_no_arguments_at_all(self):
        """The bits list is empty, so the argument loop is skipped."""
        self.assertIsInstance(self.render("{% buttons %}{% endbuttons %}"), str)

    def test_a_positional_argument_is_accepted(self):
        self.render('{% buttons "ignored" submit="OK" %}{% endbuttons %}')

    def test_as_binds_the_result_to_a_variable(self):
        html = self.render("{% buttons submit='OK' as block %}{% endbuttons %}[{{ block|safe }}]")
        self.assertTrue(html.strip().startswith("["))
        self.assertIn('type="submit"', html)

    def test_a_malformed_argument_is_rejected(self):
        """
        Django's own tokenizer never produces an empty bit, so this guards direct callers.

        `kwarg_re` matches every non-empty string, so a template cannot reach this branch.
        """
        from bootstrap4.utils import parse_token_contents

        class FakeToken:
            def split_contents(self):
                return ["buttons", ""]

        with self.assertRaises(TemplateSyntaxError) as caught:
            parse_token_contents(parser=None, token=FakeToken())
        self.assertIn("Malformed arguments", str(caught.exception))


class RemoveCssClassTest(TestCase):
    def test_removes_only_the_named_classes(self):
        self.assertEqual(remove_css_class("a b c", "b"), "a c")

    def test_removes_several_at_once(self):
        self.assertEqual(remove_css_class("a b c", "a c"), "b")

    def test_a_class_that_is_not_there_changes_nothing(self):
        self.assertEqual(remove_css_class("a b", "z"), "a b")


class RenderLinkTagTest(TestCase):
    def test_without_media(self):
        self.assertHTMLEqual(render_link_tag("/style.css"), '<link href="/style.css" rel="stylesheet">')

    def test_with_media(self):
        self.assertHTMLEqual(
            render_link_tag("/style.css", media="print"),
            '<link href="/style.css" media="print" rel="stylesheet">',
        )
