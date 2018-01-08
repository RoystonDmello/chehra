from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from ..models import Lecture


class LectureCreateSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'start_time', 'end_time',
                  'comment', 'updated', 'created', 'classroom']


class LectureListSerializer(ModelSerializer):
    class Meta:
        model = Lecture
        fields = ['lect_id', 'course_id', 'lect_no', 'start_time', 'end_time',
                  'isAttendanceTaken', 'comment', 'updated', 'created',
                  'classroom']


class CalendarDatesSerializer(serializers.Serializer):

    lect_id = serializers.CharField(read_only=True)
    course_id = serializers.CharField(read_only=True)
    lect_no = serializers.CharField(read_only=True)
    start_time = serializers.CharField(read_only=True)
    end_time = serializers.CharField(read_only=True)
    comment = serializers.CharField(read_only=True)
    updated = serializers.CharField(read_only=True)
    created = serializers.CharField(read_only=True)
    is_present=serializers.BooleanField(default=False)