# Generated by Django 4.0.6 on 2023-10-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_alter_showtime_options_screenhall_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='screenhall',
            name='slug',
            field=models.SlugField(max_length=20, unique=True, verbose_name='slug'),
        ),
    ]