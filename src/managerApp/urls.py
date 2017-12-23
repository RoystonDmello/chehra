from django.conf.urls import url
from .views import index
from .auth.views import Login, Register

urlpatterns = [
    url(r'^$', index),

    # auth
    url(r'^login/$', Login.as_view()),
    url(r'^register/$', Register.as_view())

]