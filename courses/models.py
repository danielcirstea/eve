from django.core.validators import MaxValueValidator
from django.template.defaultfilters import slugify
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class Faculty(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name


class Department(models.Model):
    faculty = models.ForeignKey('Faculty', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudyProgramme(models.Model):
    department = models.ForeignKey('Department', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    studies_type = models.IntegerField(choices=((0, "Bachelor Studies"),
                                                (1, "Master Studies"),
                                                (2, "PhD Studies"),
                                                (3, "Integrated Studies")), default=0)
    duration = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = "Study Programme"
        verbose_name_plural = 'Study Programmes'

    def __str__(self):
        return self.name


class Course(models.Model):
    study_programme = models.ForeignKey('StudyProgramme', on_delete=models.CASCADE, default='')
    name = models.CharField(max_length=50)
    ects = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    description = models.TextField()
    year = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    semester = models.IntegerField(choices=((0, "1"),
                                            (1, "2"),
                                            ), default=0)
    slug = models.SlugField(max_length=140, unique=True)

    def __str__(self):
        return self.name

    def _get_unique_slug(self):
        slug = slugify(self.name)
        unique_slug = slug
        num = 1
        while Course.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super().save()


class Lecture(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, default='', related_name='lectures')
    lecture_category = models.IntegerField(choices=((0, "Classes "),
                                                    (1, "Seminars"),
                                                    ), default=0)
    lecture_title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return str(self.lecture_title)


class FileUpload(models.Model):
    files = models.FileField(upload_to='documents', null=True, blank=True)
    lecture = models.ForeignKey('Lecture', related_name='files', on_delete=None, default=None)

    def __str__(self):
        return str(self.files)

    def file_link(self):
        if self.files:
            return "<a href='%s'>download</a>" % (self.files.url,)
        else:
            return "No attachment"

    file_link.allow_tags = True
    file_link.short_description = 'File Download'


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True, default=None)
    surname = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    student_ID = models.CharField(unique=True, max_length=14,
                                  validators=[RegexValidator(regex='^.{14}$',
                                                             message='The ID needs to be 14 characters long.')],
                                  null=True, blank=True, default=None)
    photo = models.ImageField(upload_to='students_images', null=True, blank=True, default=None)
    phone = models.CharField(max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return self.surname


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True, default=None)
    surname = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(unique=True, null=True, blank=True, default=None)
    academic_title = models.CharField(max_length=30, null=True, blank=True, default=None)
    bio = models.TextField(null=True, blank=True, default=None)
    website = models.URLField(help_text="E.g.: https://www.example.com", null=True, blank=True, default=None)
    photo = models.ImageField(upload_to='students_images', null=True, blank=True, default=None)
    phone = models.CharField(max_length=15, null=True, blank=True, default=None)

    def __str__(self):
        return self.surname


class StudentData(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    student_ID = models.CharField(unique=True, max_length=14)

    class Meta:
        verbose_name = "Student Data"
        verbose_name_plural = "Students Data"

    def __str__(self):
        return self.surname


User.student = property(lambda p: Student.objects.get_or_create(user=p)[0])
User.teacher = property(lambda p: Teacher.objects.get_or_create(user=p)[0])
