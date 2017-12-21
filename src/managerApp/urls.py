from django.conf.urls import url

from .views import index, Login

urlpatterns = [
    url(r'^$', index),
    url(r'login/$', Login.as_view())

]