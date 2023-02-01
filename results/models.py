from django.db import models
from django.contrib.auth.models import User
from .utilities import period_choices, p1




class Goal(models.Model):
    green_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    seconds_goal = models.IntegerField(default=0)
    champs_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    mention_goal = models.IntegerField(default=0)
    five_bells_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dissat_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    star_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    zenput_goal = models.IntegerField(default=0)
    audit_goal = models.IntegerField(default=0)
    
    def __str__(name) -> str:
        return "Star Goals"

    @property
    def points(self): # no longer used????
        return GreenRed.objects.count()


class Updated(models.Model):
    update_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def updates(self):
        return Updated.objects.filter(id=1).get()

class Period(models.Model):
    period = models.IntegerField(unique=True, choices=period_choices)
    start_date = models.DateField()
    end_date = models.DateField()


class GreenRed(models.Model):
    red = models.IntegerField(default=0)
    green= models.IntegerField(default=0)
    total_dayparts = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)

    def __str__(self) -> str:
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)


        


class Second(models.Model):
    seconds = models.IntegerField(default=0)
    seconds_avg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_dayparts = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)


    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)

        


class Champ(models.Model):
    shift = models.IntegerField(default=0)
    champs = models.IntegerField(default=0)
    champs_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name  + " Period " + str(name.period)

        
class Mention(models.Model):
    mention = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)

        
class Survey(models.Model):
    ones = models.IntegerField(default=0)
    twos = models.IntegerField(default=0)
    threes = models.IntegerField(default=0)
    fours = models.IntegerField(default=0)
    fives = models.IntegerField(default=0)
    five_bells = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dissat = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)


class Stars(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    stars_total = models.IntegerField(default=0)
    stars_avg = models.DecimalField(max_digits=3, decimal_places=2,default=0)
    green_stars = models.IntegerField(default=0)
    second_stars = models.IntegerField(default=0)
    champ_stars = models.IntegerField(default=0)
    mention_stars = models.IntegerField(default=0)
    dissat_stars = models.IntegerField(default=0)
    zenput_stars = models.IntegerField(default=0)
    audit_stars = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    period = models.IntegerField(choices=period_choices, default=p1)
    
    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)


class SOS(models.Model):
    date = models.DateField(primary_key=True)
    breakfast = models.TimeField(blank=True, null=True)
    lunch = models.TimeField(blank=True, null=True)
    snack = models.TimeField(blank=True, null=True)
    dinner = models.TimeField(blank=True, null=True)
    evening = models.TimeField(blank=True, null=True)
    close = models.TimeField(blank=True, null=True)
    day = models.TimeField(blank=True, null=True)

    def __str__(date) -> str:
        return str(date.date) 

class Zenput(models.Model):
    missed = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)


class Audits(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    period = models.IntegerField(choices=period_choices, default=p1)
    completed = models.IntegerField(default=0)
    
    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name + " Period " + str(name.period)


class Streak(models.Model):
    current = models.IntegerField(default=0)
    longest = models.IntegerField(default=0)

    def __str__(name) -> str:
        return "Current Daypart Streak: " + str(name.current)