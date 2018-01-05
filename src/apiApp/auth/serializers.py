from ..models import Student, StudentVideo
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['student_id', 'user', 'uid', 'dept_id']


class StudentImageSerializer(ModelSerializer):
    class Meta:
        model = StudentVideo
        fields = ['image_id', 'student_id', 'image', 'type']
