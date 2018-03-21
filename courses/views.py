from django.forms import FileInput
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.forms.models import inlineformset_factory
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import FormView
from django.contrib import messages
from .forms import LectureForm, NotificationForm, StudentFileForm
from .models import *


# main courses page view
@login_required
def index(request):
    query_list = Course.objects.all().order_by('name')
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(Q(name__icontains=query))
    paginator = Paginator(query_list, 2)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        'courses': courses,
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'studies': StudyProgramme.objects.all(),
        'teachers': Teacher.objects.all(),
    }

    return render(request, 'courses/index.html', context)


# the lectures view, displaying lectures for each course
class CourseFormView(LoginRequiredMixin, FormView):
    form_class = StudentFileForm
    success_url = reverse_lazy('courses:index')
    template_name = 'courses/courses.html'

    def get_object(self):
        return get_object_or_404(Course, slug=self.kwargs['slug'])

    def get_form_kwargs(self):
        kwargs = super(CourseFormView, self).get_form_kwargs()
        try:
            obj = StudentFileUpload.objects.get(user=self.request.user,
                                                course=self.get_object())
        except StudentFileUpload.DoesNotExist:
            pass
        else:
            kwargs['instance'] = obj
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.course = self.get_object()
        obj.show_again = False
        obj.save()
        return super(CourseFormView, self).form_valid(form)

    def already_done(self):
        return StudentFileUpload.objects.filter(course=self.get_object(),
                                                user=self.request.user,
                                                show_again=False).exists()

    def can_update(self, user):
        return user.is_teacher or (user.is_student and not self.already_done())

    def get_context_data(self, *args, **kwargs):
        data = super(CourseFormView, self).get_context_data(**kwargs)
        user = self.request.user
        student_data = StudentData.objects.get(student_ID=self.request.user.student.student_ID)
        data['object'] = self.get_object()
        data['show_form'] = self.can_update(user) and data['object'].allow_upload
        data['lectures'] = data['object'].lectures.order_by('lecture_category')
        data['course'] = data['object']
        data['teachers'] = TeacherData.objects.all()
        data['teachers2'] = Teacher.objects.all()
        data['students'] = student_data
        return data


# filter by faculty for the courses
def faculty_filter(request, slug):
    qr = get_object_or_404(Faculty, slug=slug)
    query_list = Course.objects.filter(study_programme__department__faculty=qr).order_by('name')
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(Q(name__icontains=query))
    paginator = Paginator(query_list, 1)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        'courses': courses,
        'faculties': Faculty.objects.filter(slug=slug),
        'faculties2': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'studies': StudyProgramme.objects.all(),
    }
    return render(request, 'courses/filters/faculty_filter.html', context)


# filter by study programme for the courses
def study_programme_filter(request, slug):
    qr = get_object_or_404(StudyProgramme, slug=slug)
    query_list = Course.objects.filter(study_programme=qr).order_by('name')
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(Q(name__icontains=query))
    paginator = Paginator(query_list, 1)
    page = request.GET.get('page')
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    context = {
        'courses': courses,
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'studies': StudyProgramme.objects.filter(slug=slug),
        'studies2': StudyProgramme.objects.all(),
    }
    return render(request, 'courses/filters/study_programme_filter.html', context)


FileFormset = inlineformset_factory(Lecture, FileUpload, exclude=[],
                                    widgets={'files': FileInput(attrs={'style': 'display:none'})})


# the classroom - main teacher control panel
def classroom(request):
    if not request.user.is_teacher:
        raise PermissionDenied()
    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action:
            course = Course.objects.get(id=request.POST['form3-course'])
            if action == 'activate_upload':
                messages.success(request, 'File submissions are opened for the selected course.')
                course.allow_upload = True
            elif action == 'deactivate_upload':
                messages.success(request, 'File submissions are closed for the selected course.')
                course.allow_upload = False
            course.save()
            redirect('/')
        if 'form1-course' in request.POST:
            form1 = LectureForm(request.POST, user=request.user.teacher, prefix='form1')
            if form1.is_valid():
                lecture = form1.save()
                formset = FileFormset(request.POST, request.FILES, instance=lecture, prefix='files')
                if formset.is_valid():
                    formset.save()
                    form1 = LectureForm(user=request.user.teacher, prefix='form1')
                    messages.success(request, 'Lecture added successfully.')
                formset.save()
                redirect('/')
        else:
            form1 = LectureForm(user=request.user.teacher, prefix='form1')
            formset = FileFormset(prefix='files')

        if 'form2-course' in request.POST:
            form2 = NotificationForm(request.POST, user=request.user.teacher, prefix='form2')
            if form2.is_valid():
                messages.success(request, 'Notification created successfully.')
                form2.save()
                form2 = NotificationForm(user=request.user.teacher, prefix='form2')
                redirect('/')
        else:
            form2 = NotificationForm(user=request.user.teacher, prefix='form2')
    else:
        form1 = LectureForm(user=request.user.teacher, prefix='form1')
        formset = FileFormset(prefix='files')
        form2 = NotificationForm(user=request.user.teacher, prefix='form2')
    form3 = NotificationForm(user=request.user.teacher, prefix='form3')
    teacher_data = TeacherData.objects.get(teacher_ID=request.user.teacher.teacher_ID)

    context = {
        'teacher_data': teacher_data,
        'courses': Course.objects.filter(Q(teacher1=teacher_data) | Q(teacher2=teacher_data)),
        'lectures': Lecture.objects.all(),
        'form1': form1,
        'form2': form2,
        'form3': form3,
        'formset': formset,
        'notifications': Notification.objects.all(),
        'uploads': StudentFileUpload.objects.all(),
    }
    return render(request, 'courses/classroom.html', context)


# view for deleting active notifications
class NotificationDelete(DeleteView):
    model = Notification
    success_url = reverse_lazy('classroom')
    messages = "Notification deleted successfully."


# view for deleting a lecture
class LectureDelete(DeleteView):
    model = Lecture
    success_url = reverse_lazy('classroom')


# the student upload form, allowing the student to upload files when a submission is opened
class StudentFileUploadUpdate(generic.RedirectView):
    url = reverse_lazy('classroom')

    def post(self, *args, **kwargs):
        action = self.request.POST['action']
        try:
            return getattr(self, action)()
        except AttributeError:
            raise 404

    def get_object(self):
        return get_object_or_404(StudentFileUpload, pk=self.kwargs['pk'])

    def delete(self):
        obj = self.get_object()
        obj.delete()
        return redirect(self.url)

    def show_again(self):
        obj = self.get_object()
        obj.show_again = True
        obj.save()
        return redirect(self.url)


# the enroll view which allows teachers to add students for a specific course
@login_required
def enroll(request, slug):
    if not request.user.is_teacher:
        raise PermissionDenied()
    query_list = StudentData.objects.all()
    query = request.GET.get('q')
    if query:
        query_list = query_list.filter(Q(name__icontains=query))
    paginator = Paginator(query_list, 2)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page(1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    course = Course.objects.get(slug=slug)
    if request.method == 'POST':
        course.student.add(*request.POST.getlist('student_ids'))
        course.student.remove(*request.POST.getlist('student_ids2'))
        redirect('/')
    context = {
        'course': course,
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'studies': StudyProgramme.objects.all(),
        'students': students,
        'students2': Student.objects.all()
    }
    return render(request, 'courses/enroll.html', context)


# the course page for the students, which shows only the courses he is enrolled into
def my_courses(request):
    if not request.user.is_student:
        raise PermissionDenied()
    context = {
        'courses': Course.objects.all().order_by('name'),
        'faculties': Faculty.objects.all(),
        'departments': Department.objects.all(),
        'studies': StudyProgramme.objects.all(),
        'students': StudentData.objects.all(),
        'teachers': Teacher.objects.all(),
    }
    return render(request, 'courses/student_courses.html', context)
