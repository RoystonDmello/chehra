from rest_framework.serializers import ModelSerializer

from ..models import Course, CourseData


class CourseCreateSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'dept_id', 'teacher_id', 'name', 'description',
                  'academic_yr', 'year']


class CourseDetailSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_id', 'dept_id', 'teacher_id',
                  'name', 'description', 'academic_yr', 'year',
                  'updated', 'created']


class CourseDataSerializer(ModelSerializer):
    class Meta:
        model = CourseData
        fields = ['data_id', 'course_id', 'data']
