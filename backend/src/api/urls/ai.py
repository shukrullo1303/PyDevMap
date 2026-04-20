from src.api.urls.base import *

urlpatterns = [
    path('chat/',        AiChatView.as_view(),    name='ai-chat'),
    path('code-review/', CodeReviewView.as_view(), name='ai-code-review'),
]
