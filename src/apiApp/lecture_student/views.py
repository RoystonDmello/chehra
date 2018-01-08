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
from ..lecture.serializers import LectureListSerializer,CalendarDatesSerializer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from ..permissions import IsTeacher
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)


class MarkAttendanceAPIView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated, IsTeacher]

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
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated, IsTeacher]

    def get_queryset(self, *args, **kwargs):
        lect_id = self.request.GET['lect_id']
        return Student.objects.filter(lecture=lect_id)


class LectureByStudentIdListAPIView(ListAPIView):

    serializer_class = LectureListSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        course_id = self.request.GET['course_id']
        return Lecture.objects.filter(students=student_id, course_id=course_id)


class IsPresentForLectureDatesByCourseAPIView(ListAPIView):

    serializer_class = CalendarDatesSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        course_id = self.request.GET['course_id']
        all_lectures=Lecture.objects.filter(course_id=course_id)
        serialized_lecture_data=CalendarDatesSerializer(all_lectures,many=True)

        for lecture in serialized_lecture_data.data:
            #print(lecture['lect_id'])
            if(all_lectures.filter(lect_id=lecture['lect_id'],students=student_id).exists()):
                lecture['is_present']=True

        return serialized_lecture_data.data

