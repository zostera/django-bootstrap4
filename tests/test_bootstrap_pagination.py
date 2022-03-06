from django.core.paginator import Paginator
from django_bootstrap5.utils import url_replace_param

from tests.base import BootstrapTestCase


class PaginatorTestCase(BootstrapTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.beatles = ["john", "paul", "george", "ringo"]
        cls.paginator = Paginator(cls.beatles, 2)

    def test_url_replace_param(self):
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", "yohoo"), "/foo/bar?baz=yohoo")
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", None), "/foo/bar")
        self.assertEqual(url_replace_param("/foo/bar#id", "baz", "foo"), "/foo/bar?baz=foo#id")

    def bootstrap_pagination(self, page, extra=""):
        """Helper to test bootstrap_pagination tag."""
        return self.render(f"{{% bootstrap_pagination page {extra} %}}", {"page": page})

    def test_paginator(self):
        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?foo=bar"')
        self.assertHTMLEqual(
            html,
            (
                "<nav>"
                '<ul class="pagination">'
                '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="/projects/?foo=bar&page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
                "</nav>"
            ),
        )

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?page=3#id"')
        self.assertIn("/projects/?page=1#id", html)
        self.assertNotIn("/projects/?page=2#id", html)

        html = self.bootstrap_pagination(self.paginator.page(2), extra='url="/projects/?page=3" extra="id=20"')
        self.assertIn("/projects/?page=1&id=20", html)
        self.assertNotIn("/projects/?page=2&id=20", html)

    def test_paginator_size(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="sm" %}', {"page": self.paginator.page(2)}),
            (
                "<nav>"
                '<ul class="pagination pagination-sm">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
                "</nav>"
            ),
        )
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="lg" %}', {"page": self.paginator.page(2)}),
            (
                "<nav>"
                '<ul class="pagination pagination-lg">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
                "</nav>"
            ),
        )
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page size="md" %}', {"page": self.paginator.page(2)}),
            (
                "<nav>"
                '<ul class="pagination">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
                "</nav>"
            ),
        )

        with self.assertRaisesRegex(ValueError, 'Invalid value "xl" for parameter'):
            self.render('{% bootstrap_pagination page size="xl" %}', {"page": self.paginator.page(2)})

    def test_paginator_justify(self):
        self.assertHTMLEqual(
            self.render('{% bootstrap_pagination page justify_content="center" %}', {"page": self.paginator.page(2)}),
            (
                "<nav>"
                '<ul class="pagination justify-content-center">'
                '<li class="page-item"><a class="page-link" href="?page=1">&laquo;</a></li>'
                '<li class="page-item"><a class="page-link" href="?page=1">1</a></li>'
                '<li class="page-item active"><a class="page-link" href="#">2</a></li>'
                '<li class="page-item disabled"><a class="page-link" href="#">&raquo;</a></li>'
                "</ul>"
                "</nav>"
            ),
        )
        with self.assertRaises(ValueError):
            self.render(
                '{{% bootstrap_pagination page justify_content="somewhere" %}', {"page": self.paginator.page(2)}
            )

    def test_paginator_illegal(self):
        with self.assertRaises(ValueError):
            self.render('{% bootstrap_pagination page pages_to_show="foo" %}', {"page": self.paginator.page(2)})
        with self.assertRaises(ValueError):
            self.render("{{% bootstrap_pagination page pages_to_show=-5 %}", {"page": self.paginator.page(2)})


class LargePaginatorTestCase(BootstrapTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.numbers = [f"{number}" for number in range(1, 100)]
        cls.paginator = Paginator(cls.numbers, 2)

    def test_paginator_ellipsis(self):
        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(33)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=23">&hellip;</a></li>', html)
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=43">&hellip;</a></li>', html)

        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(2)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=17">&hellip;</a></li>', html)
        self.assertInHTML("&hellip;", html, count=1)

        html = self.render("{{% bootstrap_pagination page %}", {"page": self.paginator.page(49)})
        self.assertInHTML('<li class="page-item"><a class="page-link" href="?page=38">&hellip;</a></li>', html)
        self.assertInHTML("&hellip;", html, count=1)
