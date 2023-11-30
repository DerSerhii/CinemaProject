# Generated by Django 4.0.6 on 2023-10-07 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0003_delete_spectatorprofile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='showtime',
            options={'ordering': ('start',), 'verbose_name': 'showtime', 'verbose_name_plural': 'showtimes'},
        ),
        migrations.AddField(
            model_name='screenhall',
            name='slug',
            field=models.SlugField(default='slug', max_length=20, verbose_name='slug'),
            preserve_default=False,
        ),
    ]