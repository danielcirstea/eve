from django.shortcuts import redirect, render
from courses.models import User, Student, Teacher
from courses.forms import StudentForm, TeacherForm, UserForm


def index(request):
    return render(request, 'index.html', )


def student_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = StudentForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            new_user = User.objects.create_user(username, password=password)
            new_user.save()
            cd2 = form2.cleaned_data
            name = cd2['name']
            surname = cd2['surname']
            email = cd2['email']
            phone = cd2['phone']
            student_id = cd2['student_ID']
            photo = cd2['photo']
            Student.objects.create(user=new_user, name=name, surname=surname,
                                   student_ID=student_id, email=email, phone=phone, photo=photo)
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = StudentForm()
    data['form1'] = form1
    data['form2'] = form2
    return render(request, "student_signup_form.html", data)


def teacher_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = TeacherForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            new_user = User.objects.create_user(username, password=password)
            new_user.save()
            cd2 = form2.cleaned_data
            name = cd2['name']
            surname = cd2['surname']
            email = cd2['email']
            academic_title = cd2['academic_title']
            phone = cd2['phone']
            bio = cd2['bio']
            website = cd2['website']
            photo = cd2['photo']
            Teacher.objects.create(user=new_user, name=name, surname=surname, academic_title=academic_title,
                                   email=email, phone=phone, bio=bio, website=website, photo=photo)
            return redirect('index')
    else:
        form1 = UserForm()
        form2 = TeacherForm()
    data['form1'] = form1
    data['form2'] = form2
    return render(request, "teacher_signup_form.html", data)
