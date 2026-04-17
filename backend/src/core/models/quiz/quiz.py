from src.core.models.base import *


class QuizModel(BaseModel):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey('LessonModel', on_delete=models.SET_NULL, null=True, related_name='quizzes')
    related_task = models.ForeignKey(
        'TaskModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='quizzes'
    )


    def __str__(self):
        return self.title
