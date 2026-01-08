from src.api.views.base import *


class AnswerViewSet(BaseViewSet):
    queryset = AnswerModel.objects.all()
    serializer_class = AnswerSerializer
    search_fields = ("text",)
    ordering_fields = ("created_at", "updated_at")
    ordering = ("-created_at",)