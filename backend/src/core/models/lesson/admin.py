from django.contrib import admin
from src.core.models import LessonModel, LessonProgressModel


@admin.register(LessonModel)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']
    fields = ['title', 'course', 'order', 'content', 'video_url', 'video_file', 'required_task']


@admin.register(LessonProgressModel)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed']
    list_filter = ['completed']
    search_fields = ['user__username']