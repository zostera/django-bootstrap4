=======
Widgets
=======

A form widget is available for displaying radio buttons as a Bootstrap 4 button group(https://getbootstrap.com/docs/4.5/components/button-group/).


RadioSelectButtonGroup
~~~~~~~~~~~~~~~~~~~~~~

This renders a form ChoiceField as a Bootstrap 4 button group in the `primary` Bootstrap 4 color.

.. code:: django

    from bootstrap4.widgets import RadioSelectButtonGroup

    class MyForm(forms.Form):
        media_type = forms.ChoiceField(
            help_text="Select the order type.",
            required=True,
            label="Order Type:",
            widget=RadioSelectButtonGroup,
            choices=((1, 'Vinyl'), (2, 'Compact Disc')),
            initial=1,
        )
