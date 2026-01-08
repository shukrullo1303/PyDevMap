from src.api.views.base import * 


class QuestionViewSet(BaseViewSet):
    queryset = QuestionModel.objects.all()
    serializer_class = QuestionSerializer
    search_fields = ("text",)
    ordering_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)