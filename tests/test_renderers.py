from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashWidget
from django.forms import formset_factory
from django.test import TestCase

from bootstrap4.exceptions import BootstrapError
from bootstrap4.renderers import BaseRenderer, FieldRenderer, FormsetRenderer, InlineFieldRenderer

from .forms import TestForm
from .utils import render_form_field, render_template_with_form


class SelectDateForm(forms.Form):
    when = forms.DateField(widget=forms.SelectDateWidget)


class FileForm(forms.Form):
    attachment = forms.FileField(widget=forms.ClearableFileInput, required=False)

    use_required_attribute = False


class PasswordHashForm(forms.Form):
    password = forms.CharField(widget=ReadOnlyPasswordHashWidget, required=False)


class ComplainingFormSet(forms.BaseFormSet):
    def clean(self):
        raise forms.ValidationError("Formset-level problem.")


class BaseRendererTest(TestCase):
    def test_render_of_the_base_class_is_empty(self):
        """BaseRenderer._render is a no-op that subclasses override."""
        self.assertEqual(BaseRenderer()._render(), "")

    def test_an_invalid_size_is_rejected(self):
        with self.assertRaises(BootstrapError) as caught:
            BaseRenderer(size="enormous")
        self.assertIn('Invalid value "enormous"', str(caught.exception))

    def test_the_accepted_sizes(self):
        for size, expected in (
            ("sm", "small"),
            ("small", "small"),
            ("lg", "large"),
            ("large", "large"),
            ("md", "medium"),
            ("medium", "medium"),
            ("", "medium"),
        ):
            with self.subTest(size=size):
                self.assertEqual(BaseRenderer(size=size).size, expected)


class FormsetErrorsTest(TestCase):
    def test_non_form_errors_are_rendered(self):
        formset_class = formset_factory(TestForm, formset=ComplainingFormSet, extra=1)
        formset = formset_class(data={"form-TOTAL_FORMS": "1", "form-INITIAL_FORMS": "0"})
        self.assertFalse(formset.is_valid())
        self.assertIn("Formset-level problem.", FormsetRenderer(formset).render_errors())


class WidgetSpecificMarkupTest(TestCase):
    """Widgets whose rendered HTML is rearranged after the widget renders itself."""

    def test_select_date_widget_is_split_into_columns(self):
        html = render_form_field("when", context={"form": SelectDateForm()})
        self.assertIn("bootstrap4-multi-input", html)
        self.assertIn('<div class="col-4">', html)

    def test_a_file_input_label_is_pushed_onto_its_own_line(self):
        html = render_form_field("attachment", context={"form": FileForm()})
        self.assertIn("form-control-file", html)
        self.assertIn("<br>", html)

    def test_a_file_input_in_horizontal_layout_keeps_its_line(self):
        html = render_template_with_form(
            "{% bootstrap_field form.attachment layout='horizontal' %}", {"form": FileForm()}
        )
        self.assertIn("form-control-file", html)
        self.assertNotIn("<br>", html)

    def test_read_only_password_hash_widget_is_a_static_control(self):
        html = render_form_field("password", context={"form": PasswordHashForm()})
        self.assertIn("form-control-static", html)


class RendererHelperDefaultsTest(TestCase):
    """The widget argument of these helpers defaults to the renderer's own widget."""

    def _renderer(self):
        return FieldRenderer(TestForm()["subject"])

    def test_add_class_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("class", None)
        renderer.add_class_attrs()
        self.assertIn("form-control", renderer.widget.attrs["class"])

    def test_add_placeholder_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("placeholder", None)
        renderer.add_placeholder_attrs()
        self.assertIn("placeholder", renderer.widget.attrs)

    def test_add_help_attrs_defaults_to_own_widget(self):
        renderer = self._renderer()
        renderer.widget.attrs.pop("title", None)
        renderer.add_help_attrs()
        self.assertIn("title", renderer.widget.attrs)


class PlaceholderTest(TestCase):
    """Where the placeholder comes from."""

    def test_it_defaults_to_the_label(self):
        renderer = FieldRenderer(TestForm()["sender"])
        self.assertEqual(renderer.placeholder, TestForm()["sender"].label)

    def test_an_explicit_empty_placeholder_is_honoured(self):
        self.assertEqual(FieldRenderer(TestForm()["sender"], placeholder="").placeholder, "")

    def test_set_placeholder_off_leaves_it_empty(self):
        with self.settings(BOOTSTRAP4={"set_placeholder": False}):
            renderer = FieldRenderer(TestForm()["sender"])
        self.assertEqual(renderer.placeholder, "")


class InlineFieldRendererTest(TestCase):
    """Inline layout hides the label and folds the errors into the widget's title."""

    def test_the_label_is_screen_reader_only(self):
        html = render_template_with_form("{% bootstrap_form form layout='inline' %}", {"form": TestForm()})
        self.assertIn("sr-only", html)

    def test_errors_move_into_the_title_attribute(self):
        html = InlineFieldRenderer(TestForm(data={})["sender"], layout="inline").render()
        self.assertIn("This field is required", html)
        self.assertIn("title=", html)

    def test_an_existing_title_is_kept(self):
        field = TestForm(data={})["sender"]
        field.field.widget.attrs["title"] = "Mine"
        renderer = InlineFieldRenderer(field, layout="inline")
        renderer.add_error_attrs()
        self.assertTrue(renderer.widget.attrs["title"].startswith("Mine"))

    def test_nothing_is_appended_to_the_field(self):
        """Help text and errors are not rendered below an inline field."""
        renderer = InlineFieldRenderer(TestForm()["subject"], layout="inline")
        self.assertEqual(renderer.append_to_field("<input>"), "<input>")

    def test_the_field_class_is_used_as_given(self):
        renderer = InlineFieldRenderer(TestForm()["subject"], layout="inline", field_class="mine")
        self.assertEqual(renderer.get_field_class(), "mine")
