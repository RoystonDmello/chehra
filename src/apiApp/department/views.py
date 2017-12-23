from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from ..models import Department
from ..serializers import DepartmentSerializer


# don't change variable names
class DepartmentCreateAPIView(CreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentListAPIView(ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDetailAPIView(RetrieveAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentUpdateAPIView(UpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentDeleteAPIView(DestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

