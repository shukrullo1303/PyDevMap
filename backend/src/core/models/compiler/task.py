from src.core.models.base import *


DIFFICULTY_CHOICES = [
    ('Beginner', 'Beginner'),
    ('Intermediate', 'Intermediate'),
    ('Professional', 'Professional'),
]


class TaskModel(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    test_code = models.TextField()
    starter_code = models.TextField(blank=True, default='# Kodingizni shu yerga yozing\n')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Beginner')
    expected_output = models.TextField(blank=True, default='')
    course = models.ForeignKey(
        'CourseModel', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['difficulty', 'created_at']
