from django import forms

from tests.base import BootstrapTestCase


class TestForm(forms.Form):
    subject = forms.CharField(required=True)
    date = forms.DateField()


TestFormSet = forms.formset_factory(TestForm)


class BootstrapFormSetTestCase(BootstrapTestCase):
    def test_formset(self):
        formset = TestFormSet()
        html = self.render("{% bootstrap_formset formset %}", {"formset": formset})
        self.assertHTMLEqual(
            html,
            """
<input type="hidden" name="form-TOTAL_FORMS" value="1" id="id_form-TOTAL_FORMS">
<input type="hidden" name="form-INITIAL_FORMS" value="0" id="id_form-INITIAL_FORMS">
<input type="hidden" name="form-MIN_NUM_FORMS" value="0" id="id_form-MIN_NUM_FORMS">
<input type="hidden" name="form-MAX_NUM_FORMS" value="1000" id="id_form-MAX_NUM_FORMS">
<div class="mb-3">
<label class="form-label" for="id_form-0-subject">Subject</label>
<input type="text" name="form-0-subject" class="form-control" placeholder="Subject" id="id_form-0-subject">
</div>
<div class="mb-3">
<label class="form-label" for="id_form-0-date">Date</label>
<input type="text" name="form-0-date" class="form-control" placeholder="Date" id="id_form-0-date">
</div>
            """,
        )

    def test_formset_post(self):
        formset = TestFormSet({"form-TOTAL_FORMS": 1, "form-INITIAL_FORMS": 0})
        html = self.render("{% bootstrap_formset_errors formset %}", {"formset": formset})
        self.assertEqual(html, "")

    def test_illegal_formset(self):
        with self.assertRaises(TypeError):
            self.render("{% bootstrap_formset formset %}", {"formset": "illegal"})
