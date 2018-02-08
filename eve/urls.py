from django.contrib import admin
from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.contrib.auth import views as auth_views

urlpatterns = [path('', include('django.contrib.auth.urls')),
               path('admin/', admin.site.urls),
               path('', views.index, name='index'),
               path('courses/', include('courses.urls')),
               path('signup/student/', views.student_register, name='student_signup'),
               path('signup/teacher/', views.teacher_register, name='teacher_signup'),
               path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'),
                    name='login'),
               path('logout/', auth_views.LogoutView.as_view(), name='logout'),
               path('profile/', views.profile_edit, name='profile_edit'),
               ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
