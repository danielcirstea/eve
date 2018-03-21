from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser


# main django database

class Faculty(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=140, blank=True)

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
                                                (2, "Doctoral Studies"),
                                                (3, "Integrated Studies")), default=0)
    duration = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    slug = models.SlugField(max_length=140, blank=True)

    class Meta:
        verbose_name = "Study Programme"
        verbose_name_plural = 'Study Programmes'

    def __str__(self):
        return self.name


class Course(models.Model):
    study_programme = models.ForeignKey('StudyProgramme', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, unique=True)
    ects = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    description = models.TextField()
    year = models.PositiveSmallIntegerField(validators=[MaxValueValidator(99)])
    semester = models.IntegerField(choices=((1, "1"),
                                            (2, "2"),
                                            ), default=1)
    teacher1 = models.ForeignKey('TeacherData', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="Course Teacher", related_name='%(class)s_course_teacher')
    teacher2 = models.ForeignKey('TeacherData', on_delete=models.CASCADE, null=True, blank=True,
                                 verbose_name="Seminar Teacher", related_name='%(class)s_seminar_teacher')
    student = models.ManyToManyField('StudentData')
    slug = models.SlugField(max_length=150, unique=True)
    allow_upload = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    LECTURE_CHOICES = (
        ('Courses', 'Courses'),
        ('Seminars', 'Seminars'),
    )
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True, related_name='lectures', )
    lecture_category = models.CharField(max_length=10, choices=LECTURE_CHOICES, default='Courses', )
    lecture_title = models.CharField(max_length=100, blank=True)
    content = models.TextField(blank=True)

    def __str__(self):
        return str(self.lecture_title)


class FileUpload(models.Model):
    files = models.FileField(upload_to='documents')
    lecture = models.ForeignKey('Lecture', related_name='files', on_delete=None, null=True)

    def __str__(self):
        return str(self.files)

    def file_link(self):
        if self.files:
            return "<a href='%s'>download</a>" % (self.files.url,)
        else:
            return "No attachment"


class StudentFileUpload(models.Model):
    course = models.ForeignKey("Course", related_name='files', on_delete=None, null=True)
    files = models.FileField(upload_to='student_files')
    comment = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField('courses.User', on_delete=models.CASCADE, primary_key=True, blank=True)
    show_again = models.BooleanField(default=False)

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
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True)
    student_ID = models.CharField(unique=True, max_length=14,
                                  validators=[RegexValidator(regex='^.{14}$',
                                                             message='The ID needs to be 14 characters long.')],
                                  blank=True)
    photo = models.ImageField(upload_to='students_images', blank=True)
    phone = models.CharField(max_length=15, blank=True,
                             validators=[RegexValidator(regex='^[a-zA-Z0-9+]+$',
                                                        message='Not a valid phone number.')], )
    file_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.surname)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=30, blank=True)
    surname = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True)
    teacher_ID = models.CharField(unique=True, max_length=14, blank=True,
                                  validators=[RegexValidator(regex='^.{14}$',
                                                             message='The ID needs to be 14 characters long.')])
    academic_title = models.CharField(max_length=30, blank=True)
    photo = models.ImageField(upload_to='teacher_images', blank=True)
    phone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return self.surname


class StudentData(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    student_ID = models.CharField(unique=True, max_length=14)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Student Data"
        verbose_name_plural = "Students Data"

    def __str__(self):
        return self.surname


class TeacherData(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    teacher_ID = models.CharField(unique=True, max_length=14)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Teacher Data"
        verbose_name_plural = "Teachers Data"

    def __str__(self):
        return str(self.surname)


class Notification(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, null=True)
    notification = models.CharField(max_length=100)

    def __str__(self):
        return self.notification
