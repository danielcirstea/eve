from django import forms
from courses.models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=32, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirm', max_length=32, required=True, widget=forms.PasswordInput,
                                       help_text="Passwords must match!")

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

    class Meta:
        model = User
        fields = ('username', 'password')
        exclude = ('email',)


class StudentForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    student_ID = forms.CharField(required=True, max_length=14, min_length=14)
    photo = forms.ImageField(required=True)
    phone = forms.CharField(max_length=15, required=True)

    class Meta:
        model = Student
        fields = ('name', 'surname', 'email', 'phone', 'student_ID', 'photo')


class TeacherForm(forms.ModelForm):
    name = forms.CharField(max_length=30, required=True)
    surname = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(required=True)
    academic_title = forms.CharField(max_length=30, required=True)
    bio = forms.Textarea()
    website = forms.URLField(required=False)
    photo = forms.ImageField(required=True)
    phone = forms.CharField(required=True)

    class Meta:
        model = Teacher
        fields = ('name', 'surname', 'academic_title', 'email', 'phone', 'bio', 'photo', 'website')
