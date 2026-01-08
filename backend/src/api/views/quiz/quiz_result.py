from src.api.views.base import * 


class QuizResultViewSet(BaseViewSet):
    queryset = QuizResultModel.objects.all()
    serializer_class = QuizResultSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['quiz']