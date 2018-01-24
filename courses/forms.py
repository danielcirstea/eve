from django import forms
from courses.models import *


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('phone', 'student_ID', 'photo')


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('academic_title', 'photo', 'phone', 'website', 'bio')
