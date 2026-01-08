from src.api.serializers.base import *
from src.api.serializers.lesson.lesson import LessonSerializer


class CourseSerializer(BaseSerializer):
    class Meta:
        model = CourseModel
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'level', 'category', 'price', 'slug']

# class CourseDetailSerializer(BaseSerializer):
#     lessons = LessonSerializer(many=True, read_only=True)
#     class Meta:
#         model = CourseModel
#         fields = ['id', 'title', 'description', 'lessons', 'created_at', 'updated_at', 'level', 'category', 'price', 'slug']
