from src.api.serializers.base import *


class AnswerSerializer(BaseSerializer):
    
    class Meta:
        model = AnswerModel
        fields = '__all__'
        