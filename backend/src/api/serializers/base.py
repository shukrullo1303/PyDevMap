from rest_framework import serializers
from src.core.models.base import *

from src.core.models import *
from src.api.serializers import *
from src.api.views.utils import can_user_open_lesson

class BaseSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M")
        representation['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M")
        return representation