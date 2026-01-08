from src.core.models.base import *


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()  # Masala sharti
    test_code = models.TextField()    # Tekshirish uchun unit-testlar
    created_at = models.DateTimeField(auto_now_add=True)

