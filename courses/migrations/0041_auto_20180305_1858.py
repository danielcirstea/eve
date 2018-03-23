# Generated by Django 2.0.1 on 2018-03-05 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0040_auto_20180302_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='Control',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='studentdata',
            name='enrolled',
        ),
        migrations.AlterField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(to='courses.StudentData'),
        ),
        migrations.AlterField(
            model_name='studentfileupload',
            name='files',
            field=models.FileField(default='', upload_to='student_files'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='control',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses.Course'),
        ),
    ]
