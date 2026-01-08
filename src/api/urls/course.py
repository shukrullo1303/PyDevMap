from src.api.urls.base import *


router = DefaultRouter()
router.register("", CourseViewSet, basename="course")
router.register("categories", CategoryViewSet, basename="category")
router.register("enrollments", EnrollmentViewSet, basename="enrollment")

urlpatterns = router.urls