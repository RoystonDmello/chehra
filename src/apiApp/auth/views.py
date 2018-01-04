# from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView
)

from rest_framework_jwt.settings import api_settings
import json, jsonpickle

from .serializers import StudentImageSerializer, UserSerializer
from ..models import Teacher, Student, Department, StudentImage


def get_jwt(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token


class Register(APIView):

    def post(self, request, *args, **kwargs):
        if not request.POST:
            return Response({'Error': "Please provide username/password", 'msg': 'failure'}, status=400)

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_teacher = request.POST.get('isTeacher')

        is_teacher = (is_teacher == 'False' or is_teacher == 'false' or is_teacher == 0 or is_teacher == '0')

        try:
            user = User.objects.create(email=email, username=username,
                                       first_name=first_name, last_name=last_name)
            user.set_password(password)
            user.save()

            if is_teacher:
                instance = Teacher(user=user)
                instance.save()
            else:
                uid = request.POST.get('uid')
                dept_id = request.POST.get('dept_id')
                dept_id = int(dept_id)
                department = Department.objects.get(dept_id=dept_id)
                instance = Student(user=user, uid=uid)
                instance.dept_id = department
                instance.save()

            return Response({'msg': 'success'})
        except Exception as e:
            return Response(
                {
                    'msg': 'failure',
                    'Error': e.__str__()
                }, status=400
            )


class Login(APIView):

    def post(self, request, *args, **kwargs):
        if not request.POST:
            return Response({'Error': "Please provide username/password", 'msg': 'failure'}, status=400)

        username = request.POST.get('username')
        password = request.POST.get('password')
        is_teacher = request.POST.get('isTeacher')

        is_teacher = (is_teacher == 'False' or is_teacher == 'false' or is_teacher == 0 or is_teacher == '0')


        try:
            user = authenticate(username=username, password=password)

            if is_teacher:
                teacher = Teacher.objects.get(user=user)
                id = teacher.teacher_id
            else:
                student = Student.objects.get(user=user)
                id = student.student_id

        except Exception as e:
            print(e)
            return Response({'Error': "Invalid username/password", 'msg': 'failure'}, status=401)

        token = get_jwt(user)
        return Response({'token': token, 'id': id,
                         'is_teacher': is_teacher,
                         'user': UserSerializer(user).data
                         }, status=200)


class StudentImageCreateAPIView(CreateAPIView):
    serializer_class = StudentImageSerializer
    queryset = StudentImage.objects.all()


class StudentImageUpdateAPIView(UpdateAPIView):
    serializer_class = StudentImageSerializer
    queryset = StudentImage.objects.all()


class StudentImageGetListAPIView(ListAPIView):
    serializer_class = StudentImageSerializer

    def get_queryset(self, *args, **kwargs):
        student_id = self.request.GET['student_id']
        return StudentImage.objects.filter(student_id=student_id)


class StudentImageDeleteAPIView(DestroyAPIView):
    serializer_class = StudentImageSerializer
    queryset = StudentImage.objects.all()


