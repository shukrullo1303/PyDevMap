from src.core.models.base import *


class OrderModel(BaseModel):
    STATUS_PENDING  = 'pending'
    STATUS_PAID     = 'paid'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_PENDING,   'Kutilmoqda'),
        (STATUS_PAID,      'To\'langan'),
        (STATUS_CANCELLED, 'Bekor qilingan'),
    ]

    PROVIDER_PAYME = 'payme'
    PROVIDER_CLICK = 'click'
    PROVIDER_FREE  = 'free'
    PROVIDER_CHOICES = [
        (PROVIDER_PAYME, 'Payme'),
        (PROVIDER_CLICK, 'Click'),
        (PROVIDER_FREE,  'Bepul'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course      = models.ForeignKey('CourseModel', on_delete=models.CASCADE, related_name='orders')
    amount      = models.DecimalField(max_digits=12, decimal_places=0)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    provider    = models.CharField(max_length=20, choices=PROVIDER_CHOICES, default=PROVIDER_PAYME)

    # To'lov tizimidan kelgan ID
    transaction_id = models.CharField(max_length=255, blank=True, null=True, unique=True)

    class Meta:
        unique_together = ('user', 'course', 'status')
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} — {self.user.username} — {self.course.title} — {self.status}"
