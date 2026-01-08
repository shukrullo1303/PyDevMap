from src.api.serializers.base import *


class LessonProgressSerializer(BaseSerializer):
    class Meta:
        model = LessonProgressModel
        fields = '__all__'