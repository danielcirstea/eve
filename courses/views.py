from .models import Course
from django.shortcuts import render


def index(request):
    con = Course.objects.all()
    return render(request, 'courses/index.html', {'courses': con})


def courses(request, slug):
    query = Course.objects.get(slug=slug)
    context = {'courses': Course.objects.filter(slug=slug),
               'lectures': query.lectures.order_by('lecture_category'),
               }
    return render(request, 'courses/courses.html', context)
