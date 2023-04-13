from django import forms
from .models import *
from .widgets import *

HR = (
    ('', 'Choose...'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
)

HR_DUR = (
    ('', 'Choose...'),
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
    ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'),
)

MIN = (
    ('', 'Choose...'),
    ('00', '00'),
    ('15', '15'),
    ('30', '30'),
    ('45', '45'),
)

AMPM = (
    ('AM', 'AM'),
    ('PM', 'PM'),
)

WEEKS = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)

OCCUR = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
    ('11', '11'),
    ('12', '12'),
    ('13', '13'),
    ('14', '14'),
    ('15', '15'),
    ('16', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'),
)

REPEAT_OPTIONS = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('biweekly', 'Biweekly'),
    ('monthly', 'Monthly')
)


class AddressFormModel(forms.ModelForm):
    start_hour = forms.ChoiceField(choices=HR)
    start_minute = forms.ChoiceField(choices=MIN)
    duration_hour = forms.ChoiceField(choices=HR_DUR)
    duration_minute = forms.ChoiceField(choices=MIN)
    ampm = forms.ChoiceField(choices=AMPM)
    recur_check = forms.BooleanField(required=False)
    start_date = forms.DateTimeField(widget=forms.DateInput(  # DateTimeInput
        # "type": "datetime-local"
        attrs={"type": "date", "class": "form-control"},
        format="%Y-%m-%d",
    ))
    repeat_weeks = forms.ChoiceField(choices=WEEKS, required=False)
    sun = forms.BooleanField(required=False)
    mon = forms.BooleanField(required=False)
    tue = forms.BooleanField(required=False)
    wed = forms.BooleanField(required=False)
    thu = forms.BooleanField(required=False)
    fri = forms.BooleanField(required=False)
    sat = forms.BooleanField(required=False)
    end_date_check = forms.BooleanField(required=False)
    end_date = forms.DateTimeField(widget=forms.DateInput(  # DateTimeInput
        # "type": "datetime-local"
        attrs={"type": "date", "class": "form-control"},
        format="%Y-%m-%d",
    ), required=False)
    occurences_check = forms.BooleanField(required=False)
    occurences = forms.ChoiceField(choices=OCCUR, required=False)
    recur_options = forms.ChoiceField(choices=REPEAT_OPTIONS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_hour'].label = "Hour"
        self.fields['start_minute'].label = "Minute"
        self.fields['start_date'].label = "Date"
        self.fields['ampm'].label = "AM/PM"
        self.fields['duration_hour'].label = "Hour"
        self.fields['duration_minute'].label = "Minute"
        self.fields['repeat_weeks'].label = "Repeat every ? week(s)"
        self.fields['end_date'].label = ""
        self.fields['occurences'].label = ""
        self.fields['end_date_check'].label = ""
        self.fields['occurences_check'].label = ""

    class Meta:
        model = Testz
        fields = ['date_string']
