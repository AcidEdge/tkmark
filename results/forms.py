from django import forms
from .models import Goal, Second, Champ, Mention, Survey, Period, Zenput, User
from django.forms.widgets import NumberInput
from .utilities import period_result_options
import datetime

def get_current_period():
    today = datetime.date.today()
    current_period = Period.objects.filter(start_date__lte=today, end_date__gte=today).get()
    return current_period.period

def get_managers():
    manager_choices = []
    for x in User.objects.filter(groups__name='manager').all():
            manager_choices.append((x.id, x.first_name+" "+x.last_name))
    return manager_choices

class GoalsForm(forms.ModelForm):
    class Meta:
        model=Goal
        fields=['star_goal', 'green_goal', 'seconds_goal', 'champs_goal', 'mention_goal', 'zenput_goal', 'dissat_goal', 'audit_goal']
        labels = {'star_goal': '5 Star Goal', 'green_goal': 'Green Dayparts %', 'seconds_goal': 'Avg Seconds vs Goal', 'champs_goal': 'Champs Cards %', 
            'mention_goal': '# of Loop Calls', 'zenput_goal': '# of missed zenputs', 'dissat_goal': 'Dissat %', 'audit_goal': '# of Self Audits per period'}

class GreenUpdate(forms.Form):
#    class Meta:
#        model=GreenRed
#        fields=['period', 'manager', 'green', 'red']
#        labels={'manager': 'Select Manager', 'green': "# of Green Dayparts", 'red': "# of Red Dayparts"}
    period = forms.ChoiceField(choices=period_result_options, label="Select Period:", initial=get_current_period())
    manager = forms.ChoiceField(choices=get_managers(), label='Select Manager:')
    green = forms.IntegerField(label="# of Green Dayparts:", initial=0)
    red = forms.IntegerField(label='# of Red Dayparts:', initial=0)



class SecondUpdate(forms.ModelForm):
    class Meta:
        model=Second
        fields=['seconds']
        labels={'seconds': 'Seconds +/- Goals'}


class ChampUpdate(forms.ModelForm):
        class Meta:
            model=Champ
            fields=['shift', 'champs']
            labels={'shift': '# of Shifts Worked', 'champs': "# of Champ's Cards Given"}


class MentionUpdate(forms.ModelForm):
    class Meta:
        model=Mention
        fields=['mention']
        labels={'mention': '# of Loop Calls'}


class SurveyUpdate(forms.ModelForm):
    class Meta:
        model=Survey
        fields=['fives', 'fours', 'threes', 'twos', 'ones']
        labels={'fives': "# of 5's Recieved", 'fours': "# of 4's Recieved", 'threes': "# of 3's Recieved",
                'twos': "# of 2's Recieved", 'ones': "# of 1's Recieved",}


class SOSUpdate(forms.Form):
    date = forms.DateField(label='Select Date:', widget=NumberInput(attrs={'type':'date'}))
    breakfast = forms.TimeField(label='Breakfast SOS:')
    brk_green = forms.BooleanField(label="Check if Green", required=False)
    lunch = forms.TimeField(label='Lunch SOS:')
    lunch_green = forms.BooleanField(label="Check if Green", required=False)
    snack = forms.TimeField(label='Snack SOS:')
    snack_green = forms.BooleanField(label="Check if Green", required=False)
    dinner = forms.TimeField(label='Dinner SOS:')
    dinner_green = forms.BooleanField(label="Check if Green", required=False)
    evening = forms.TimeField(label='Evening (8p-11p) SOS:')
    eve_green = forms.BooleanField(label="Check if Green", required=False)
    close = forms.TimeField(label='Close (11p-2a) SOS:')
    cl_green = forms.BooleanField(label="Check if Green", required=False)
    day = forms.TimeField(label='Total SOS for the Day:')

class ZenputUpdate(forms.ModelForm):
    class Meta:
        model=Zenput
        fields=['missed']
        labels={'missed':'# of missed zenputs'}
    

class SelfAuditUpdate(forms.Form):
    completed = forms.BooleanField(label='Check to enter Completed Self Audit', required=False)