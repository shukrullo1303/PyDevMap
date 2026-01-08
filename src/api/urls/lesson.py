from src.api.urls.base import * 

router = DefaultRouter()
router.register("", LessonViewSet, basename="lesson")
urlpatterns = router.urls
