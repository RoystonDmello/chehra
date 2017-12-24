from rest_framework.permissions import BasePermission
from .models import Teacher


class IsUserTeacherOfCourse(BasePermission):

    message = "You are not the teacher of this course"

    def has_object_permission(self, request, view, obj):
        teacher = Teacher.objects.filter(user=request.user).first()
        return teacher == obj.teacher_id


class IsTeacher(BasePermission):
    message = "You are not a teacher"

    def has_object_permission(self, request, view, obj):
        num_results = Teacher.objects.filter(user=request.user).count()
        return num_results == 1
