from src.api.views.base import *


class CompleteLessonAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_id):
        progress, _ = LessonProgressModel.objects.get_or_create(
            user=request.user,
            lesson_id=lesson_id
        )
        progress.is_completed = True
        progress.save()
        return Response({"status": "completed"})
