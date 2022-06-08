from bs4 import BeautifulSoup
from django.forms import formset_factory
from django.test import TestCase
from django.utils.html import escape

from bootstrap4.exceptions import BootstrapError
from bootstrap4.utils import DJANGO_VERSION
from tests.utils import html_39x27

from .forms import CharFieldTestForm, TestForm
from .utils import render_field, render_form_field, render_template_with_form


class FieldTest(TestCase):
    def _select_one_element(self, html, selector, err_msg):
        """
        Select exactly one html element in an BeautifulSoup html fragment.

        Fail if there is not exactly one element.
        """
        lst = html.select(selector)
        self.assertEqual(len(lst), 1, err_msg)
        return lst[0]

    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_show_help(self):
        res = render_form_field("subject")
        self.assertIn("my_help_text", res)
        self.assertNotIn("<i>my_help_text</i>", res)
        res = render_template_with_form("{% bootstrap_field form.subject show_help=0 %}")
        self.assertNotIn("my_help_text", res)

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = render_form_field("sender")
        self.assertIn('title="{}"'.format(escape(TestForm.base_fields["sender"].help_text)), res)
        res = render_form_field("cc_myself")
        self.assertIn('title="{}"'.format(escape(TestForm.base_fields["cc_myself"].help_text)), res)

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_xss_field(self):
        res = render_form_field("xss_field")
        self.assertIn('type="text"', res)

        expect = html_39x27(
            '<label for="id_xss_field">'
            "XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;</label>"
        )
        self.assertIn(
            expect,
            res,
        )
        expect = html_39x27('placeholder="XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;"')
        self.assertIn(expect, res)

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_radio_select(self):
        """Test RadioSelect rendering, because it is special."""
        res = render_form_field("category1")
        expected_html = (
            '<div class="form-group bootstrap4-req">'
            '<label for="id_category1_0">Category1</label>'
            '<div class="radio radio-success" id="id_category1">'
            '<div class="form-check">'
            '<label class="form-check-label" for="id_category1_0">'
            '<input class="form-check-input" id="id_category1_0" name="category1" title="" type="radio" value="1">'
            "Radio 1"
            "</label>"
            "</div>"
            '<div class="form-check">'
            '<label class="form-check-label" for="id_category1_1">'
            '<input class="form-check-input" id="id_category1_1" name="category1" title="" type="radio" value="2">'
            "Radio 2"
            "</label>"
            "</div>"
            "</div>"
            "</div>"
        )
        if DJANGO_VERSION >= 4:
            expected_html = expected_html.replace(
                '<label for="id_category1_0">Category1</label>', "<label>Category1</label>"
            )
        self.assertHTMLEqual(res, expected_html)

    def test_checkbox(self):
        """Test Checkbox rendering, because it is special."""
        res = render_form_field("cc_myself")
        # strip out newlines and spaces around newlines
        res = "".join(line.strip() for line in res.split("\n"))
        res = BeautifulSoup(res, "html.parser")
        form_group = self._select_one_element(res, ".form-group", "Checkbox should be rendered inside a .form-group.")
        form_check = self._select_one_element(
            form_group, ".form-check", "There should be a .form-check inside .form-group"
        )
        checkbox = self._select_one_element(form_check, "input", "The checkbox should be inside the .form-check")
        self.assertIn("form-check-input", checkbox["class"], "The checkbox should have the class 'form-check-input'.")
        label = checkbox.nextSibling
        self.assertIsNotNone(label, "The label should be rendered after the checkbox.")
        self.assertEqual(label.name, "label", "After the checkbox there should be a label.")
        self.assertEqual(
            label["for"], checkbox["id"], "The for attribute of the label should be the id of the checkbox."
        )
        help_text = label.nextSibling
        self.assertIsNotNone(help_text, "The help text should be rendered after the label.")
        self.assertEqual(help_text.name, "small", "The help text should be rendered as <small> tag.")
        self.assertIn("form-text", help_text["class"], "The help text should have the class 'form-text'.")
        self.assertIn("text-muted", help_text["class"], "The help text should have the class 'text-muted'.")

    def test_required_field(self):
        required_css_class = "bootstrap4-req"
        required_field = render_form_field("subject")
        self.assertIn(required_css_class, required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field " + form_field + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        required_css_class = "bootstrap4-req"
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn(required_css_class, res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn(required_css_class, res)

    def test_input_group(self):
        res = render_template_with_form('{% bootstrap_field form.subject addon_before="$"  addon_after=".00" %}')
        self.assertIn('class="input-group"', res)
        self.assertIn('class="input-group-prepend"><span class="input-group-text">$', res)
        self.assertIn('class="input-group-append"><span class="input-group-text">.00', res)

    def test_input_group_addon_button(self):
        res = render_template_with_form(
            # Jumping through hoops to keep flake8 and black happy here
            "{% bootstrap_field "
            'form.subject addon_before="$" addon_before_class=None addon_after=".00" addon_after_class=None'
            " %}"
        )
        self.assertIn('class="input-group"', res)
        self.assertIn('<div class="input-group-prepend">$</div>', res)
        self.assertIn('<div class="input-group-append">.00</div>', res)

    def test_input_group_addon_empty(self):
        res = render_template_with_form(
            '{% bootstrap_field form.subject addon_before=None addon_after="after" %}'
        )  # noqa
        self.assertIn('class="input-group"', res)
        self.assertNotIn("input-group-prepend", res)
        self.assertIn('<div class="input-group-append"><span class="input-group-text">after</span></div>', res)

    def test_input_group_addon_validation(self):
        """
        Test that invalid-feedback messages are placed inside input-groups.

        See issue #89.
        """
        # invalid form data:
        data = {"subject": ""}
        res = render_template_with_form(
            '{% bootstrap_field form.subject addon_before=None addon_after="after" %}', data=data
        )  # noqa
        res = BeautifulSoup(res, "html.parser")
        self._select_one_element(
            res,
            ".input-group > .invalid-feedback",
            "The invalid-feedback message, complaining that this field is "
            "required, must be placed inside the input-group",
        )
        self._select_one_element(
            res, ".form-group > .form-text", "The form-text message must be placed inside the form-group"
        )
        self.assertEqual(
            len(res.select(".form-group > .invalid-feedback")),
            0,
            "The invalid-feedback message must be placed inside the " "input-group and not inside the form-group",
        )
        self.assertEqual(
            len(res.select(".input-group > .form-text")),
            0,
            "The form-text message must be placed inside the form-group and " "not inside the input-group",
        )

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form('{% bootstrap_field form.subject size="' + param + '" %}')
            self.assertNotIn("form-control-lg", res)
            self.assertNotIn("form-control-sm", res)
            self.assertNotIn("form-control-md", res)

        _test_size("sm", "form-control-sm")
        _test_size("small", "form-control-sm")
        _test_size("lg", "form-control-lg")
        _test_size("large", "form-control-lg")
        _test_size_medium("md")
        _test_size_medium("medium")
        _test_size_medium("")

    def test_datetime(self):
        field = render_form_field("datetime")
        self.assertIn("vDateField", field)
        self.assertIn("vTimeField", field)

    def test_field_same_render(self):
        context = dict(form=TestForm())
        rendered_a = render_form_field("addon", context)
        rendered_b = render_form_field("addon", context)
        self.assertEqual(rendered_a, rendered_b)

    def test_label(self):
        res = render_template_with_form('{% bootstrap_label "foobar" label_for="subject" %}')
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields["addon"].widget.attrs.copy()
        self.assertEqual(attrs, form.fields["addon"].widget.attrs)


class ComponentsTest(TestCase):
    def test_bootstrap_alert(self):
        res = render_template_with_form('{% bootstrap_alert "content" alert_type="danger" %}')
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissible" role="alert">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-label="close">'
            + "&times;</button>content</div>",
        )


class ShowLabelTest(TestCase):
    def test_show_label_false(self):
        form = CharFieldTestForm()
        res = render_template_with_form("{% bootstrap_form form show_label=False %}", {"form": form})
        self.assertIn("sr-only", res)

    def test_show_label_sr_only(self):
        form = CharFieldTestForm()
        res = render_template_with_form("{% bootstrap_form form show_label='sr-only' %}", {"form": form})
        self.assertIn("sr-only", res)

    def test_show_label_skip(self):
        form = CharFieldTestForm()
        res = render_template_with_form("{% bootstrap_form form show_label='skip' %}", {"form": form})
        self.assertNotIn("<label>", res)

    def test_for_formset(self):
        TestFormSet = formset_factory(CharFieldTestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template_with_form("{% bootstrap_formset formset show_label=False %}", {"formset": test_formset})
        self.assertIn("sr-only", res)
