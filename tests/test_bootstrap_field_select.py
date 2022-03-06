from django import forms

from .base import BootstrapTestCase


class SelectTestForm(forms.Form):
    test = forms.ChoiceField(
        choices=(
            (1, "one"),
            (2, "two"),
        )
    )


class BootstrapFieldRadioSelectTestCase(BootstrapTestCase):
    def test_select(self):
        """Test field with select widget."""
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<select class="form-select" id="id_test" name="test">'
                '<option value="1">one</option>'
                '<option value="2">two</option>'
                "</select>"
                "</div>"
            ),
        )

    def test_select_horizontal(self):
        """Test field with select widget in horizontal layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="horizontal" %}', context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req row mb-3">'
                '<label for="id_test" class="col-form-label col-sm-2">Test</label>'
                '<div class="col-sm-10">'
                '<select class="form-select" id="id_test" name="test">'
                '<option value="1">one</option>'
                '<option value="2">two</option>'
                "</select>"
                "</div>"
                "</div>"
            ),
        )

    def test_select_floating(self):
        """Test field with select widget in floating layout."""
        self.assertHTMLEqual(
            self.render('{% bootstrap_field form.test layout="floating" %}', context={"form": SelectTestForm()}),
            (
                '<div class="django_bootstrap5-req form-floating mb-3">'
                '<select class="form-select" id="id_test" name="test">'
                '<option value="1">one</option>'
                '<option value="2">two</option>'
                "</select>"
                '<label for="id_test" class="form-label">Test</label>'
                "</div>"
            ),
        )
