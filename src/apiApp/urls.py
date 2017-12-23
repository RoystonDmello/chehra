from django.conf.urls import url, include
from .views import index
from .auth.views import Login, Register
from .department.views import (
    DepartmentListAPIView,
    DepartmentCreateAPIView,
    DepartmentDetailAPIView,
    DepartmentUpdateAPIView,
    DepartmentDeleteAPIView
)
from .course.views import (
    CourseCreateAPIView,
    CourseListAPIView,
    CourseDetailAPIView
)

urlpatterns = [
    url(r'^$', index),

    # auth
    url(r'^login/$', Login.as_view()),
    url(r'^register/$', Register.as_view()),


    # department
    url(r'^department/create/$', DepartmentCreateAPIView.as_view()),
    url(r'^department/get/$', DepartmentListAPIView.as_view()),
    url(r'^department/get/(?P<pk>\d+)/$', DepartmentDetailAPIView.as_view()),

    # put request eg: http://127.0.0.1:8000/api/department/update/2/ with params ['name']
    url(r'^department/update/(?P<pk>\d+)/$', DepartmentUpdateAPIView.as_view()),
    # delete request eg: http://127.0.0.1:8000/api/department/delete/2/
    url(r'^department/delete/(?P<pk>\d+)/$', DepartmentDeleteAPIView.as_view()),


    # course
    url(r'^course/create/$', CourseCreateAPIView.as_view()),
    url(r'^course/get/$', CourseListAPIView.as_view()),
    url(r'^course/get/(?P<pk>\d+)/$', CourseDetailAPIView.as_view()),


]