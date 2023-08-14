# Generated by Django 4.0.6 on 2022-09-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0007_showtime_end_showtime_start'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='showtime',
            options={'ordering': ('start',), 'verbose_name': 'Showtime', 'verbose_name_plural': 'Showtimes'},
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='date',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='time_end',
        ),
        migrations.RemoveField(
            model_name='showtime',
            name='time_start',
        ),
        migrations.AlterField(
            model_name='showtime',
            name='end',
            field=models.DateTimeField(verbose_name='Showtime end time'),
        ),
        migrations.AlterField(
            model_name='showtime',
            name='start',
            field=models.DateTimeField(verbose_name='Showtime start time'),
        ),
    ]