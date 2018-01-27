from django.shortcuts import redirect, render
from courses.models import User, Student, Teacher
from courses.forms import StudentForm, TeacherForm, UserForm
from django.http import HttpResponseRedirect

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
            email = cd1["email"]
            new_user = User.objects.create_user(username, password=password, email=email)
            new_user.save()
            cd2 = form2.cleaned_data
            name = cd2['name']
            surname = cd2['surname']
            email = cd1['email']
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
    return render(request, "registration/student_signup_form.html", data)


def teacher_register(request):
    data = dict()
    if request.method == 'POST':
        form1 = UserForm(request.POST)
        form2 = TeacherForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            cd1 = form1.cleaned_data
            username = cd1["username"]
            password = cd1["password"]
            email = cd1["email"]
            new_user = User.objects.create_user(username, password=password, email=email)
            new_user.save()
            cd2 = form2.cleaned_data
            name = cd2['name']
            surname = cd2['surname']
            email = cd1['email']
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
    return render(request, "registration/teacher_signup_form.html", data)


def profile_edit(request):
    user = request.user
    form = StudentForm(request.POST or None, initial={'first_name': user.first_name, 'last_name': user.last_name})
    if request.method == 'POST':
        if form.is_valid():
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']

            user.save()
            return HttpResponseRedirect('index')

    context = {
        "form": form
    }

    return render(request, "profile_edit.html", context)
