from src.api.urls.base import *

urlpatterns = [
    path('start/',    StartTestView.as_view(),     name='placement-start'),
    path('answer/',   AnswerView.as_view(),         name='placement-answer'),
    path('result/',   TestResultView.as_view(),     name='placement-result'),
    path('coupon/',   ValidateCouponView.as_view(), name='placement-coupon'),
]
