from ..models import Student, StudentData, Teacher
from rest_framework.serializers import ModelSerializer
from ..models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class StudentSerializer(ModelSerializer):

    user = UserSerializer(required=True)

    class Meta:
        model = Student
        fields = ['student_id', 'uid', 'dept_id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student = Student.objects.update_or_create(
            user=user,
            uid=validated_data.pop('uid'),
            dept_id=validated_data.pop('dept_id')
        )
        return student


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['teacher_id', 'user']


class StudentDataSerializer(ModelSerializer):
    class Meta:
        model = StudentData
        fields = ['data_id', 'student_id', 'data']
