from django.shortcuts import redirect, render
from courses.forms import StudentForm, TeacherForm, UserForm, StudentEditForm, TeacherEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.core.exceptions import PermissionDenied
from courses.models import *


# the starting page of the website
def index(request):
    context = {
        'courses': Course.objects.all(),
        'students_data': StudentData.objects.all(),
        'teachers': Teacher.objects.all(),
    }
    return render(request, 'base.html', context)


# the student registration view
def student_register(request):
    if request.method == 'POST':
        form1 = UserForm(request.POST, prefix='user')
        form2 = StudentForm(request.POST, request.FILES, prefix='student')
        if form1.is_valid() and form2.is_valid():
            cd2 = form2.cleaned_data
            phone = cd2['phone']
            student_id = cd2['student_ID']
            photo = cd2['photo']
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            name = cd2["name"]
            surname = cd2["surname"]
            email = cd2["email"]
            new_user = User.objects.create_user(username, password=password, first_name=name,
                                                last_name=surname, email=email, user_type=User.USER_TYPE_STUDENT)
            Student.objects.create(user=new_user, name=name, surname=surname,
                                   student_ID=student_id, email=email, phone=phone, photo=photo)
            new_user.save()
            login(request, new_user)
            return redirect('index')

    else:
        form1 = UserForm(prefix='user')
        form2 = StudentForm(prefix='student')
    data = {
        'form1': form1,
        'form2': form2
    }
    return render(request, "registration/student_signup_form.html", data)


# the teacher registration view
def teacher_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = TeacherForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            cd2 = form2.cleaned_data
            academic_title = cd2['academic_title']
            phone = cd2['phone']
            teacher_id = cd2['teacher_ID']
            photo = cd2['photo']
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            email = cd2["email"]
            name = cd2['name']
            surname = cd2['surname']
            new_user = User.objects.create_user(username, password=password, first_name=name,
                                                last_name=surname, email=email, user_type=User.USER_TYPE_TEACHER)
            Teacher.objects.create(user=new_user, name=name, surname=surname, academic_title=academic_title,
                                   email=email, teacher_ID=teacher_id, phone=phone,
                                   photo=photo)
            new_user.save()

            login(request, new_user)
            return redirect('index')

    else:
        form1 = UserForm()
        form2 = TeacherForm()
    data['form1'] = form1
    data['form2'] = form2
    return render(request, "registration/teacher_signup_form.html", data)


# the view which allows a student/teacher to edit their information
@login_required
def profile_edit(request):
    user = request.user
    if user.is_teacher:
        form_class = TeacherEditForm
        instance = request.user.teacher
    elif user.is_student:
        form_class = StudentEditForm
        instance = request.user.student
    else:
        raise PermissionDenied()

    if request.method != 'POST':
        form = form_class(instance=instance)
    else:
        form = form_class(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['name']
            user.last_name = form.cleaned_data['surname']
            user.save()
            form.save()
            return redirect('index')

    context = {
        "form": form,
        'notifications': Notification.objects.all(),
    }
    return render(request, "registration/profile_edit.html", context)


# the about page
def about(request):
    return render(request, 'about.html')


# the guide page containing all useful information about eve
def guide(request):
    return render(request, 'guide.html')
