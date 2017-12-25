from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Lecture, Student, Course


# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse({'text': 'hello This is index page',
                         'status': '200 OK'}
                        )


def markAttendance(lect_id, student_id, has_attended):

    lecture = Lecture.objects.filter(lect_id=lect_id).first()
    student = Student.objects.filter(student_id=student_id).first()

    if has_attended:
        lecture.students.add(student)
    else:
        lecture.students.remove(student)


def isStudentEnrolledInCourse(student_id, course):
    # student = Student.objects.filter(student_id=student_id)
    course = Course.objects.filter(course_id=course.course_id).first()
    queryset = course.students.filter(student_id=student_id)
    print(queryset)
    return queryset.count() == 1
