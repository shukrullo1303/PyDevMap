from src.core.models.base import *


class DiscountCoupon(BaseModel):
    code          = models.CharField(max_length=20, unique=True)
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coupons')
    percentage    = models.IntegerField(default=30)   # 30% chegirma
    valid_until   = models.DateTimeField()
    is_used       = models.BooleanField(default=False)
    used_for_course = models.ForeignKey('CourseModel', on_delete=models.SET_NULL,
                                        null=True, blank=True, related_name='coupon_uses')
    # Placement test natijasiga bog'liq
    session       = models.OneToOneField('PlacementSession', on_delete=models.SET_NULL,
                                          null=True, blank=True, related_name='coupon')

    def __str__(self):
        return f"{self.code} — {self.user.username} — {self.percentage}%"
