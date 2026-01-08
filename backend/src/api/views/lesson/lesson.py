from src.api.views.base import *


class LessonViewSet(BaseViewSet):
    queryset = LessonModel.objects.all()
    serializer_class = LessonSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['course']
    search_fields = ["course"]
    ordering_fields = ("created_at", "title")
    ordering = ("-created_at",)

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOnly()]
        return []
    
    @action(detail=True, methods=['post'], url_path="complete")
    def complete(self, request, pk=None):
        lesson = self.get_object()  # pk orqali lesson
        user = request.user
        try:
            progress, created = LessonProgressModel.objects.get_or_create(
                user=user,
                lesson=lesson
            )
            progress.completed = True
            progress.save()
            return Response({"detail": "Lesson marked as completed."}, status=200)
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
