from django.test import TestCase

from bootstrap4.components import render_alert


class ComponentsTest(TestCase):
    def test_render_alert_with_type(self):
        alert = render_alert("content")
        self.assertEqual(
            alert,
            '<div class="alert alert-info alert-dismissable" role="alert">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-label="close">'
            + "&times;</button>content</div>",
        )
