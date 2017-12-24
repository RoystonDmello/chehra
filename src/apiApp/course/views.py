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

from ..models import Course,Teacher


# don't change variable names
class CourseCreateAPIView(CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated]


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]


class CourseListByTeacherIdAPIView(ListAPIView):
    # queryset = Course.objects.filter()
    serializer_class = CourseDetailSerializer

    def get_queryset(self, *args, **kwargs):
        teacher = Teacher.objects.filter(user=self.request.user).first()
        queryset = Course.objects.filter(teacher_id=teacher.teacher_id)
        return queryset


class CourseDetailAPIView(RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [IsAuthenticated]


class CourseUpdateAPIView(UpdateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsUserTeacherOfCourse]


class CourseDeleteAPIView(DestroyAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseCreateSerializer
    permission_classes = [IsAuthenticated, IsUserTeacherOfCourse]
