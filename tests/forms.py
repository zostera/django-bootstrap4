from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime
from django.contrib.gis import forms as gisforms

from bootstrap4.widgets import RadioSelectButtonGroup

RADIO_CHOICES = (("1", "Radio 1"), ("2", "Radio 2"))

MEDIA_CHOICES = (
    ("Audio", (("vinyl", "Vinyl"), ("cd", "CD"))),
    ("Video", (("vhs", "VHS Tape"), ("dvd", "DVD"))),
    ("unknown", "Unknown"),
)


class CharFieldTestForm(forms.Form):
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
    )


class TestForm(forms.Form):
    """Form with a variety of widgets to test bootstrap4 rendering."""

    date = forms.DateField(required=False)
    datetime = forms.SplitDateTimeField(widget=AdminSplitDateTime(), required=False)
    subject = forms.CharField(
        max_length=100,
        help_text="my_help_text",
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "placeholdertest"}),
    )
    xss_field = forms.CharField(label='XSS" onmouseover="alert(\'Hello, XSS\')" foo="', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text="<i>my_help_text</i>")
    sender = forms.EmailField(label="Sender © unicode", help_text='E.g., "me@example.com"')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False, help_text='cc stands for "carbon copy." You will get a copy in your mailbox.'
    )
    select1 = forms.ChoiceField(choices=RADIO_CHOICES)
    select2 = forms.MultipleChoiceField(choices=RADIO_CHOICES, help_text="Check as many as you like.")
    select3 = forms.ChoiceField(choices=MEDIA_CHOICES)
    select4 = forms.MultipleChoiceField(choices=MEDIA_CHOICES, help_text="Check as many as you like.")
    category1 = forms.ChoiceField(choices=RADIO_CHOICES, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=RADIO_CHOICES, widget=forms.CheckboxSelectMultiple, help_text="Check as many as you like."
    )
    category3 = forms.ChoiceField(widget=forms.RadioSelect, choices=MEDIA_CHOICES)
    category4 = forms.MultipleChoiceField(
        choices=MEDIA_CHOICES, widget=forms.CheckboxSelectMultiple, help_text="Check as many as you like."
    )
    category5 = forms.ChoiceField(widget=RadioSelectButtonGroup, choices=MEDIA_CHOICES)
    addon = forms.CharField(widget=forms.TextInput(attrs={"addon_before": "before", "addon_after": "after"}))
    polygon = gisforms.PointField()

    required_css_class = "bootstrap4-req"
    non_field_error_message = "This is a non field error."

    # Set this to allow tests to work properly in Django 1.10+
    # More information, see issue #337
    use_required_attribute = False

    def clean(self):
        super().clean()
        raise forms.ValidationError(self.non_field_error_message)


class TestFormWithoutRequiredClass(TestForm):
    required_css_class = ""
