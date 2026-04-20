from src.api.serializers.base import *


class EnrollmentSerializer(BaseSerializer):
    course_title = serializers.SerializerMethodField()
    course_slug  = serializers.SerializerMethodField()

    class Meta:
        model = EnrollmentModel
        fields = '__all__'

    def get_course_title(self, obj):
        return obj.course.title if obj.course else None

    def get_course_slug(self, obj):
        return obj.course.slug if obj.course else None
