import tempfile

from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from tests.base import BootstrapTestCase
from tests.image import get_test_image


class FileFieldTestForm(forms.Form):
    test = forms.FileField()


class ClearableFileInputTestForm(forms.Form):
    test = forms.FileField(widget=forms.ClearableFileInput, required=False)


class ImageFieldTestForm(forms.Form):
    test = forms.ImageField()


class InputTypeFileTestCase(BootstrapTestCase):
    def test_input_type_file(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": FileFieldTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": ClearableFileInputTestForm()}),
            (
                '<div class="mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" type="file">'
                "</div>"
            ),
        )

    def test_clearable_file_input_post(self):
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test %}",
                context={"form": ClearableFileInputTestForm({}, {"test": SimpleUploadedFile("test.txt", b"test")})},
            ),
            (
                '<div class="django_bootstrap5-success mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" class="form-control is-valid" id="id_test">'
                "</div>"
            ),
        )

    def test_image_field(self):
        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": ImageFieldTestForm()}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input accept="image/*" class="form-control" id="id_test" name="test" required type="file">'
                "</div>"
            ),
        )

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_image_field_post(self):
        form = ImageFieldTestForm({}, {"test": get_test_image()})
        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test %}",
                context={"form": form},
            ),
            (
                '<div class="django_bootstrap5-success django_bootstrap5-req mb-3">'
                '<label class="form-label" for="id_test">Test</label>'
                '<input type="file" name="test" accept="image/*" class="form-control is-valid"'
                ' required id="id_test">'
                "</div>"
            ),
        )
