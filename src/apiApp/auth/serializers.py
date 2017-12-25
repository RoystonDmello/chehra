from ..models import Student, StudentImage
from rest_framework.serializers import ModelSerializer


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'user', 'uid', 'dept_id']


class StudentImageSerializer(ModelSerializer):
    class Meta:
        model = StudentImage
        fields = ['image_id', 'student_id', 'image', 'type']
