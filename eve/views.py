from django.shortcuts import redirect, render
from courses.models import User, Student, Teacher
from courses.forms import StudentForm, TeacherForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login


def index(request):
    return render(request, 'index.html')


def student_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = StudentForm(request.POST, request.FILES)
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
                                                last_name=surname, email=email, is_student=True)
            Student.objects.create(user=new_user, name=name, surname=surname,
                                   student_ID=student_id, email=email, phone=phone, photo=photo)
            new_user.save()
            login(request, new_user)
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = StudentForm()
    data['form1'] = form1
    data['form2'] = form2
    return render(request, "registration/student_signup_form.html", data)


def teacher_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = TeacherForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            cd2 = form2.cleaned_data
            academic_title = cd2['academic_title']
            phone = cd2['phone']
            bio = cd2['bio']
            website = cd2['website']
            photo = cd2['photo']
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            email = cd2["email"]
            name = cd2['name']
            surname = cd2['surname']
            new_user = User.objects.create_user(username, password=password, first_name=name,
                                                last_name=surname, email=email, is_teacher=True)
            Teacher.objects.create(user=new_user, name=name, surname=surname, academic_title=academic_title,
                                   email=email, phone=phone, bio=bio, website=website, photo=photo)
            new_user.save()
            login(request, new_user)
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = TeacherForm()
    data['form1'] = form1
    data['form2'] = form2
    return render(request, "registration/teacher_signup_form.html", data)


@login_required
def profile_edit(request):
    user = request.user
    student = request.user.student
    teacher = request.user.teacher
    if user.is_teacher:
        if request.method != 'POST':
            form = TeacherForm(instance=teacher)
        else:
            form = TeacherForm(request.POST, instance=teacher)
            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['surname']
                user.save()
                form.save()
                return redirect('index')
    elif user.is_student:
        if request.method != 'POST':
            form = StudentForm(instance=student)
        else:
            form = StudentForm(request.POST, instance=student)
            if form.is_valid():
                user.email = form.cleaned_data['email']
                user.first_name = form.cleaned_data['name']
                user.last_name = form.cleaned_data['surname']
                user.save()
                form.save()
                return redirect('index')
    context = {
        "form": form,
    }
    return render(request, "registration/profile_edit.html", context)
