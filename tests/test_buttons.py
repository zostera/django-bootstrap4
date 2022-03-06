from django.test import TestCase

from bootstrap4.exceptions import BootstrapError
from bootstrap4.forms import render_button

from .utils import render_template_with_form


class ButtonsTest(TestCase):
    def test_button(self):
        self.assertEqual(render_button("button"), '<button class="btn btn-primary">button</button>')

    def test_button_with_illegal_type(self):
        try:
            self.assertEqual(
                render_button("button", button_type="illegal"), '<button class="btn btn-primary">button</button>'
            )
        except BootstrapError as e:
            self.assertEqual(
                str(e),
                'Parameter "button_type" should be "submit", "reset", "button", "link" or empty ("illegal" given).',
            )

    def test_bootstrap_button_tag(self):
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(res.strip(), '<button class="btn btn-primary btn-lg">button</button>')

        link_button = '<a class="btn btn-primary btn-lg" href="#" role="button">button</a>'

        res = render_template_with_form("{% bootstrap_button 'button' size='lg' href='#' %}")
        self.assertIn(res.strip(), link_button)
        res = render_template_with_form("{% bootstrap_button 'button' button_type='link' size='lg' href='#' %}")
        self.assertIn(res.strip(), link_button)
        with self.assertRaises(BootstrapError):
            res = render_template_with_form("{% bootstrap_button 'button' button_type='button' href='#' %}")
