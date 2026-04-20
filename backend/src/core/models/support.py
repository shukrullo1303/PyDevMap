from django.db import models
from django.contrib.auth.models import User


class SupportMessage(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_messages')
    message         = models.TextField()
    reply           = models.TextField(blank=True, null=True)
    replied_at      = models.DateTimeField(null=True, blank=True)
    is_read         = models.BooleanField(default=False)   # admin o'qidimi
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_messages'
        ordering = ['-created_at']

    def __str__(self):
        return f"SupportMessage({self.user.username}, {self.created_at:%Y-%m-%d})"
