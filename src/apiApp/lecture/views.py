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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import LectureCreateSerializer, LectureListSerializer
from ..permissions import IsTeacher, IsCourseEnrollmentComplete
from ..models import Lecture


class LectureCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsTeacher,
                          IsCourseEnrollmentComplete]
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

