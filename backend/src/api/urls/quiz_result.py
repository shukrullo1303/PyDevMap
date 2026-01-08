from src.api.urls.base import *

router = DefaultRouter()
router.register('', QuizResultViewSet, basename='quiz_result')

urlpatterns = [
    
]
urlpatterns += router.urls
