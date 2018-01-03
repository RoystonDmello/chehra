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
from ..permissions import IsUserTeacherOfCourse
from .serializers import (
    CourseCreateSerializer,
    CourseDetailSerializer
)

from ..models import Course, Teacher, Department


# don't change variable names
class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = []


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = []


class CourseListByTeacherIdAPIView(ListAPIView):
    # queryset = Course.objects.filter()
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        teacher = Teacher.objects.filter(user=self.request.user).first()
        queryset = Course.objects.filter(teacher_id=teacher.teacher_id)
        return queryset


class CourseListByDeptIdAPIView(ListAPIView):
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        department = Department.objects.filter(dept_id=self.request.POST['dept_id']).first()
        queryset = Course.objects.filter(dept_id=department)
        return queryset


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = []


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsUserTeacherOfCourse]


class CourseDeleteAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsUserTeacherOfCourse]
