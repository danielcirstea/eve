# Generated by Django 2.0.1 on 2018-03-20 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0048_auto_20180319_1940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='biography',
        ),
    ]
