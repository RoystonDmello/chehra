from rest_framework.serializers import ModelSerializer

from ..models import Lecture


class LectureCreateSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'duration', 'comment',
                  'updated', 'created']


class LectureListSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'duration', 'comment',
                  'updated', 'created']
