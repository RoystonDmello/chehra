from ..models import Student
from rest_framework.serializers import ModelSerializer


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'user', 'uid', 'dept_id' ]
