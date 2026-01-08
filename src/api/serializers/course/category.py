from src.api.serializers.base import *


class CategorySerializer(BaseSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'