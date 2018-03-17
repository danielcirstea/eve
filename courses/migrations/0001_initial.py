# Generated by Django 2.0.1 on 2018-02-21 16:47

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_student', models.BooleanField(default=False)),
                ('is_teacher', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('ects', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99)])),
                ('description', models.TextField()),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99)])),
                ('semester', models.IntegerField(choices=[(1, '1'), (2, '2')], default=None)),
                ('slug', models.SlugField(max_length=140, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField(blank=True, default=None, max_length=140, null=True)),
            ],
            options={
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(blank=True, null=True, upload_to='documents')),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lecture_category', models.IntegerField(choices=[(0, 'Classes '), (1, 'Seminars')], default=None)),
                ('lecture_title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('course', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='lectures', to='courses.Course')),
            ],
        ),
        migrations.CreateModel(
            name='StudentData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=50)),
                ('student_ID', models.CharField(max_length=14, unique=True)),
                ('notes', models.CharField(blank=True, default=None, max_length=255)),
            ],
            options={
                'verbose_name': 'Student Data',
                'verbose_name_plural': 'Students Data',
            },
        ),
        migrations.CreateModel(
            name='StudyProgramme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('studies_type', models.IntegerField(choices=[(0, 'Bachelor Studies'), (1, 'Master Studies'), (2, 'Doctoral Studies'), (3, 'Integrated Studies')], default=0)),
                ('duration', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(99)])),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Department')),
            ],
            options={
                'verbose_name': 'Study Programme',
                'verbose_name_plural': 'Study Programmes',
            },
        ),
        migrations.CreateModel(
            name='TeacherData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('surname', models.CharField(max_length=50)),
                ('teacher_ID', models.CharField(max_length=14, unique=True)),
                ('notes', models.CharField(blank=True, default=None, max_length=255)),
            ],
            options={
                'verbose_name': 'Teacher Data',
                'verbose_name_plural': 'Teachers Data',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('surname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('student_ID', models.CharField(blank=True, default=None, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='The ID needs to be 14 characters long.', regex='^.{14}$')])),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='students_images')),
                ('phone', models.CharField(blank=True, default=None, max_length=15, null=True, validators=[django.core.validators.RegexValidator(message='Not a valid phone number.', regex='^[a-zA-Z0-9+]+$')])),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('name', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('surname', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('email', models.EmailField(blank=True, default=None, max_length=254, null=True, unique=True)),
                ('teacher_ID', models.CharField(blank=True, default=None, max_length=14, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='The ID needs to be 14 characters long.', regex='^.{14}$')])),
                ('academic_title', models.CharField(blank=True, default=None, max_length=30, null=True)),
                ('biography', models.TextField(blank=True, default=None, null=True)),
                ('website', models.URLField(blank=True, default=None, help_text='E.g.: https://www.example.com', null=True)),
                ('photo', models.ImageField(blank=True, default=None, null=True, upload_to='students_images')),
                ('phone', models.CharField(blank=True, default=None, max_length=15, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='fileupload',
            name='lecture',
            field=models.ForeignKey(default=None, on_delete=None, related_name='files', to='courses.Lecture'),
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Faculty'),
        ),
        migrations.AddField(
            model_name='course',
            name='study_programme',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='courses.StudyProgramme'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher1',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='course_course_teacher', to='courses.TeacherData', verbose_name='Course Teacher'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher2',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_seminar_teacher', to='courses.TeacherData', verbose_name='Seminar Teacher'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
