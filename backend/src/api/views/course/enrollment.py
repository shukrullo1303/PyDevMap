from src.api.views.base import *


class EnrollmentViewSet(BaseViewSet):
    """
    ViewSet for managing course enrollments.
    """
    queryset = EnrollmentModel.objects.all()
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields =  ["user"]

    # def get_queryset(self):
    #     """
    #     Optionally restricts the returned enrollments to a given user,
    #     by filtering against a `user_id` query parameter in the URL.
    #     """
    #     queryset = super().get_queryset()
    #     user_id = self.request.query_params.get('user_id')
    #     if user_id is not None:
    #         queryset = queryset.filter(user__id=user_id)
    #     return queryset