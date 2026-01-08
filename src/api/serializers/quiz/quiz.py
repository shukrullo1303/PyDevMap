from src.api.serializers.base import *
from src.api.serializers.quiz.question import QuestionSerializer
from src.api.serializers.quiz.quiz_result import QuizResultSerializer


class QuizSerializer(BaseSerializer):
    questions = QuestionSerializer(many=True)
    
    class Meta:
        model = QuizModel
        fields = "__all__"


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.IntegerField(), 
        help_text="Question ID => Answer ID mapping"
    )