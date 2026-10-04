from django.forms import formset_factory
from django.test import TestCase

from bootstrap4.exceptions import BootstrapError
from bootstrap4.forms import render_button, render_field_and_label, render_form_errors, render_formset_errors

from .forms import TestForm


class RenderButtonSizeTest(TestCase):
    """`size` maps to a Bootstrap button size class."""

    def test_sizes(self):
        for size, expected in (
            ("xs", "btn-xs"),
            ("sm", "btn-sm"),
            ("small", "btn-sm"),
            ("lg", "btn-lg"),
            ("large", "btn-lg"),
        ):
            with self.subTest(size=size):
                self.assertIn(expected, render_button("Click", size=size))

    def test_medium_adds_no_size_class(self):
        for size in ("md", "medium"):
            with self.subTest(size=size):
                html = render_button("Click", size=size)
                self.assertNotIn("btn-xs", html)
                self.assertNotIn("btn-sm", html)
                self.assertNotIn("btn-lg", html)

    def test_an_unknown_size_is_rejected(self):
        with self.assertRaises(BootstrapError) as caught:
            render_button("Click", size="enormous")
        self.assertIn('should be "xs", "sm", "lg" or empty', str(caught.exception))


class RenderButtonAttributesTest(TestCase):
    """The optional attributes are only emitted when given."""

    def test_each_attribute_is_emitted(self):
        html = render_button("Click", id="go", name="action", value="save", title="Save it")
        self.assertIn('id="go"', html)
        self.assertIn('name="action"', html)
        self.assertIn('value="save"', html)
        self.assertIn('title="Save it"', html)

    def test_none_are_emitted_by_default(self):
        html = render_button("Click")
        for attribute in ("id=", "name=", "value=", "title="):
            self.assertNotIn(attribute, html)


class RenderErrorsTest(TestCase):
    """The standalone error renderers."""

    def test_form_errors(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("This field is required", render_form_errors(form))

    def test_form_errors_for_a_single_type(self):
        form = TestForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn(TestForm.non_field_error_message, render_form_errors(form, type="non_fields"))

    def test_formset_errors(self):
        formset_class = formset_factory(TestForm, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertIsInstance(render_formset_errors(formset), str)


class RenderFieldAndLabelTest(TestCase):
    """Horizontal layout fills in the classes the caller did not supply."""

    def test_horizontal_defaults_are_used_when_nothing_is_given(self):
        html = render_field_and_label("<input>", "Label", layout="horizontal")
        self.assertIn("col-form-label", html)
        self.assertIn("col-md-", html)

    def test_explicit_classes_are_left_alone(self):
        html = render_field_and_label(
            "<input>", "Label", layout="horizontal", label_class="my-label", field_class="my-field"
        )
        self.assertIn("my-label", html)
        self.assertIn("my-field", html)
        self.assertIn("col-form-label", html)

    def test_an_empty_label_becomes_a_non_breaking_space(self):
        self.assertIn("&#160;", render_field_and_label("<input>", "", layout="horizontal"))
