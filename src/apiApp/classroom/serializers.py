from rest_framework.serializers import ModelSerializer
from ..models import Classroom


class ClassroomSerializer(ModelSerializer):
    class Meta:
        model = Classroom
        fields = ['classroom_id', 'classroom_name']
