from ..models import Student, StudentData
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


class StudentDataSerializer(ModelSerializer):
    class Meta:
        model = StudentData
        fields = ['data_id', 'student_id', 'data']
