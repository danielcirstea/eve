from courses.models import *
from django.contrib import admin

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Notification)


class StudyProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(StudyProgramme, StudyProgrammeAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Faculty, FacultyAdmin)


class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ects', 'year', 'semester')
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('student',)


admin.site.register(Course, CourseAdmin)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'student_ID', 'email', 'phone')


admin.site.register(Student, StudentAdmin)


class TeacherAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'teacher_ID', 'email', 'phone')


admin.site.register(Teacher, TeacherAdmin)


class FileUploadInline(admin.TabularInline):
    model = FileUpload

    def get_model_perms(self, request):
        return {}


admin.site.register(StudentFileUpload)


class LectureAdmin(admin.ModelAdmin):
    model = Lecture
    list_display = ('lecture_title', 'course', 'lecture_category')
    inlines = (FileUploadInline,)


admin.site.register(Lecture, LectureAdmin)


class StudentDataAdmin(admin.ModelAdmin):
    model = StudentData
    list_display = ('surname', 'name', 'student_ID', 'notes')
    exclude = ('enrolled',)


admin.site.register(StudentData, StudentDataAdmin)


class TeacherDataAdmin(admin.ModelAdmin):
    model = TeacherData
    list_display = ('surname', 'name', 'teacher_ID', 'notes')
    list_display_links = ('surname', 'name',)


admin.site.register(TeacherData, TeacherDataAdmin)
