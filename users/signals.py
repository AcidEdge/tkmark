from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from results.models import GreenRed, Second, Champ, Mention, Survey, Stars


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        GreenRed.objects.create(red=0, green=0, total_dayparts=0, green_percent=0, manager=instance)
        Second.objects.create(seconds=0, seconds_avg=0, total_dayparts=0, manager=instance)
        Champ.objects.create(shift=0, champs=0, champs_percent=0, manager=instance)
        Mention.objects.create(mention=0, manager=instance)
        Survey.objects.create(ones=0, twos=0, threes=0, fours=0, fives=0, five_bells=0, dissat=0, manager=instance)
        Stars.objects.create(manager=instance, stars_total=0, stars_avg=0, green_stars=0, second_stars=0, 
                                champ_stars=0, mention_stars=0, fivebell_stars=0, dissat_stars=0)
        


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
