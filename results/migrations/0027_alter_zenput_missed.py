# Generated by Django 4.1.3 on 2023-01-29 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0026_alter_mention_mention_alter_zenput_missed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zenput',
            name='missed',
            field=models.IntegerField(default=0),
        ),
    ]
