from django.urls import path
from . import views

app_name = 'courses'
# the url patterns of the course app
urlpatterns = [
    path('', views.index, name='index'),
    path('faculties-filter/<slug:slug>/', views.faculty_filter, name='faculty_filter'),
    path('studies-filter/<slug:slug>/', views.study_programme_filter, name='study_programme_filter'),
    path('<slug:slug>/', views.CourseFormView.as_view(), name='courses'),
    path('teacher/classroom/<int:pk>/delete/', views.LectureDelete.as_view(), name='lecture_delete'),
    path('teacher/classroom/notification/<int:pk>/delete/', views.NotificationDelete.as_view(), name='not_delete'),
    path('teacher/classroom/upload/<int:pk>/update/', views.StudentFileUploadUpdate.as_view(), name='upload_update'),
]

