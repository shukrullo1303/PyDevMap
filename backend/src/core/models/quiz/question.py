from src.core.models.base import *


class QuestionModel(BaseModel):
    text = models.TextField()
    quiz = models.ForeignKey("QuizModel", on_delete=models.SET_NULL, null=True, related_name="questions")
    
