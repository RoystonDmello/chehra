from django.conf.urls import url

from .views import index, Login, Register

urlpatterns = [
    url(r'^$', index),
    url(r'login/$', Login.as_view()),
    url(r'register/$', Register.as_view())

]