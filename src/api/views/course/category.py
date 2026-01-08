from src.api.views.base import *


class CategoryViewSet(BaseViewSet):
    queryset = CategoryModel.objects.all()
    serializer_class = CategorySerializer
    search_fields = ['name', 'description']
    # ordering = ['courses.enrollments__count']   # xatolik bor

    