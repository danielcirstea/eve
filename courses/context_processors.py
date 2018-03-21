from courses.models import Notification


# notifications for students

def notifications(request):

    student = getattr(request.user, 'student', None)
    if request.user.is_authenticated and student:
        student_notifications = Notification.objects.filter(course__student__student_ID=student.student_ID)
        return {
            'notifications': student_notifications
        }

    return {}
