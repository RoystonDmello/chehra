from django.http import JsonResponse
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.views import APIView
from ..models import Student, Course
from .serializers import StudentSerializer
from ..course.serializers import CourseDetailSerializer


class EnrollInCourse(APIView):
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

    def get_queryset(self, *args, **kwargs):
        course_id = self.request.GET['course_id']
        queryset = Student.objects.filter(course=course_id)
        print(queryset)
        return queryset


class GetEnrolledCoursesByStudentIdListAPIView(ListAPIView):
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        return Course.objects.filter(students=student_id)

