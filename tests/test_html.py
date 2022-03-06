from django.test import TestCase

from django_bootstrap4.html import render_tag


class HtmlTestCase(TestCase):
    def test_render_tag(self):
        self.assertEqual(render_tag("span"), "<span></span>")
        self.assertEqual(render_tag("span", content="foo"), "<span>foo</span>")
        self.assertEqual(render_tag("span", attrs={"bar": 123}, content="foo"), '<span bar="123">foo</span>')
        self.assertEqual(render_tag("span", attrs={"bar": "{foo}"}, content="foo"), '<span bar="{foo}">foo</span>')
