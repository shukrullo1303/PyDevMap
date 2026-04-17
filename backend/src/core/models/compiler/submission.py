from src.core.models.base import *


POINTS_MAP = {
    'Beginner': 10,
    'Intermediate': 20,
    'Professional': 30,
}


class SubmissionModel(BaseModel):
    task = models.ForeignKey("TaskModel", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='submissions')
    code = models.TextField()
    status = models.CharField(max_length=20, default='Pending')  # Success / Fail
    result = models.TextField(blank=True)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)

    class Meta:
        ordering = ['-created_at']