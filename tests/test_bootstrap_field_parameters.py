from django import forms

from tests.base import BootstrapTestCase


class CharFieldTestForm(forms.Form):
    test = forms.CharField()


class BootstrapFieldParameterTestCase(BootstrapTestCase):
    """Test `bootstrap_field` parameters`."""

    def test_wrapper_class(self):
        """Test field with default CharField widget."""

        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test inline_wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req mb-3">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req foo">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test wrapper_class=None %}", context={"form": form}),
            (
                '<div class="django_bootstrap5-req">'
                '<label for="id_test" class="form-label">Test</label>'
                '<input class="form-control" id="id_test" name="test" placeholder="Test" required type="text">'
                "</div>"
            ),
        )

    def test_inline_wrapper_class(self):
        """Test field with default CharField widget."""

        form = CharFieldTestForm()

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='inline' %}", context={"form": form}),
            (
                '<div class="col-12 django_bootstrap5-req">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render("{% bootstrap_field form.test layout='inline' wrapper_class='foo' %}", context={"form": form}),
            (
                '<div class="col-12 django_bootstrap5-req">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )

        self.assertHTMLEqual(
            self.render(
                "{% bootstrap_field form.test layout='inline' inline_wrapper_class='foo' %}", context={"form": form}
            ),
            (
                '<div class="col-12 django_bootstrap5-req foo">'
                '<label class="visually-hidden" for="id_test">Test</label>'
                '<input type="text" name="test" class="form-control" placeholder="Test" required id="id_test">'
                "</div>"
            ),
        )
