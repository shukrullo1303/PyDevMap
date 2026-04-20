from src.core.models.base import *


class PlacementSession(BaseModel):
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_COMPLETED   = 'completed'

    LEVEL_BEGINNER     = 'beginner'
    LEVEL_INTERMEDIATE = 'intermediate'
    LEVEL_ADVANCED     = 'advanced'
    LEVEL_EXPERT       = 'expert'

    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='placement_sessions')
    status     = models.CharField(max_length=20, default=STATUS_IN_PROGRESS)
    total_score    = models.IntegerField(default=0)
    max_score      = models.IntegerField(default=0)
    percentage     = models.FloatField(default=0.0)
    result_level   = models.CharField(max_length=20, blank=True, default='')

    # Adaptiv holat: har bir topic uchun to'g'ri/noto'g'ri soni
    topic_stats    = models.JSONField(default=dict)   # {"basics": {"correct": 2, "wrong": 1}, ...}
    current_q_num  = models.IntegerField(default=0)   # nechta savol berildi
    total_questions = models.IntegerField(default=25)

    # AI tahlil natijasi
    ai_analysis    = models.TextField(blank=True, default='')
    recommended_courses = models.JSONField(default=list)  # [course_id, ...]

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} — {self.result_level or 'jarayonda'} — {self.percentage:.0f}%"


class PlacementResponse(BaseModel):
    session  = models.ForeignKey(PlacementSession, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey('PlacementQuestion', on_delete=models.CASCADE)
    user_answer = models.TextField()
    is_correct  = models.BooleanField(default=False)
    time_spent  = models.IntegerField(default=0)  # soniyada
    question_num = models.IntegerField(default=0)

    class Meta:
        ordering = ['question_num']
