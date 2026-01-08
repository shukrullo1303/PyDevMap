from src.core.models.base import *


class SubmissionModel(BaseModel):
    task = models.ForeignKey("TaskModel", on_delete=models.CASCADE)
    code = models.TextField()         # Foydalanuvchi yozgan kod
    status = models.CharField(max_length=20, default='Pending') # Success / Fail
    result = models.TextField(blank=True)