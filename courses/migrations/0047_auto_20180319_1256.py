# Generated by Django 2.0.1 on 2018-03-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0046_auto_20180318_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
