from django.forms import (
    RadioSelect,
    DateInput,
    DateTimeInput,
    TimeInput
)


class RadioSelectButtonGroup(RadioSelect):
    """
    This widget renders a Bootstrap 4 set of buttons horizontally instead of typical radio buttons.

    Much more mobile friendly.
    """

    template_name = "bootstrap4/widgets/radio_select_button_group.html"


class DateWidget(DateInput):
    """
    This widget renders a HML5 date field type and enables date picker.
    """

    input_type = "date"

    def format_value(self, value):
        return str(value or '')


class DateTimeWidget(DateTimeInput):
    """
    This widget renders a HML5 datetime-local field type and enables date and time picker.
    """

    input_type = "datetime-local"
    template_name = "bootstrap4/widgets/datetime_field.html"

    def format_value(self, value):
        return 'T'.join(str(value or '').split())


class TimeWidget(TimeInput):
    """
    This widget renders a HML5 time field type and enables time picker.
    """

    input_type = "time"
