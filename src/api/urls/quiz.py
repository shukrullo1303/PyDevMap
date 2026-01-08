from src.api.urls.base import *

router = DefaultRouter()
router.register('', QuizViewSet, basename='')

urlpatterns = [
    
]
urlpatterns += router.urls
