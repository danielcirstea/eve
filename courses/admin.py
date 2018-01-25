from courses.models import *
from django.contrib import admin

admin.site.register(User)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(StudyProgramme)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ects', 'year', 'semester')
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Course, CourseAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'student_ID', 'email', 'phone')


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'email', 'phone')


admin.site.register(Teacher, TeacherAdmin)

'''

    def get_model_perms(self, request):
        return {}
    actions = ['delete']

'''


class FileUploadInline(admin.TabularInline):
    model = FileUpload

    def get_model_perms(self, request):
        return {}


class LectureAdmin(admin.ModelAdmin):
    model = Lecture
    list_display = ('lecture_title', 'course', 'lecture_category')
    inlines = (FileUploadInline,)


admin.site.register(Lecture, LectureAdmin)
