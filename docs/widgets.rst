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



DateTimeWidget
~~~~~~~~~~~~~~~~~~~~~~

This renders a form DateTimeField as a input of type datetime-local.

.. code:: django

    from bootstrap4.widgets import DateTimeWidget

    class MyForm(forms.Form):
        media_type = forms.DateTimeField(
            help_text="Pick a Date and Time",
            required=True,
            label="Schedule:",
            widget=DateTimeWidget,
            initial=datetime.now(),
        )


DateWidget
~~~~~~~~~~~~~~~~~~~~~~

This renders a form DateField as a input of type date.

.. code:: django

    from bootstrap4.widgets import DateWidget

    class MyForm(forms.Form):
        media_type = forms.DateField(
            help_text="Enter your bird day",
            required=True,
            label="Bird Day:",
            widget=DateWidget,
            initial=date.today(),
        )


TimeWidget
~~~~~~~~~~~~~~~~~~~~~~

This renders a form TimeField as a input of type time.

.. code:: django

    from bootstrap4.widgets import TimeWidget

    class MyForm(forms.Form):
        media_type = forms.TimeField(
            help_text="Pick a time:",
            required=True,
            label="Time:",
            widget=TimeWidget,
            initial=datetime.now().time(),
        )
