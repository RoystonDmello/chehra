from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from rest_framework.views import APIView

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from django.core.files import File
from ..permissions import IsUserTeacherOfCourse, IsTeacher
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer
)

from ..models import Course, Teacher, Department, CourseData

import pickle as pkl
from tempfile import TemporaryFile

from chera import modelling


# don't change variable names
class CourseCreateAPIView(CreateAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer


class CourseListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseListByTeacherIdAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        teacher = Teacher.objects.filter(user=self.request.user).first()
        queryset = Course.objects.filter(teacher_id=teacher.teacher_id)
        return queryset


class CourseListByDeptIdAPIView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        department = Department.objects.filter(dept_id=self.request.GET['dept_id']).first()
        queryset = Course.objects.filter(dept_id=department)
        return queryset


class CourseDetailAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated, IsUserTeacherOfCourse)
    authentication_classes = JSONWebTokenAuthentication
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer


class CourseDeleteAPIView(DestroyAPIView):
    permission_classes = (IsAuthenticated, IsUserTeacherOfCourse)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer


class CourseDataCreateView(APIView):
    permission_classes = (IsTeacher, IsUserTeacherOfCourse)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request):
        course_id = request.POST['course_id']

        course = Course.objects.get(course_id=course_id)

        students = course.students.all()

        # to add exception handling for no training data of students
        try:
            datas = [student.studentdata.data for student in students]
            ids = [student.student_id for student in students]

            saveable = modelling.train(ids, datas)

            outfile = TemporaryFile()
            pkl.dump(saveable, outfile)

            f = File(outfile, name='{0}.pkl'.format(course.course_id))

            course_data = CourseData(course_id=course, data=f)
            course_data.save()
        except Exception as e:
            print(e)

        course.enrollment_complete = True
        course.save()

        return Response({'msg': 'success'})


class CourseEnrollmentRetrieveView(APIView):
    permission_classes = (IsTeacher,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        course_id = request.GET['course_id']

        course = Course.objects.get(course_id=course_id)

        enrollment = course.enrollment_complete

        return Response({'enrollment_complete': enrollment})
