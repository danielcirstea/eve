# Generated by Django 2.0.1 on 2018-02-22 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20180222_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecture',
            name='lecture_category',
            field=models.CharField(choices=[('Courses', 'Courses'), ('Seminars', 'Seminars')], default='Courses', max_length=10),
        ),
    ]
