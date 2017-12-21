from django.http import JsonResponse
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from django.contrib.auth import authenticate

import jwt, json, jsonpickle

from .models import Teacher


# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse({'text': 'hello This is index page',
                         'status': '200 OK'})


class Login(APIView):

    def post(self, request, *args, **kwargs):
        if not request.data:
            return Response({'Error': "Please provide username/password"}, status="400")

        username = request.data['username']
        password = request.data['password']
        try:
            user = authenticate(username=username, password=password)
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({'Error': "Invalid username/password"}, status="400")
        if teacher:
            payload = {
                'id': teacher.teacher_id,
                'email': teacher.user.email,
            }
            jwt_token = {'token': jwt.encode(payload, "SECRET_KEY")}
            serialized_data = jsonpickle.encode(jwt_token)
            return JsonResponse(
                json.dumps(serialized_data),
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
