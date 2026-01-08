from src.api.urls.base import * 

router = DefaultRouter()
router.register("", LessonProgressViewSet, basename="lesson-progress")
urlpatterns = router.urls
