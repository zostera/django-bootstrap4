from django.template import engines

from bootstrap4.utils import DJANGO_VERSION

from .forms import TestForm


def render_template_with_form(text, context=None, data=None):
    """
    Create a template ``text`` that first loads bootstrap4.

    When ``data`` is given, the form will be initialized with data and
    form.is_valid() will be called in order to enable validations.
    """
    if not context:
        context = {}
    if "form" not in context:
        form = TestForm(data=data)
        if data:
            form.is_valid()
        context["form"] = form
    return render_template_with_bootstrap(text, context)


def render_formset(formset=None, context=None):
    """Create a template that renders a formset."""
    if not context:
        context = {}
    context["formset"] = formset
    return render_template_with_form("{% bootstrap_formset formset %}", context)


def render_form(form=None, context=None):
    """Create a template that renders a form."""
    if not context:
        context = {}
    if form:
        context["form"] = form
    return render_template_with_form("{% bootstrap_form form %}", context)


def render_form_field(field, context=None):
    """Create a template that renders a field."""
    form_field = "form.%s" % field
    return render_template_with_form("{% bootstrap_field " + form_field + " %}", context)


def render_field(field, context=None):
    """Create a template that renders a field."""
    if not context:
        context = {}
    context["field"] = field
    return render_template_with_form("{% bootstrap_field field %}", context)


def html_39x27(html):
    """
    Return HTML string with &#39; (Django < 3) instead of &#x27; (Django >= 3).

    See https://docs.djangoproject.com/en/dev/releases/3.0/#miscellaneous
    """
    if DJANGO_VERSION < 3:
        return html.replace("&#x27;", "&#39;")
    return html


def render_template(text, context=None):
    """Create a template ``text`` that first loads bootstrap4."""
    template = engines["django"].from_string(text)
    if not context:
        context = {}
    return template.render(context)


def render_template_with_bootstrap(text, context=None):
    """Create a template ``text`` that first loads bootstrap4."""
    if not context:
        context = {}
    return render_template("{% load bootstrap4 %}" + text, context)
