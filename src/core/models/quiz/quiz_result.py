from src.core.models.base import *


class QuizResultModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
    quiz = models.ForeignKey("QuizModel", on_delete=models.CASCADE, related_name='quiz', null=True, blank=True)
    score = models.FloatField(null=True)

    class Meta:
        unique_together = ('user', 'quiz')