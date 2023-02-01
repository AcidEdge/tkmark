from django import forms
from django.forms.widgets import NumberInput
from results.utilities import *


class AttendanceForm(forms.Form):
    date = forms.DateField(label='Select Date of absence:', widget=NumberInput(attrs={'type':'date'}))
    employee = forms.ChoiceField(choices=get_all_users(), label='Select Employee')
    type = forms.ChoiceField(choices=get_absence_types(), label="Select Absence Type")
    notes= forms.CharField(label="Absence Notes", help_text="Enter any additional/contributing\ninformation about the absence.", widget=forms.Textarea(attrs={"rows":3}), required=False)
