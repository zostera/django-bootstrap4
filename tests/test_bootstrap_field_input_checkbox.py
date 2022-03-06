from django import forms

from tests.base import BootstrapTestCase


class CheckboxTestForm(forms.Form):
    test = forms.BooleanField()


class InputTypeCheckboxTestCase(BootstrapTestCase):
    def test_input_type_checkbox(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CheckboxTestForm()}),
            (
                '<div class="django_bootstrap4-req">'
                '<div class="form-check">'
                '<input type="checkbox" name="test" class="form-check-input" required id="id_test">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_is_invalid(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CheckboxTestForm(data={})}),
            (
                '<div class="bootstrap4-err django_bootstrap4-req"><div class="form-check">'
                '<input type="checkbox" name="test" class="form-check-input" required id="id_test">'
                '<label class="form-check-label" for="id_test">Test</label>'
                '<div class="invalid-feedback">This field is required.</div>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_is_valid(self):
        """Test field with checkbox widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": CheckboxTestForm(data={"test": "on"})}),
            (
                '<div class="bootstrap4-bound django_bootstrap4-req">'
                '<div class="form-check">'
                '<input type="checkbox" name="test" class="form-check-input" required id="id_test" checked>'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_input_type_checkbox_style_switch(self):
        """Test field with checkbox widget, style switch."""
        self.assertHTMLEqual(
            self.render(
                '{% bootstrap_field form.test checkbox_style="switch" %}', context={"form": CheckboxTestForm()}
            ),
            (
                '<div class="django_bootstrap4-req">'
                '<div class="form-check form-switch">'
                '<input type="checkbox" name="test" class="form-check-input" required id="id_test">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
            ),
        )

    def test_bootstrap_field_checkbox_horizontal(self):
        """Test field with checkbox widget, layout horizontal."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='horizontal' %}", context={"form": CheckboxTestForm()}),
            (
                '<div class="row django_bootstrap4-req">'
                '<div class="col-md-9">'
                '<div class="form-check">'
                '<input type="checkbox" name="test" class="form-check-input" required id="id_test">'
                '<label class="form-check-label" for="id_test">Test</label>'
                "</div>"
                "</div>"
                "</div>"
            ),
        )
