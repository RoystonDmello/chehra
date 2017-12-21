from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


import jwt, json, jsonpickle

from .models import Teacher


# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse({'text': 'hello This is index page',
                         'status': '200 OK'})


class Register(APIView):

    def post(self, request, *args, **kwargs):
        if not request.POST:
            return Response({'Error': "Please provide username/password"}, status="400")

        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.create(email=email, username=username)
            user.set_password(password)
            user.save()
            instance = Teacher(user=user)
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
        try:
            user = authenticate(username=username, password=password)
            teacher = Teacher.objects.get(user=user)
        except Exception as e:
            print(e)
            return Response({'Error': "Invalid username/password"}, status="400")
        if teacher:
            payload = {
                'id': teacher.teacher_id,
                'email': teacher.user.email,
            }
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
            serialized_data = jsonpickle.encode(jwt_token)
            return JsonResponse(
                serialized_data,
                status=200,
                content_type="application/json",
                safe=False
            )
        else:
            return JsonResponse(
                json.dumps({'Error': "Invalid credentials"}),
                status=400,
                content_type="application/json",
                safe=False
            )


