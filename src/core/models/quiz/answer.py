from src.core.models.base import *


class AnswerModel(BaseModel):
    text = models.TextField()
    question = models.ForeignKey("QuestionModel", on_delete=models.SET_NULL, null=True, related_name="answers")
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text