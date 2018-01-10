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
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from .serializers import ClassroomSerializer
from ..permissions import IsTeacher
from ..models import Classroom


class ClassroomListAPIView(ListAPIView):
    permission_classes = (IsAuthenticated, IsTeacher)
    serializer_class = ClassroomSerializer
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = Classroom.objects.all()
