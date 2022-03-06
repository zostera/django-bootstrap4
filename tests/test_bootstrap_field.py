from django import forms

from .base import BootstrapTestCase, html_39x27


class XssTestForm(forms.Form):
    xss_field = forms.CharField(label='XSS" onmouseover="alert(\'Hello, XSS\')" foo="', max_length=100)


class SubjectTestForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"}),
    )


class FieldTestCase(BootstrapTestCase):
    def test_illegal_field(self):
        with self.assertRaises(TypeError):
            self.render("{% bootstrap_field field %}", {"field": "illegal"})

    def test_show_help(self):
        html = self.render("{% bootstrap_field form.subject %}", {"form": SubjectTestForm()})
        self.assertIn("my_help_text", html)
        self.assertNotIn("<i>my_help_text</i>", html)
        html = self.render("{% bootstrap_field form.subject show_help=False %}", {"form": SubjectTestForm()})
        self.assertNotIn("my_help_text", html)

    def test_placeholder(self):
        html = self.render("{% bootstrap_field form.subject %}", {"form": SubjectTestForm()})
        self.assertIn('type="text"', html)
        self.assertIn('placeholder="placeholdertest"', html)

    def test_xss_field(self):
        html = self.render("{% bootstrap_field form.xss_field %}", {"form": XssTestForm()})
        self.assertIn('type="text"', html)
        self.assertIn(html_39x27(">XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;<"), html)
        self.assertIn(
            html_39x27('placeholder="XSS&quot; onmouseover=&quot;alert(&#x27;Hello, XSS&#x27;)&quot; foo=&quot;"'), html
        )

    def test_empty_permitted(self):
        """If a form has empty_permitted, no fields should get the CSS class for required."""
        form = SubjectTestForm()

        html = self.render("{% bootstrap_field form.subject %}", {"form": form})
        self.assertIn("django_bootstrap5-req", html)

        form.empty_permitted = True
        html = self.render("{% bootstrap_field form.subject %}", {"form": form})
        self.assertNotIn("django_bootstrap5-req", html)

    def test_size(self):
        def _test_size(param, klass):
            html = self.render('{% bootstrap_field form.subject size="' + param + '" %}', {"form": SubjectTestForm()})
            self.assertIn(klass, html)

        def _test_size_medium(param):
            html = self.render('{% bootstrap_field form.subject size="' + param + '" %}', {"form": SubjectTestForm()})
            self.assertNotIn("form-control-lg", html)
            self.assertNotIn("form-control-sm", html)
            self.assertNotIn("form-control-md", html)

        _test_size("sm", "form-control-sm")
        _test_size("lg", "form-control-lg")
        _test_size_medium("md")
        _test_size_medium("")

    def test_label(self):
        self.assertEqual(
            self.render('{% bootstrap_label "foobar" label_for="subject" %}'),
            '<label for="subject">foobar</label>',
        )
