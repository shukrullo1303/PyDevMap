from src.core.models.base import *


class QuizModel(BaseModel):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey('LessonModel', on_delete=models.SET_NULL, null=True, related_name='quizzes')
    # total_questions = models.PositiveIntegerField()


    def __str__(self):
        return self.title
