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
from ..permissions import IsUserTeacherOfCourse, IsTeacher
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer
)

from ..models import Course, Teacher, Department

from ..tasks import course_process

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
        year = self.request.GET['year']
        academic_yr = self.request.GET['academic_yr']
        queryset = Course.objects.filter(dept_id=department, year=year, academic_yr=academic_yr)
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

        course_process.delay(course_id)

        return Response({'msg': 'success'})


class CourseEnrollmentRetrieveView(APIView):
    permission_classes = (IsTeacher,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(self, request):
        course_id = request.GET['course_id']

        course = Course.objects.get(course_id=course_id)

        enrollment = course.enrollment_complete

        return Response({'enrollment_complete': enrollment})
