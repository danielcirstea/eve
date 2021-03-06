# Generated by Django 2.0.1 on 2018-02-26 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0013_auto_20180223_1823'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='enroll_slug',
            field=models.SlugField(default=None, max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(max_length=150, unique=True),
        ),
    ]
