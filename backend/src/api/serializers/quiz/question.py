from src.api.serializers.base import * 
from src.api.serializers.quiz.answer import AnswerSerializer


class QuestionSerializer(BaseSerializer):
    answers = AnswerSerializer(many=True)
    class Meta:
        model = QuestionModel
        fields = ['id', 'text', 'answers' ]
    
