# Generated by Django 2.0.1 on 2018-02-21 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_studyprogramme_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faculty',
            old_name='slug',
            new_name='faculty_slug',
        ),
        migrations.RenameField(
            model_name='studyprogramme',
            old_name='slug',
            new_name='study_programme_slug',
        ),
    ]
