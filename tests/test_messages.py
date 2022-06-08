import re

from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.test import TestCase

from .utils import render_template_with_form


class MessagesTest(TestCase):
    def test_bootstrap_messages(self):
        class FakeMessage(object):
            """Follows the `django.contrib.messages.storage.base.Message` API."""

            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(r"\s+")
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(None, "hello")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="close">&#215;</button>
        hello http://example.com
    </div>        """
        self.assertEqual(
            re.sub(pattern, "", res).replace('rel="nofollow"', ""),
            re.sub(pattern, "", expected).replace('rel="nofollow"', ""),
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        res = render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages})
        expected = """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello there
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))
