# Generated by Django 4.1.3 on 2023-01-02 00:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_remove_stars_fivebell_stars'),
    ]

    operations = [
        migrations.CreateModel(
            name='SOS',
            fields=[
                ('date', models.DateField(primary_key=True, serialize=False)),
                ('breakfast', models.TimeField()),
                ('lunch', models.TimeField()),
                ('snack', models.TimeField()),
                ('dinner', models.TimeField()),
                ('evening', models.TimeField()),
                ('close', models.TimeField()),
            ],
        ),
    ]
