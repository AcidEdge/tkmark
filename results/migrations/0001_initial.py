# Generated by Django 4.1.3 on 2022-12-14 00:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('green_goal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('seconds_goal', models.IntegerField(default=0)),
                ('champs_goal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('mention_goal', models.IntegerField(default=0)),
                ('five_bells_goal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('dissat_goal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('star_goal', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Updated',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('update_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ones', models.IntegerField(default=0)),
                ('twos', models.IntegerField(default=0)),
                ('threes', models.IntegerField(default=0)),
                ('fours', models.IntegerField(default=0)),
                ('fives', models.IntegerField(default=0)),
                ('five_bells', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('dissat', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stars_total', models.IntegerField(default=0)),
                ('stars_avg', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('green_stars', models.IntegerField(default=0)),
                ('second_stars', models.IntegerField(default=0)),
                ('champ_stars', models.IntegerField(default=0)),
                ('mention_stars', models.IntegerField(default=0)),
                ('fivebell_stars', models.IntegerField(default=0)),
                ('dissat_stars', models.IntegerField(default=0)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Second',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seconds', models.IntegerField(default=0)),
                ('seconds_avg', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('total_dayparts', models.IntegerField(default=0)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mention', models.IntegerField(default=0)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GreenRed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('red', models.IntegerField(default=0)),
                ('green', models.IntegerField(default=0)),
                ('total_dayparts', models.IntegerField(default=0)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Champ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shift', models.IntegerField(default=0)),
                ('champs', models.IntegerField(default=0)),
                ('champs_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('green_percent', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
