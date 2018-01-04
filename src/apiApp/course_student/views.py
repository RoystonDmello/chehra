from django.http import JsonResponse
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.views import APIView
from ..models import Student, Course
from ..auth.serializers import StudentSerializer
from ..course.serializers import CourseDetailSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from ..permissions import IsTeacher, IsStudent


class EnrollInCourse(APIView):
    permission_classes = (IsAuthenticated, IsStudent)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, *args, **kwargs):
        try:
            course_id = request.POST['course_id']
            student_id = request.POST['student_id']

            course = Course.objects.filter(course_id=course_id).first()
            student = Student.objects.filter(student_id=student_id).first()

            if not course:
                return JsonResponse({'msg': 'failure'}, {'detail': 'Invalid course'})
            if not student:
                return JsonResponse({'msg': 'failure'}, {'detail': 'Invalid Student'})

            course.students.add(student)
            return JsonResponse({'msg': 'success'})
        except Exception as e:
            return JsonResponse({'msg': 'failure'}, {'detail': e})


class GetEnrolledStudentsByCourseIdListAPIView(ListAPIView):
    serializer_class = StudentSerializer
    permission_classes = (IsAuthenticated, IsTeacher)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        course_id = self.request.GET['course_id']
        queryset = Student.objects.filter(course=course_id)
        print(queryset)
        return queryset


class GetEnrolledCoursesByStudentIdListAPIView(ListAPIView):
    serializer_class = CourseDetailSerializer
    permission_classes = (IsAuthenticated, IsStudent)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        return Course.objects.filter(students=student_id)

