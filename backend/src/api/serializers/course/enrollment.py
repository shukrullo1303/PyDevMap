from src.api.serializers.base import *


class EnrollmentSerializer(BaseSerializer):
    class Meta:
        model = EnrollmentModel
        fields = '__all__'

    