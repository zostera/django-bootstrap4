from bs4 import BeautifulSoup
from django import forms
from django.forms import formset_factory

from tests.base import BootstrapTestCase


class FormTestForm(forms.Form):
    required_text = forms.CharField(required=True, help_text="<i>required_text_help</i>")
    optional_text = forms.CharField(required=False, help_text="<i>required_text_help</i>")


class ShowLabelTestForm(forms.Form):
    subject = forms.CharField()


class NonFieldErrorTestForm(FormTestForm):
    non_field_error_message = "This is a non field error."

    def clean(self):
        super().clean()
        raise forms.ValidationError(self.non_field_error_message)


class BootstrapFormTestCase(BootstrapTestCase):
    def test_illegal_form(self):
        with self.assertRaises(TypeError):
            self.render("{% bootstrap_form form %}", {"form": "illegal"})

    def test_exclude(self):
        html = self.render('{% bootstrap_form form exclude="optional_text" %}', {"form": FormTestForm()})
        self.assertHTMLEqual(
            html,
            (
                '<div class="mb-3 django_bootstrap5-req">'
                '<label class="form-label" for="id_required_text">Required text</label>'
                '<input type="text" name="required_text" class="form-control"'
                ' placeholder="Required text" required id="id_required_text">'
                '<div class="form-text"><i>required_text_help</i>'
                "</div>"
            ),
        )

    def test_error_css_class(self):
        form = FormTestForm({"optional_text": "my_message"})

        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-err", html)

        html = self.render('{% bootstrap_form form error_css_class="custom-error-class" %}', {"form": form})
        self.assertIn("custom-error-class", html)

        html = self.render('{% bootstrap_form form error_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-err", html)

    def test_required_css_class(self):
        form = FormTestForm({"subject": "subject"})
        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-req", html)

        html = self.render('{% bootstrap_form form required_css_class="custom-required-class" %}', {"form": form})
        self.assertIn("custom-required-class", html)

        html = self.render('{% bootstrap_form form required_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-req", html)

    def test_success_css_class(self):
        form = FormTestForm({"subject": "subject"})

        html = self.render("{% bootstrap_form form %}", {"form": form})
        self.assertIn("django_bootstrap5-success", html)

        form = FormTestForm({"subject": "subject"})

        html = self.render('{% bootstrap_form form success_css_class="successful-test" %}', {"form": form})
        self.assertIn("successful-test", html)

        form = FormTestForm({"subject": "subject"})

        html = self.render('{% bootstrap_form form success_css_class="" %}', {"form": form})
        self.assertNotIn("django_bootstrap5-success", html)

    def test_alert_error_type(self):
        form = NonFieldErrorTestForm({"subject": "subject"})

        html = self.render("{% bootstrap_form form alert_error_type='all' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='non_fields' %}", {"form": form})
        self.assertEqual(
            html,
            self.render("{% bootstrap_form form %}", {"form": form}),
            "Default behavior is not the same as showing non-field errors",
        )

        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertIn(form.non_field_error_message, errors)
        self.assertNotIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='fields' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        errors = list(soup.select(".text-danger")[0].stripped_strings)
        self.assertNotIn(form.non_field_error_message, errors)
        self.assertIn("This field is required.", errors)

        html = self.render("{% bootstrap_form form alert_error_type='none' %}", {"form": form})
        soup = BeautifulSoup(html, "html.parser")
        self.assertFalse(soup.select(".text-danger"))

    def test_form_errors(self):
        form = FormTestForm({"subject": "subject"})
        html = self.render("{% bootstrap_form_errors form %}", {"form": form})
        self.assertHTMLEqual(
            html,
            '<ul class="list-unstyled text-danger"><li>This field is required.</li></ul>',
        )


class ShowLabelTestCase(BootstrapTestCase):
    def test_show_label_false(self):
        self.assertInHTML(
            '<label class="visually-hidden" for="id_subject">Subject</label>',
            self.render("{% bootstrap_form form show_label=False %}", {"form": ShowLabelTestForm()}),
        )

    def test_show_label_sr_only(self):
        self.assertInHTML(
            '<label class="visually-hidden" for="id_subject">Subject</label>',
            self.render("{% bootstrap_form form show_label='' %}", {"form": ShowLabelTestForm()}),
        )

    def test_show_label_skip(self):
        self.assertNotIn(
            "label",
            self.render("{% bootstrap_form form show_label='skip' %}", {"form": ShowLabelTestForm()}),
        )

    def test_show_label_false_in_formset(self):
        TestFormSet = formset_factory(ShowLabelTestForm, extra=1)
        self.assertInHTML(
            '<label class="visually-hidden" for="id_form-0-subject">Subject</label>',
            self.render("{% bootstrap_formset formset show_label=False %}", {"formset": TestFormSet()}),
        )
