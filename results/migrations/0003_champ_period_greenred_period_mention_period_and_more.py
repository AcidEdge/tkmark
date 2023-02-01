# Generated by Django 4.1.3 on 2022-12-26 16:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_period'),
    ]

    operations = [
        migrations.AddField(
            model_name='champ',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='greenred',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mention',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='second',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='stars',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='survey',
            name='period',
            field=models.ForeignKey(default=13, on_delete=django.db.models.deletion.RESTRICT, to='results.period', to_field='period'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='period',
            name='period',
            field=models.IntegerField(choices=[(1, 'Period 1'), (2, 'Period 2'), (3, 'Period 3'), (4, 'Period 4'), (5, 'Period 5'), (6, 'Period 6'), (7, 'Period 7'), (8, 'Period 8'), (9, 'Period 9'), (10, 'Period 10'), (11, 'Period 11'), (12, 'Period 12'), (13, 'Period 13')], unique=True),
        ),
    ]