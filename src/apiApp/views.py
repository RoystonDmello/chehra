from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
@csrf_exempt
def index(request):
    return JsonResponse({'text': 'hello This is index page',
                         'status': '200 OK'}
                        )
