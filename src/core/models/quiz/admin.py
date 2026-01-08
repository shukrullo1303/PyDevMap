from django.contrib import admin
from src.core.models import QuizModel, QuestionModel, AnswerModel, QuizResultModel


@admin.register(QuizModel)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson']
    list_filter = ['lesson']
    search_fields = ['title']


@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'quiz']
    list_filter = ['quiz']
    search_fields = ['title']


@admin.register(AnswerModel)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['text']


@admin.register(QuizResultModel)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score']
    list_filter = ['quiz']
    search_fields = ['user__username']
