from src.api.urls.base import * 

router = DefaultRouter()
router.register("", EnrollmentViewSet, basename="enrollment")
urlpatterns = router.urls
