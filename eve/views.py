from django.contrib.auth import login
from django.shortcuts import redirect, render_to_response, render
from django.views.generic import CreateView, View
from courses.models import User
from courses.forms import StudentForm, TeacherForm, UserForm
from django.contrib import messages


def index(request):
    return render(request, 'index.html', )


def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        student_form = StudentForm(request.POST, instance=request.user.student)
        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        student_form = StudentForm(instance=request.user.student)
    return render(request, 'index.html', {
        'user_form': user_form,
        'student_form': student_form
    })
