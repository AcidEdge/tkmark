# Generated by Django 4.1.3 on 2023-01-20 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0021_stars_audit_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selfaudit',
            name='completed',
            field=models.IntegerField(default=0),
        ),
    ]
