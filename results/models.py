from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Goal(models.Model):
    green_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    seconds_goal = models.IntegerField(default=0)
    champs_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    mention_goal = models.IntegerField(default=0)
    five_bells_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    dissat_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    star_goal = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    @property
    def points(self):
        return GreenRed.objects.count()

    def get_absolute_url(self):     #not used***
        return reverse('results-detail', kwargs={'pk': self.pk})

class Updated(models.Model):
    update_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_updated = models.DateTimeField(auto_now=True)

    @property
    def updates(self):
        return Updated.objects.filter(id=1).get()


class GreenRed(models.Model):
    red = models.IntegerField(default=0)
    green= models.IntegerField(default=0)
    total_dayparts = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name

        


class Second(models.Model):
    seconds = models.IntegerField(default=0)
    seconds_avg = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_dayparts = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name

        


class Champ(models.Model):
    shift = models.IntegerField(default=0)
    champs = models.IntegerField(default=0)
    champs_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name

        
class Mention(models.Model):
    mention = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    manager = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name

        
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

    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name


class Stars(models.Model):
    manager = models.ForeignKey(User, on_delete=models.CASCADE)
    stars_total = models.IntegerField(default=0)
    stars_avg = models.DecimalField(max_digits=3, decimal_places=2,default=0)
    green_stars = models.IntegerField(default=0)
    second_stars = models.IntegerField(default=0)
    champ_stars = models.IntegerField(default=0)
    mention_stars = models.IntegerField(default=0)
    fivebell_stars = models.IntegerField(default=0)
    dissat_stars = models.IntegerField(default=0)
    green_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.manager.first_name
    
    def __str__(name) -> str:
        return name.manager.first_name

