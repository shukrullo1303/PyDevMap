from src.api.serializers.base import *
from src.api.serializers.quiz.question import QuestionSerializer
from src.api.serializers.quiz.quiz_result import QuizResultSerializer


class QuizSerializer(BaseSerializer):
    questions = QuestionSerializer(many=True)
    related_task_id = serializers.SerializerMethodField()
    related_task_title = serializers.SerializerMethodField()
    related_task_difficulty = serializers.SerializerMethodField()

    class Meta:
        model = QuizModel
        fields = "__all__"

    def get_related_task_id(self, obj):
        return obj.related_task_id

    def get_related_task_title(self, obj):
        return obj.related_task.title if obj.related_task else None

    def get_related_task_difficulty(self, obj):
        return obj.related_task.difficulty if obj.related_task else None


class QuizSubmitSerializer(serializers.Serializer):
    answers = serializers.DictField(
        child=serializers.IntegerField(), 
        help_text="Question ID => Answer ID mapping"
    )