from django.http import JsonResponse
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)
from rest_framework.views import APIView
from ..views import markAttendance, isStudentEnrolledInCourse
from ..models import Lecture, Student
from ..auth.serializers import StudentSerializer
from ..lecture.serializers import LectureListSerializer


class MarkAttendanceAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            lect_id = request.POST['lect_id']
            student_id = request.POST['student_id']
            has_attended = request.POST['has_attended']

            lecture = Lecture.objects.filter(lect_id=lect_id).first()
            boolean = isStudentEnrolledInCourse(student_id=student_id, course=lecture.course_id)
            if not boolean:
                return JsonResponse(
                    {'msg': 'failure'},
                    {'detail': 'Student is not enrolled in the course'}
                )
            if has_attended == 'False' or has_attended == 'false' or has_attended == 0 or has_attended == '0':
                has_attended = False
            else:
                has_attended = True
            markAttendance(lect_id=lect_id, student_id=student_id, has_attended=has_attended)
            return JsonResponse({'msg': 'success'})

        except Exception as e:
            return JsonResponse({'msg': 'failure'}, {'detail': e})


class StudentListByLectureIdListAPIView(ListAPIView):

    serializer_class = StudentSerializer

    def get_queryset(self, *args, **kwargs):
        lect_id = self.request.GET['lect_id']
        return Student.objects.filter(lecture=lect_id)


class LectureByStudentIdListAPIView(ListAPIView):

    serializer_class = LectureListSerializer

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        course_id = self.request.GET['course_id']
        return Lecture.objects.filter(students=student_id, course_id=course_id)
