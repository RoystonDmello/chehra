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

import jwt, json, jsonpickle

from .serializers import StudentImageSerializer
from ..models import Teacher, Student, Department, StudentImage


class Register(APIView):

    def post(self, request, *args, **kwargs):
        if not request.POST:
            return Response({'Error': "Please provide username/password"}, status="400")

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        is_teacher = request.POST.get('isTeacher')

        if is_teacher == 'False' or is_teacher == 'false' or is_teacher == 0 or is_teacher == '0':
            is_teacher = False
        else:
            is_teacher = True

        try:
            user = User.objects.create(email=email, username=username)
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

            response = {
                'msg': 'success'
            }
            return JsonResponse(
                    response,
                    status=200,
                    content_type="application/json",
                    safe=False
            )
        except Exception as e:
            response = {
                'msg': 'failure',
                'Error': e
            }
            serialized_response = jsonpickle.encode(response)
            return JsonResponse(
                    serialized_response,
                    status=400,
                    content_type="application/json",
                    safe=False
                )


class Login(APIView):

    def post(self, request, *args, **kwargs):
        if not request.POST:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.POST.get('username')
        password = request.POST.get('password')
        is_teacher = request.POST.get('isTeacher')

        if is_teacher == 'False' or is_teacher == 'false' or is_teacher == 0 or is_teacher == '0':
            is_teacher = False
        else:
            is_teacher = True

        try:
            user = authenticate(username=username, password=password)
            if is_teacher == 'False' or is_teacher == 'false' or is_teacher == 0 or is_teacher == '0':
                is_teacher = False
            else:
                is_teacher = True

            if is_teacher:
                teacher = Teacher.objects.get(user=user)
            else:
                student = Student.objects.get(user=user)

        except Exception as e:
            print(e)
            return Response({'Error': "Invalid username/password"}, status="400")

        errorResponse = Response({'Error': "Invalid credentials"})

        if is_teacher:
            if teacher:
                payload = {
                    'id': teacher.teacher_id,
                    'email': teacher.user.email,
                }
            else:
                return errorResponse
        else:
            if student:
                payload = {
                    'id': student.student_id,
                    'email': student.user.email,
                }
            else:
                return errorResponse

        token = jwt.encode(payload, "SECRET_KEY")
        return Response({'token': token})


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


