from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)
from ..permissions import IsUserTeacherOfCourse, IsTeacher
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer
)

from ..models import Course, Teacher, Department


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
        department = Department.objects.filter(dept_id=self.request.POST['dept_id']).first()
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
