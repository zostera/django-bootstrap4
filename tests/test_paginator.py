from django.core.paginator import Paginator
from django.test import TestCase

from bootstrap4.utils import url_replace_param

from .utils import render_template


class PaginatorTest(TestCase):
    def test_url_replace_param(self):
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", "yohoo"), "/foo/bar?baz=yohoo")
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", None), "/foo/bar")
        self.assertEqual(url_replace_param("/foo/bar#id", "baz", "foo"), "/foo/bar?baz=foo#id")

    def bootstrap_pagination(self, page, extra=""):
        """Helper to test bootstrap_pagination tag."""
        template = """
            {% load bootstrap4 %}
            {% bootstrap_pagination page {extra} %}
        """.replace(
            "{extra}", extra
        )

        return render_template(template, {"page": page})

    def test_paginator(self):
        objects = ["john", "paul", "george", "ringo"]
        p = Paginator(objects, 2)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/?foo=bar"')
        # order in dicts is not guaranteed in some python versions,
        # so we have to check both options
        self.assertTrue("/projects/?foo=bar&page=1" in res or "/projects/?page=1&foo=bar" in res)
        self.assertTrue("/projects/?foo=bar&page=3" not in res and "/projects/?page=3&foo=bar" not in res)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/#id"')
        self.assertTrue("/projects/?page=1#id" in res)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/?page=3#id"')
        self.assertTrue("/projects/?page=1#id" in res)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/?page=3" extra="id=20"')
        self.assertTrue("/projects/?page=1&id=20" in res or "/projects/?id=20&page=1" in res)
