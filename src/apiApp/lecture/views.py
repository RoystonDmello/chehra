from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import LectureCreateSerializer, LectureListSerializer
from ..permissions import IsTeacher, IsCourseEnrollmentComplete, \
    IsUserTeacherOfCourse
from ..models import Lecture

from node_image import image_retrieval as ir
from chera import modelling

import pickle as pkl

class LectureCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher,
                          IsCourseEnrollmentComplete,
                          IsUserTeacherOfCourse]
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Lecture.objects.all()
    serializer_class = LectureCreateSerializer


class LectureListByCourse(ListAPIView):
    serializer_class = LectureListSerializer
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = (JSONWebTokenAuthentication,)

    def get_queryset(self, *args, **kwargs):
        course_id = self.request.GET['course_id']
        queryset = Lecture.objects.filter(course_id=course_id)
        return queryset


class LectureUpdateAPIView(UpdateAPIView):
    queryset = Lecture.objects.all()
    serializer_class = LectureCreateAPIView
    permission_classes = [IsAuthenticated, IsTeacher]
    authentication_classes = (JSONWebTokenAuthentication,)


class LectureAttendanceTakenView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        lecture_id = request.GET['lect_id']

        lecture = Lecture.objects.get(lect_id=lecture_id)

        attendance = lecture.isAttendanceTaken
        return Response({'isAttendanceTaken': attendance})


class LectureTakeAttendanceView(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsTeacher, IsCourseEnrollmentComplete)

    def get(self, request):
        lecture_id = request.GET['lect_id']
        lecture = Lecture.objects.get(lect_id=lecture_id)
        classroom = lecture.classroom
        cameras = classroom.camera_set.all()

        base_urls = [camera.camera_url for camera in cameras]

        imgs = ir.class_click(base_urls)

        course = lecture.course_id
        model, mappings = pkl.load(course.coursedata.data)

        student_ids = modelling.predict(model, mappings, imgs)

        sendable = {'present_student_ids': student_ids}

        return Response(sendable)
