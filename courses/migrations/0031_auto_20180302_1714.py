# Generated by Django 2.0.1 on 2018-03-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0030_auto_20180302_1700'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentfileupload',
            name='comment',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
