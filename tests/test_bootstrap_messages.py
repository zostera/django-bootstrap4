from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.contrib.messages.storage.base import Message
from django.utils.safestring import mark_safe

from tests.base import BootstrapTestCase


class MessagesTestCase(BootstrapTestCase):
    def _html(self, content, css_class):
        return (
            f'<div class="alert {css_class} alert-dismissible fade show" role="alert">'
            f"{content}"
            '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            "</div>"
        )

    def test_bootstrap_messages(self):
        messages = [Message(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-warning"),
        )

        messages = [Message(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-danger"),
        )

    def test_bootstrap_messages_with_other_levels(self):
        messages = [Message(DEFAULT_MESSAGE_LEVELS.INFO, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-info"),
        )
        messages = [Message(999, "hello")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello", css_class="alert-info"),
        )

    def test_bootstrap_messages_with_other_content(self):
        messages = [Message(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello http://example.com", css_class="alert-danger"),
        )

        messages = [Message(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="hello there", css_class="alert-danger"),
        )

    def test_bootstrap_messages_with_safe_message(self):
        messages = [Message(DEFAULT_MESSAGE_LEVELS.INFO, mark_safe("Click <a href='https://www.github.com/'>here</a>"))]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="Click <a href='https://www.github.com/'>here</a>", css_class="alert-info"),
        )

    def test_bootstrap_messages_with_invalid_message(self):
        messages = [None]
        self.assertHTMLEqual(
            self.render("{% bootstrap_messages messages %}", {"messages": messages}),
            self._html(content="", css_class="alert-info"),
        )
