from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views
from . import views as views1
from courses import views as views2

urlpatterns = [path('accounts/', include('django.contrib.auth.urls')),
               path('admin/', admin.site.urls),
               path('', views1.index, name='index'),
               path('courses/', include('courses.urls')),
               path('teacher/classroom/', views2.classroom, name='classroom'),
               path('teacher/classroom/<slug:slug>/enroll/', views2.enroll, name='enroll'),
               path('signup/student/', views1.student_register, name='student_signup'),
               path('signup/teacher/', views1.teacher_register, name='teacher_signup'),
               path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
                    name='login'),
               path('logout/', auth_views.LogoutView.as_view(), name='logout'),
               path('profile/', views1.profile_edit, name='profile_edit'),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
