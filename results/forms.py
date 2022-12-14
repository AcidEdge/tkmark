from django import forms
from .models import Goal, GreenRed, Second, Champ, Mention, Survey

class GoalsForm(forms.ModelForm):
    class Meta:
        model=Goal
        fields=['green_goal', 'seconds_goal', 'champs_goal', 'mention_goal', 'five_bells_goal', 'dissat_goal', 'star_goal']
        labels = {'green_goal': 'Green Dayparts %', 'seconds_goal': 'Avg Seconds vs Goal', 'champs_goal': 'Champs Cards %', 
            'mention_goal': 'Survey Name Mentions', 'five_bells_goal': 'Five Bells %', 'dissat_goal': 'Dissat %', 'star_goal': '5 Star Goal'}

class GreenUpdate(forms.ModelForm):
    class Meta:
        model=GreenRed
        fields=['manager', 'green', 'red']
        labels={'manager': 'Select Manager', 'green': "# of Green Dayparts", 'red': "# of Red Dayparts"}


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
        labels={'mention': '# of Survey Mentions'}


class SurveyUpdate(forms.ModelForm):
    class Meta:
        model=Survey
        fields=['fives', 'fours', 'threes', 'twos', 'ones']
        labels={'fives': "# of 5's Recieved", 'fours': "# of 4's Recieved", 'threes': "# of 3's Recieved",
                'twos': "# of 2's Recieved", 'ones': "# of 1's Recieved",}