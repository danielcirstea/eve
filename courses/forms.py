from django import forms
from courses.models import *
from django.db.models import Q


class UserForm(forms.ModelForm):
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
        id = self.cleaned_data['student_ID']
        try:
            StudentData.objects.get(student_ID=id)
        except:
            raise forms.ValidationError("Wrong student ID.")
        return id

    class Meta:
        model = Student
        fields = ('email', 'name', 'surname', 'phone', 'student_ID', 'photo')


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
    biography = forms.Textarea(attrs={'class': 'bio'})
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic2', 'name': 'teacher-photo'}))
    phone = forms.CharField(required=True, validators=[RegexValidator(regex='^[0-9+]+$',
                                                                      message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone2'}))

    def __init__(self, *args, **kwargs):
        super(TeacherForm, self).__init__(*args, **kwargs)
        self.fields['biography'].widget.attrs['placeholder'] = "Write few things about yourself."

    def clean_teacher_ID(self):
        id = self.cleaned_data['teacher_ID']
        try:
            TeacherData.objects.get(teacher_ID=id)
        except:
            raise forms.ValidationError("Wrong teacher ID.")
        return id

    class Meta:
        model = Teacher
        fields = ('email', 'name', 'surname', 'teacher_ID', 'academic_title', 'phone', 'biography', 'photo')


class TeacherEditForm(forms.ModelForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'placeholder': "E-mail Address", 'class': 'email2'}))
    name = forms.CharField(max_length=30, required=True,
                           widget=forms.TextInput(attrs={'placeholder': "Name", 'class': 'name2'}))
    surname = forms.CharField(max_length=50, required=True,
                              widget=forms.TextInput(attrs={'placeholder': "Surname", 'class': 'surname2'}))
    academic_title = forms.CharField(max_length=30, required=True,
                                     widget=forms.TextInput(attrs={'placeholder': "Academic Title", 'class': 'acad2'}))
    biography = forms.Textarea(attrs={'class': 'bio_edit'})
    photo = forms.ImageField(required=True, error_messages={'required': 'A profile picture is required.'},
                             widget=forms.FileInput(attrs={'class': 'profile_pic2', 'name': 'teacher-photo'}))
    phone = forms.CharField(required=True, validators=[RegexValidator(regex='^[0-9+]+$',
                                                                      message='Not a valid phone number.')],
                            widget=forms.TextInput(attrs={'placeholder': "Phone Number", 'class': 'phone2'}))

    def __init__(self, *args, **kwargs):
        super(TeacherEditForm, self).__init__(*args, **kwargs)
        self.fields['biography'].widget.attrs['placeholder'] = "Write few things about yourself."
        self.fields['biography'].widget.attrs['class'] = "bio_edit"

    class Meta:
        model = Teacher
        fields = ('email', 'name', 'surname', 'academic_title', 'phone', 'biography', 'photo')


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


class FileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('files',)


class StudentFileForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Add a message...', 'class': 'comment'}))

    class Meta:
        model = StudentFileUpload
        fields = ('files', 'comment')


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
