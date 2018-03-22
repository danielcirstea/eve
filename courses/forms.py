from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, PasswordResetForm, SetPasswordForm
from django.utils.translation import ugettext_lazy as _
from courses.models import *
from django.db.models import Q
from django.contrib.auth import password_validation


class MyAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username', 'class': 'user'}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'pass'}),
    )


class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(
        attrs={'placeholder': 'E-mail Address', 'class': 'email'}), )


class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password', 'class': 'password1'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'password2'}),
    )


class UserForm(forms.ModelForm):
    """
    It is main user form
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': "Username", 'class': 'user2'}))
    password = forms.CharField(label='Password', max_length=32, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': "Password", 'class': 'pass2'}))
    confirm_password = forms.CharField(label='Confirm', max_length=32, required=True,
                                       widget=forms.PasswordInput(
                                           attrs={'placeholder': "Repeat Password", 'class': 'pass3'}))

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match."
            )

    class Meta:
        model = User
        fields = ('username', 'password', 'confirm_password')


# student form

class StudentForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "E-mail Address", 'class': 'email'}))
    name = forms.CharField(max_length=50, required=True,
                           widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'name'}))
    surname = forms.CharField(max_length=50, required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Surname", 'class': 'surname'}))
    student_ID = forms.CharField(required=True, max_length=14, min_length=14,
                                 widget=forms.PasswordInput(attrs={'placeholder': "Student ID", 'class': 'std_id'}))
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic'}))
    phone = forms.CharField(max_length=15, required=True,
                            validators=[RegexValidator(regex='^[0-9+]+$',
                                                       message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone'}))

    def clean_student_ID(self):
        student_id = self.cleaned_data['student_ID']
        try:
            StudentData.objects.get(student_ID=student_id)
        except:
            raise forms.ValidationError("Wrong student ID.")
        return student_id

    class Meta:
        model = Student
        fields = ('email', 'name', 'surname', 'phone', 'student_ID', 'photo')


# form for editing the student model
class StudentEditForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "E-mail Address", 'class': 'email'}))
    name = forms.CharField(max_length=50, required=True,
                           widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'name'}))
    surname = forms.CharField(max_length=50, required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Surname", 'class': 'surname'}))
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic'}))
    phone = forms.CharField(max_length=15, required=True,
                            validators=[RegexValidator(regex='^[0-9+]+$',
                                                       message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone'}))

    class Meta:
        model = Student
        fields = ('email', 'name', 'surname', 'phone', 'photo')


# the teacher form
class TeacherForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "E-mail Address", 'class': 'email2'}))
    name = forms.CharField(max_length=30, required=True,
                           widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'name2'}))
    surname = forms.CharField(max_length=50, required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Surname", 'class': 'surname2'}))
    teacher_ID = forms.CharField(required=True, max_length=14, min_length=14,
                                 widget=forms.PasswordInput(attrs={'placeholder': "Teacher ID", 'class': 'tdr_id'}))
    academic_title = forms.CharField(max_length=30, required=True,
                                     error_messages={'required': 'An academic title is required.'},
                                     widget=forms.TextInput(attrs={'placeholder': "Academic Title", 'class': 'acad'}))
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic2', 'name': 'teacher-photo'}))
    phone = forms.CharField(required=True, validators=[RegexValidator(regex='^[0-9+]+$',
                                                                      message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone2'}))

    def clean_teacher_ID(self):
        id = self.cleaned_data['teacher_ID']
        try:
            TeacherData.objects.get(teacher_ID=id)
        except:
            raise forms.ValidationError("Wrong teacher ID.")
        return id

    class Meta:
        model = Teacher
        fields = ('email', 'name', 'surname', 'teacher_ID', 'academic_title', 'phone', 'photo')


# the form for editing the teacher model
class TeacherEditForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "E-mail Address", 'class': 'email2'}))
    name = forms.CharField(max_length=30, required=True,
                           widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'name2'}))
    surname = forms.CharField(max_length=50, required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Surname", 'class': 'surname2'}))
    academic_title = forms.CharField(max_length=30, required=True,
                                     widget=forms.TextInput(attrs={'placeholder': "Academic Title", 'class': 'acad2'}))
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic2', 'name': 'teacher-photo'}))
    phone = forms.CharField(required=True, validators=[RegexValidator(regex='^[0-9+]+$',
                                                                      message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone2'}))

    class Meta:
        model = Teacher
        fields = ('email', 'name', 'surname', 'academic_title', 'phone', 'photo')


# form for adding a lecture as a teacher
class LectureForm(forms.ModelForm):
    lecture_title = forms.CharField(max_length=100, required=True,
                                    widget=forms.TextInput(
                                        attrs={'class': 'lec_title', 'placeholder': 'Lecture Title'}))
    course = forms.ChoiceField(widget=forms.Select(attrs={'class': 'lec_course'}))

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = self.get_courses(user)
        self.fields['lecture_category'].widget.attrs['class'] = "lec_cat"
        self.fields['content'].widget.attrs['placeholder'] = "Write the lecture content here."
        self.fields['content'].widget.attrs['class'] = "lec_cont"

    @staticmethod
    def get_courses(teacher):
        teacher_data = TeacherData.objects.get(teacher_ID=teacher.teacher_ID)
        return [(x.id, x.name) for x in Course.objects.filter(Q(teacher1=teacher_data)
                                                              | Q(teacher2=teacher_data))]

    def clean_course(self):
        course_id = self.cleaned_data.get('course')
        course_obj = Course.objects.get(pk=course_id)
        return course_obj

    class Meta:
        model = Lecture
        fields = ('course', 'lecture_category', 'lecture_title', 'content')


# the form allowing a student to upload files on a course
class StudentFileForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a message...', 'class': 'comment'}))

    class Meta:
        model = StudentFileUpload
        fields = ('files', 'comment')


# the form allowing teacher to add notifications
class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['course'].choices = self.get_courses(user)
        self.fields['course'].widget.attrs['class'] = 'not_crs'
        self.fields['notification'].widget.attrs['class'] = "not_not"
        self.fields['notification'].widget.attrs['placeholder'] = "Notification"

    @staticmethod
    def get_courses(teacher):
        teacher_data = TeacherData.objects.get(teacher_ID=teacher.teacher_ID)
        return [(x.id, x.name) for x in Course.objects.filter(Q(teacher1=teacher_data)
                                                              | Q(teacher2=teacher_data))]

    class Meta:
        model = Notification
        fields = ('course', 'notification')
