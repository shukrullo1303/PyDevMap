from src.core.models.base import * 


class LessonProgressModel(BaseModel):
    user = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, related_name='lesson_progress')
    lesson = models.ForeignKey('LessonModel', on_delete=models.SET_NULL, null=True, related_name='progress_records')
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')

    def mark_completed(self):
        self.completed = True
        self.updated_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Progress of {self.user.username} for {self.lesson.title}"