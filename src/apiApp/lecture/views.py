import pickle as pkl

from chera import modelling
from node_image import image_retrieval as ir
from push_notifications.models import GCMDevice
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
)
from rest_framework.permissions import (
    IsAuthenticated
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from .serializers import LectureCreateSerializer, LectureListSerializer
from ..models import Lecture, Student
from ..permissions import IsTeacher, IsCourseEnrollmentComplete, \
    IsUserTeacherOfCourse


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
    permission_classes = (IsTeacher, IsUserTeacherOfCourse)

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

        attendances = [{'student_id': student_id,
                        'attended': student_id in student_ids}
                       for student_id in mappings]

        sendable = {'attendances': attendances}

        absent_student_ids = list(set(mappings).difference(set(student_ids)))

        present_students = Student.objects.filter(
            student_id__in=student_ids).all()
        absent_students = Student.objects.filter(
            student_id__in=absent_student_ids).all()

        present_students = [st.user for st in present_students]
        absent_students = [st.user for st in absent_students]

        present_devices = GCMDevice.objects.filter(
            user__in=present_students)
        present_devices.send_message("You have been marked {0}"
                                     " for the lecture of {1} on {2}".format(
            'present', course.name, lecture.start_time))

        absent_devices = GCMDevice.objects.filter(
            user__in=absent_students).all()

        absent_devices.send_message("You have been marked {0}"
                                     " for the lecture of {1} on {2}".format(
            'absent', course.name, lecture.start_time))

        return Response(sendable)
