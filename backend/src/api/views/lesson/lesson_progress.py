from src.api.views.base import *


# example: Django ViewSet
class LessonProgressViewSet(BaseViewSet):
    queryset = LessonProgressModel.objects.all()
    serializer_class = LessonProgressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(lesson__course__id=course_id, user=self.request.user)
        else:
            queryset = queryset.filter(user=self.request.user)
        return queryset