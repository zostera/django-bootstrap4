from bs4 import BeautifulSoup
from django.test import TestCase

from bootstrap4.exceptions import BootstrapError

from .forms import TestForm
from .utils import render_form, render_formset, render_template_with_form


class BootstrapFormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset="illegal")


class BootstrapFormTest(TestCase):
    def test_illegal_form(self):
        with self.assertRaises(BootstrapError):
            render_form(form="illegal")

    def test_field_names(self):
        form = TestForm()
        res = render_form(form)
        for field in form:
            # datetime has a multiwidget field widget
            if field.name == "datetime":
                self.assertIn('name="datetime_0"', res)
                self.assertIn('name="datetime_1"', res)
            else:
                self.assertIn('name="%s"' % field.name, res)

    def test_field_addons(self):
        form = TestForm()
        res = render_form(form)
        self.assertIn(
            '<div class="input-group">'
            '<div class="input-group-prepend">'
            '<span class="input-group-text">before</span></div><input',
            res,
        )
        self.assertIn('><div class="input-group-append"><span class="input-group-text">after</span></div></div>', res)

    def test_exclude(self):
        form = TestForm()
        res = render_template_with_form('{% bootstrap_form form exclude="cc_myself" %}', {"form": form})
        self.assertNotIn("cc_myself", res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template_with_form('{% bootstrap_form form layout="horizontal" %}', {"form": form})
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)
        res = render_template_with_form(
            '{% bootstrap_form form layout="horizontal" '
            + 'horizontal_label_class="hlabel" '
            + 'horizontal_field_class="hfield" %}',
            {"form": form},
        )
        self.assertIn("hlabel", res)
        self.assertIn("hfield", res)

    def test_form_check_class(self):
        form = TestForm()
        res = render_template_with_form(
            "{% bootstrap_form form form_check_class='form-check form-check-inline' %}", {"form": form}
        )
        self.assertIn('div class="form-check form-check-inline"', res)

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template_with_form('{% buttons layout="horizontal" %}{% endbuttons %}', {"form": form})
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)

    def test_error_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-err", res)

        res = render_template_with_form('{% bootstrap_form form error_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form error_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap4-err", res)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-req", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="successful-test" %}', {"form": form}
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form('{% bootstrap_form form required_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap4-req", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-bound", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form('{% bootstrap_form form bound_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form('{% bootstrap_form form bound_css_class="" %}', {"form": form})
        self.assertNotIn("bootstrap4-bound", res)

    def test_radio_select_button_group(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        soup = BeautifulSoup(res, features="html.parser")
        element = soup.find("input", id="id_category5_0_0")
        self.assertEqual(element.attrs["name"], "category5")
        self.assertEqual(element.attrs["type"], "radio")

    def test_alert_error_type(self):
        form = TestForm({"sender": "sender"})

        # Show all error messages
        res = render_template_with_form("{% bootstrap_form form alert_error_type='all' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".alert-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        # Show only non-field error messages (default config)
        res = render_template_with_form("{% bootstrap_form form alert_error_type='non_fields' %}", {"form": form})
        default = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertEqual(res, default, "Default behavior is not the same as showing non-field errors")
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".alert-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertNotIn("This field is required.", errors)

        # Show only field error messages
        res = render_template_with_form("{% bootstrap_form form alert_error_type='fields' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        errors = list(html.select(".alert-danger")[0].stripped_strings)
        self.assertNotIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        # Show nothing
        res = render_template_with_form("{% bootstrap_form form alert_error_type='none' %}", {"form": form})
        html = BeautifulSoup(res, "html.parser")
        self.assertFalse(html.select(".alert-danger"))
