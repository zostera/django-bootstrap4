# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from bs4 import BeautifulSoup
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.gis import forms as gisforms
from django.contrib.messages import constants as DEFAULT_MESSAGE_LEVELS
from django.core.paginator import Paginator
from django.forms.formsets import formset_factory
from django.template import engines
from django.test import TestCase, override_settings
from django.utils.html import escape

from bootstrap4.bootstrap import get_bootstrap_setting
from bootstrap4.exceptions import BootstrapError
from bootstrap4.text import text_concat, text_value
from bootstrap4.utils import add_css_class, render_tag, url_replace_param
from bootstrap4.widgets import RadioSelectButtonGroup

RADIO_CHOICES = (("1", "Radio 1"), ("2", "Radio 2"))

MEDIA_CHOICES = (
    ("Audio", (("vinyl", "Vinyl"), ("cd", "CD"))),
    ("Video", (("vhs", "VHS Tape"), ("dvd", "DVD"))),
    ("unknown", "Unknown"),
)


class TestForm(forms.Form):
    """
    Form with a variety of widgets to test bootstrap4 rendering.
    """

    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"})
    )
    xss_field = forms.CharField(
        label='XSS" onmouseover="alert(\'Hello, XSS\')" foo="',
        max_length=100,
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text="<i>my_help_text</i>")
    sender = forms.EmailField(
        label="Sender © unicode", help_text='E.g., "me@example.com"'
    )
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False,
        help_text='cc stands for "carbon copy." You will get a copy in your mailbox.',
    )
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES, help_text="Check as many as you like."
    )
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES, help_text="Check as many as you like."
    )
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Check as many as you like.",
    )
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        help_text="Check as many as you like.",
    )
    category5 = forms.ChoiceField(widget=RadioSelectButtonGroup, choices=MEDIA_CHOICES)
    addon = forms.CharField(
        widget=forms.TextInput(attrs={"addon_before": "before", "addon_after": "after"})
    )
    polygon = gisforms.PointField()

    required_css_class = "bootstrap4-req"

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling."
        )
        return cleaned_data


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ""


def render_template(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap4.
    """
    template = engines["django"].from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_template_with_bootstrap(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap4.
    """
    if not context:
        context = {}
    return render_template("{% load bootstrap4 %}" + text, context)


def render_template_with_form(text, context=None):
    """
    Create a template ``text`` that first loads bootstrap4.
    """
    if not context:
        context = {}
    if "form" not in context:
        context["form"] = TestForm()
    return render_template_with_bootstrap(text, context)


def render_formset(formset=None, context=None):
    """
    Create a template that renders a formset
    """
    if not context:
        context = {}
    context["formset"] = formset
    return render_template_with_form("{% bootstrap_formset formset %}", context)


def render_form(form=None, context=None):
    """
    Create a template that renders a form
    """
    if not context:
        context = {}
    if form:
        context["form"] = form
    return render_template_with_form("{% bootstrap_form form %}", context)


def render_form_field(field, context=None):
    """
    Create a template that renders a field
    """
    form_field = "form.%s" % field
    return render_template_with_form(
        "{% bootstrap_field " + form_field + " %}", context
    )


def render_field(field, context=None):
    """
    Create a template that renders a field
    """
    if not context:
        context = {}
    context["field"] = field
    return render_template_with_form("{% bootstrap_field field %}", context)


class MediaTest(TestCase):
    def expected_css(self, tag):
        template = '<link href="{href}" integrity="{integrity}" crossorigin="{crossorigin}" rel="stylesheet">'

        setting = get_bootstrap_setting(tag + "_url")
        return template.format(**setting)

    def expected_js(self, tag):
        template = '<script src="{url}" integrity="{integrity}" crossorigin="{crossorigin}"></script>'
        setting = get_bootstrap_setting(tag + "_url")

        return template.format(**setting)

    def test_bootstrap_jquery(self):
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery %}"),
            self.expected_js("jquery"),
        )
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery jquery=True %}"),
            self.expected_js("jquery"),
        )
        self.assertHTMLEqual(
            render_template_with_form('{% bootstrap_jquery jquery="full" %}'),
            self.expected_js("jquery"),
        )
        self.assertHTMLEqual(
            render_template_with_form('{% bootstrap_jquery jquery="slim" %}'),
            self.expected_js("jquery_slim"),
        )
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery jquery=False %}"), ""
        )

    @override_settings(BOOTSTRAP4={"jquery_url": {"url": "foo"}})
    def test_bootstrap_jquery_custom_setting_dict(self):
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery %}"),
            '<script src="foo"></script>',
        )

    @override_settings(BOOTSTRAP4={"jquery_url": "http://example.com"})
    def test_bootstrap_jquery_custom_setting_str(self):
        self.assertHTMLEqual(
            render_template_with_form("{% bootstrap_jquery %}"),
            '<script src="http://example.com"></script>',
        )

    def test_bootstrap_javascript_tag(self):
        html = render_template_with_form("{% bootstrap_javascript jquery=True %}")
        # jQuery
        self.assertInHTML(self.expected_js("jquery"), html)
        # Popper
        self.assertInHTML(self.expected_js("popper"), html)
        # Bootstrap
        self.assertInHTML(self.expected_js("javascript"), html)

    def test_bootstrap_css_tag(self):
        html = render_template_with_form("{% bootstrap_css %}").strip()
        self.assertInHTML(self.expected_css("css"), html)
        # Theme
        self.assertInHTML(
            '<link rel="stylesheet" href="//example.com/theme.css">', html
        )

    def test_settings_filter(self):
        res = render_template_with_form('{{ "required_css_class"|bootstrap_setting }}')
        self.assertEqual(res.strip(), "bootstrap4-req")
        res = render_template_with_form(
            '{% if "javascript_in_head"|bootstrap_setting %}head{% else %}body{% endif %}'
        )
        self.assertEqual(res.strip(), "head")

    def test_required_class(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-req", res)

    def test_error_class(self):
        form = TestForm({})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-err", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-bound", res)


class TemplateTest(TestCase):
    def test_empty_template(self):
        res = render_template_with_form("")
        self.assertEqual(res.strip(), "")

    def test_text_template(self):
        res = render_template_with_form("some text")
        self.assertEqual(res.strip(), "some text")

    def test_bootstrap_template(self):
        res = render_template(
            '{% extends "bootstrap4/bootstrap4.html" %}'
            + "{% block bootstrap4_content %}"
            + "test_bootstrap4_content"
            + "{% endblock %}"
        )
        self.assertIn("test_bootstrap4_content", res)

    def test_javascript_without_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript %}")
        self.assertIn("bootstrap", res)
        self.assertNotIn("jquery", res)

    def test_javascript_with_jquery(self):
        res = render_template_with_form("{% bootstrap_javascript jquery=True %}")
        self.assertIn("bootstrap", res)
        self.assertIn("jquery", res)


class FormSetTest(TestCase):
    def test_illegal_formset(self):
        with self.assertRaises(BootstrapError):
            render_formset(formset="illegal")


class FormTest(TestCase):
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
        self.assertIn(
            '><div class="input-group-append"><span class="input-group-text">after</span></div></div>',
            res,
        )

    def test_exclude(self):
        form = TestForm()
        res = render_template_with_form(
            '{% bootstrap_form form exclude="cc_myself" %}', {"form": form}
        )
        self.assertNotIn("cc_myself", res)

    def test_layout_horizontal(self):
        form = TestForm()
        res = render_template_with_form(
            '{% bootstrap_form form layout="horizontal" %}', {"form": form}
        )
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

    def test_buttons_tag(self):
        form = TestForm()
        res = render_template_with_form(
            '{% buttons layout="horizontal" %}{% endbuttons %}', {"form": form}
        )
        self.assertIn("col-md-3", res)
        self.assertIn("col-md-9", res)

    def test_error_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-err", res)

        res = render_template_with_form(
            '{% bootstrap_form form error_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form(
            '{% bootstrap_form form error_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap4-err", res)

    def test_required_class(self):
        form = TestForm({"sender": "sender"})
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-req", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        res = render_template_with_form(
            '{% bootstrap_form form required_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap4-req", res)

    def test_bound_class(self):
        form = TestForm({"sender": "sender"})

        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn("bootstrap4-bound", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form(
            '{% bootstrap_form form bound_css_class="successful-test" %}',
            {"form": form},
        )
        self.assertIn("successful-test", res)

        form = TestForm({"sender": "sender"})

        res = render_template_with_form(
            '{% bootstrap_form form bound_css_class="" %}', {"form": form}
        )
        self.assertNotIn("bootstrap4-bound", res)

    def test_radio_select_button_group(self):
        form = TestForm()
        res = render_template_with_form("{% bootstrap_form form %}", {"form": form})
        self.assertIn('input type="radio" name="category5" id="id_category5_0_0"', res)


class FieldTest(TestCase):
    def test_illegal_field(self):
        with self.assertRaises(BootstrapError):
            render_field(field="illegal")

    def test_show_help(self):
        res = render_form_field("subject")
        self.assertIn("my_help_text", res)
        self.assertNotIn("<i>my_help_text</i>", res)
        res = render_template_with_form(
            "{% bootstrap_field form.subject show_help=0 %}"
        )
        self.assertNotIn("my_help_text", res)

    def test_help_with_quotes(self):
        # Checkboxes get special handling, so test a checkbox and something else
        res = render_form_field("sender")
        self.assertIn(
            'title="{}"'.format(escape(TestForm.base_fields["sender"].help_text)), res
        )
        res = render_form_field("cc_myself")
        self.assertIn(
            'title="{}"'.format(escape(TestForm.base_fields["cc_myself"].help_text)),
            res,
        )

    def test_subject(self):
        res = render_form_field("subject")
        self.assertIn('type="text"', res)
        self.assertIn('placeholder="placeholdertest"', res)

    def test_xss_field(self):
        res = render_form_field("xss_field")
        self.assertIn('type="text"', res)
        self.assertIn(
            '<label for="id_xss_field">XSS&quot; onmouseover=&quot;alert(&#39;Hello, XSS&#39;)&quot; foo=&quot;</label>',
            res,
        )
        self.assertIn(
            'placeholder="XSS&quot; onmouseover=&quot;alert(&#39;Hello, XSS&#39;)&quot; foo=&quot;"',
            res,
        )

    def test_password(self):
        res = render_form_field("password")
        self.assertIn('type="password"', res)
        self.assertIn('placeholder="Password"', res)

    def test_checkbox(self):
        """Test Checkbox rendering, because it is special."""

        def _select_one_element(html, selector, err_msg):
            lst = html.select(selector)
            self.assertEqual(len(lst), 1, err_msg)
            return lst[0]

        res = render_form_field("cc_myself")
        # strip out newlines and spaces around newlines
        res = "".join(line.strip() for line in res.split("\n"))
        res = BeautifulSoup(res, "html.parser")
        form_group = _select_one_element(
            res, ".form-group", "Checkbox should be rendered inside a .form-group."
        )
        form_check = _select_one_element(
            form_group,
            ".form-check",
            "There should be a .form-check inside .form-group",
        )
        checkbox = _select_one_element(
            form_check, "input", "The checkbox should be inside the .form-check"
        )
        self.assertIn(
            "form-check-input",
            checkbox["class"],
            "The checkbox should have the class 'form-check-input'.",
        )
        label = checkbox.nextSibling
        self.assertIsNotNone(label, "The label should be rendered after the checkbox.")
        self.assertEqual(
            label.name, "label", "After the checkbox there should be a label."
        )
        self.assertEqual(
            label["for"],
            checkbox["id"],
            "The for attribute of the label should be the id of the checkbox.",
        )
        help_text = label.nextSibling
        self.assertIsNotNone(
            help_text, "The help text should be rendered after the label."
        )
        self.assertEqual(
            help_text.name, "small", "The help text should be rendered as <small> tag."
        )
        self.assertIn(
            "form-text",
            help_text["class"],
            "The help text should have the class 'form-text'.",
        )
        self.assertIn(
            "text-muted",
            help_text["class"],
            "The help text should have the class 'text-muted'.",
        )

    def test_required_field(self):
        required_css_class = "bootstrap4-req"
        required_field = render_form_field("subject")
        self.assertIn(required_css_class, required_field)
        not_required_field = render_form_field("message")
        self.assertNotIn(required_css_class, not_required_field)
        # Required settings in field
        form_field = "form.subject"
        rendered = render_template_with_form(
            "{% bootstrap_field "
            + form_field
            + ' required_css_class="test-required" %}'
        )
        self.assertIn("test-required", rendered)

    def test_empty_permitted(self):
        """
        If a form has empty_permitted, no fields should get the CSS class for required.
        """
        required_css_class = "bootstrap4-req"
        form = TestForm()
        res = render_form_field("subject", {"form": form})
        self.assertIn(required_css_class, res)
        form.empty_permitted = True
        res = render_form_field("subject", {"form": form})
        self.assertNotIn(required_css_class, res)

    def test_input_group(self):
        res = render_template_with_form(
            '{% bootstrap_field form.subject addon_before="$"  addon_after=".00" %}'
        )
        self.assertIn('class="input-group"', res)
        self.assertIn(
            'class="input-group-prepend"><span class="input-group-text">$', res
        )
        self.assertIn(
            'class="input-group-append"><span class="input-group-text">.00', res
        )

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
        self.assertIn(
            '<div class="input-group-append"><span class="input-group-text">after</span></div>',
            res,
        )

    def test_size(self):
        def _test_size(param, klass):
            res = render_template_with_form(
                '{% bootstrap_field form.subject size="' + param + '" %}'
            )
            self.assertIn(klass, res)

        def _test_size_medium(param):
            res = render_template_with_form(
                '{% bootstrap_field form.subject size="' + param + '" %}'
            )
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
        res = render_template_with_form(
            '{% bootstrap_label "foobar" label_for="subject" %}'
        )
        self.assertEqual('<label for="subject">foobar</label>', res)

    def test_attributes_consistency(self):
        form = TestForm()
        attrs = form.fields["addon"].widget.attrs.copy()
        self.assertEqual(attrs, form.fields["addon"].widget.attrs)


class ComponentsTest(TestCase):
    def test_alert(self):
        res = render_template_with_form(
            '{% bootstrap_alert "content" alert_type="danger" %}'
        )
        self.assertEqual(
            res.strip(),
            '<div class="alert alert-danger alert-dismissable" role="alert">'
            + '<button type="button" class="close" data-dismiss="alert" '
            + 'aria-label="close">'
            + "&times;</button>content</div>",
        )


class MessagesTest(TestCase):
    def test_messages(self):
        class FakeMessage(object):
            """
            Follows the `django.contrib.messages.storage.base.Message` API.
            """

            level = None
            message = None
            extra_tags = None

            def __init__(self, level, message, extra_tags=None):
                self.level = level
                self.extra_tags = extra_tags
                self.message = message

            def __str__(self):
                return self.message

        pattern = re.compile(r"\s+")
        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.WARNING, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-warning alert-dismissable fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
"""
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [FakeMessage(None, "hello")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello
    </div>
        """

        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))

        messages = [
            FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello http://example.com")
        ]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert" aria-label="close">&#215;</button>
        hello http://example.com
    </div>        """
        self.assertEqual(
            re.sub(pattern, "", res).replace('rel="nofollow"', ""),
            re.sub(pattern, "", expected).replace('rel="nofollow"', ""),
        )

        messages = [FakeMessage(DEFAULT_MESSAGE_LEVELS.ERROR, "hello\nthere")]
        res = render_template_with_form(
            "{% bootstrap_messages messages %}", {"messages": messages}
        )
        expected = """
    <div class="alert alert-danger alert-dismissable fade show" role="alert">
        <button type="button" class="close" data-dismiss="alert"
            aria-label="close">&#215;</button>
        hello there
    </div>
        """
        self.assertEqual(re.sub(pattern, "", res), re.sub(pattern, "", expected))


class UtilsTest(TestCase):
    def test_add_css_class(self):
        css_classes = "one two"
        css_class = "three four"
        classes = add_css_class(css_classes, css_class)
        self.assertEqual(classes, "one two three four")

        classes = add_css_class(css_classes, css_class, prepend=True)
        self.assertEqual(classes, "three four one two")

    def test_text_value(self):
        self.assertEqual(text_value(""), "")
        self.assertEqual(text_value(" "), " ")
        self.assertEqual(text_value(None), "")
        self.assertEqual(text_value(1), "1")

    def test_text_concat(self):
        self.assertEqual(text_concat(1, 2), "12")
        self.assertEqual(text_concat(1, 2, separator="="), "1=2")
        self.assertEqual(text_concat(None, 2, separator="="), "2")

    def test_render_tag(self):
        self.assertEqual(render_tag("span"), "<span></span>")
        self.assertEqual(render_tag("span", content="foo"), "<span>foo</span>")
        self.assertEqual(
            render_tag("span", attrs={"bar": 123}, content="foo"),
            '<span bar="123">foo</span>',
        )


class ButtonTest(TestCase):
    def test_button(self):
        res = render_template_with_form("{% bootstrap_button 'button' size='lg' %}")
        self.assertEqual(
            res.strip(), '<button class="btn btn-default btn-lg">button</button>'
        )

        link_button = (
            '<a class="btn btn-default btn-lg" href="#" role="button">button</a>'
        )

        res = render_template_with_form(
            "{% bootstrap_button 'button' size='lg' href='#' %}"
        )
        self.assertIn(res.strip(), link_button)
        res = render_template_with_form(
            "{% bootstrap_button 'button' button_type='link' size='lg' href='#' %}"
        )
        self.assertIn(res.strip(), link_button)
        with self.assertRaises(BootstrapError):
            res = render_template_with_form(
                "{% bootstrap_button 'button' button_type='button' href='#' %}"
            )


class ShowLabelTest(TestCase):
    def test_show_label(self):
        form = TestForm()
        res = render_template_with_form(
            "{% bootstrap_form form show_label=False %}", {"form": form}
        )
        self.assertIn("sr-only", res)

    def test_for_formset(self):
        TestFormSet = formset_factory(TestForm, extra=1)
        test_formset = TestFormSet()
        res = render_template_with_form(
            "{% bootstrap_formset formset show_label=False %}",
            {"formset": test_formset},
        )
        self.assertIn("sr-only", res)


class PaginatorTest(TestCase):
    def test_url_replace_param(self):
        self.assertEqual(
            url_replace_param("/foo/bar?baz=foo", "baz", "yohoo"), "/foo/bar?baz=yohoo"
        )
        self.assertEqual(url_replace_param("/foo/bar?baz=foo", "baz", None), "/foo/bar")
        self.assertEqual(
            url_replace_param("/foo/bar#id", "baz", "foo"), "/foo/bar?baz=foo#id"
        )

    def bootstrap_pagination(self, page, extra=""):
        """Helper to test bootstrap_pagination tag"""
        template = """
            {% load bootstrap4 %}
            {% bootstrap_pagination page {extra} %}
        """.replace(
            "{extra}", extra
        )

        return render_template(template, {"page": page})

    def test_paginator(self):
        objects = ["john", "paul", "george", "ringo"]
        p = Paginator(objects, 2)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/?foo=bar"')
        # order in dicts is not guaranteed in some python versions,
        # so we have to check both options
        self.assertTrue(
            "/projects/?foo=bar&page=1" in res or "/projects/?page=1&foo=bar" in res
        )
        self.assertTrue(
            "/projects/?foo=bar&page=3" not in res
            and "/projects/?page=3&foo=bar" not in res
        )

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/#id"')
        self.assertTrue("/projects/?page=1#id" in res)

        res = self.bootstrap_pagination(p.page(2), extra='url="/projects/?page=3#id"')
        self.assertTrue("/projects/?page=1#id" in res)

        res = self.bootstrap_pagination(
            p.page(2), extra='url="/projects/?page=3" extra="id=20"'
        )
        self.assertTrue(
            "/projects/?page=1&id=20" in res or "/projects/?id=20&page=1" in res
        )
