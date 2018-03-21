from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from eve import views
from courses import views as courses_views

# the main url patterns for the project, mostly for authentication
urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('courses/', include('courses.urls')),
    path('teacher/classroom/', courses_views.classroom, name='classroom'),
    path('teacher/classroom/<slug:slug>/enroll/', courses_views.enroll, name='enroll'),
    path('signup/student/', views.student_register, name='student_signup'),
    path('signup/teacher/', views.teacher_register, name='teacher_signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
        name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile_edit, name='profile_edit'),
    path('my-courses/', courses_views.my_courses, name='my_courses'),
    path('about/', views.about, name='about'),
    path('guide/', views.guide, name='guide'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns