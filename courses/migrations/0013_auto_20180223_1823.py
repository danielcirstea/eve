# Generated by Django 2.0.1 on 2018-02-23 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0012_auto_20180223_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='teacher1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='course_course_teacher', to='courses.TeacherData', verbose_name='Course Teacher'),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_seminar_teacher', to='courses.TeacherData', verbose_name='Seminar Teacher'),
        ),
    ]
