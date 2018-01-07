from rest_framework.serializers import ModelSerializer

from ..models import Lecture


class LectureCreateSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'start_time', 'end_time',
                  'comment', 'updated', 'created']


class LectureListSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'start_time', 'end_time',
                  'comment', 'updated', 'created']