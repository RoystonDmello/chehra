from rest_framework.permissions import BasePermission
from .models import Teacher, Student, Course


class IsUserTeacherOfCourse(BasePermission):

    message = "You are not the teacher of this course"

    def has_object_permission(self, request, view, obj):
        teacher = Teacher.objects.filter(user=request.user).first()
        return teacher == obj.teacher_id


class IsTeacher(BasePermission):
    message = "You are not a teacher"

    def has_permission(self, request, view):
        num_results = Teacher.objects.filter(user=request.user).count()
        return num_results == 1


class IsStudent(BasePermission):
    message = "You are not a student"

    def has_permission(self, request, view):
        num_results = Student.objects.filter(user=request.user).count()
        return num_results == 1


class IsCourseEnrollmentComplete(BasePermission):
    message = "The course has not completed enrollment"

    def has_permission(self, request, view):
        course = Course.objects.filter(course_id=request.POST['course_id']).first()

        return course.enrollment_complete
