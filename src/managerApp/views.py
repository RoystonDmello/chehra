from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.
def index(request):
    return JsonResponse({'text': 'hello This is index page',
                         'status': '200 OK'})
