# Generated by Django 2.0.1 on 2018-02-27 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0019_auto_20180227_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='study_programme',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='courses.StudyProgramme'),
        ),
    ]
