from src.api.serializers.base import * 


class QuizResultSerializer(BaseSerializer):
    class Meta:
        model = QuizResultModel
        fields = '__all__'
        