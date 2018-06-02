from courses.models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(Department)
admin.site.register(Notification)


class StudentInline(admin.StackedInline):
    model = Student


class TeacherInline(admin.StackedInline):
    model = Teacher


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline,
        TeacherInline
    ]

    def get_fieldsets(self, request, obj=None):
        return super(UserAdmin, self).get_fieldsets(request, obj)


class StudentUser(User):
    class Meta:
        proxy = True


class TeacherUser(User):
    class Meta:
        proxy = True


@admin.register(StudentUser)
class StudentUserAdmin(admin.ModelAdmin):
    inlines = [
        StudentInline
    ]

    def get_queryset(self, request):
        return User.objects.filter(user_type=User.USER_TYPE_STUDENT)


@admin.register(TeacherUser)
class TeacherUserAdmin(admin.ModelAdmin):
    inlines = [
        TeacherInline
    ]

    def get_queryset(self, request):
        return User.objects.filter(user_type=User.USER_TYPE_TEACHER)


class StudyProgrammeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(StudyProgramme, StudyProgrammeAdmin)


class FacultyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Faculty, FacultyAdmin)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'ects', 'year', 'semester')
    prepopulated_fields = {'slug': ('name',)}
    exclude = ('student', 'allow_upload')


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
admin.site.site_header = 'EVE Administration'
