from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Codes(models.Model):
    code_id = models.IntegerField(primary_key=True)
    points = models.IntegerField(default=0)
    title = models.CharField(max_length=20, default="", unique=True)
    info = models.TextField(blank=True, null=True, default="")
    
    def __str__(name) -> str:
        return name.title

class Attendance(models.Model):
    date = models.DateField()
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.ForeignKey(Codes, to_field='title', on_delete=models.PROTECT)
    points = models.IntegerField()
    notes = models.TextField(blank=True, default="")
    entered_by = models.CharField(max_length=20)
    entered_on = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('absence-detail', kwargs={'pk': self.pk})

    def __str__(name) -> str:
        return name.employee.first_name + " " + name.employee.last_name + " - " + str(name.code.title) + " on " + str(name.date)