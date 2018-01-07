from rest_framework.serializers import ModelSerializer

from ..models import Course


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'dept_id', 'teacher_id', 'name', 'description', 'academic_yr', 'year']


class CourseDetailSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'dept_id', 'teacher_id',
                  'name', 'description', 'academic_yr', 'year',
                  'updated', 'created']
