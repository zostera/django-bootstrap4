from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.test import TestCase

from .utils import render_template_with_form


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


class MessagesTest(TestCase):
    def test_bootstrap_messages(self):
        for messages, expected_html in [
            [
                [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")],
                """
    <div class="alert alert-warning alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
""",
            ],
            [
                [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")],
                """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """,
            ],
            [
                [FakeMessage(None, "hello")],
                """
    <div class="alert alert-info alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """,
            ],
            [
                [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")],
                """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="close">&#215;</button>
        hello http://example.com
    </div>        """,
            ],
            [
                [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")],
                """
    <div class="alert alert-danger alert-dismissible fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello there
    </div>
        """,
            ],
        ]:
            self.assertHTMLEqual(
                render_template_with_form("{% bootstrap_messages messages %}", {"messages": messages}), expected_html
            )
