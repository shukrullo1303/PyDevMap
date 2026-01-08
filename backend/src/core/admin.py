from django.contrib import admin
import nested_admin
from src.core.models import *


# ===== ANSWER INLINE =====
class AnswerInline(nested_admin.NestedTabularInline):
    model = AnswerModel
    extra = 1
    fields = ['text', 'is_correct']


# ===== QUESTION INLINE (for Quiz) =====
class QuestionInline(nested_admin.NestedStackedInline):
    model = QuestionModel
    extra = 1
    inlines = [AnswerInline]
    fields = ['text', 'quiz']


# ===== QUIZ ADMIN (Nested) =====
class QuizInline(nested_admin.NestedStackedInline):
    model = QuizModel
    extra = 1
    inlines = [QuestionInline]
    fields = ['title']


# ===== LESSON ADMIN (Nested) =====
class LessonInline(nested_admin.NestedStackedInline):
    model = LessonModel
    extra = 1
    inlines = [QuizInline]
    fields = ['title', 'order', 'content']


# ===== COURSE ADMIN (Nested) =====
@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CourseModel)
class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'category', 'level', 'price']
    list_filter = ['category', 'level']
    search_fields = ['title']
    # inlines = [LessonInline]


@admin.register(LessonModel)
class LessonAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'course', 'order']
    list_filter = ['course']
    search_fields = ['title']
    inlines = [QuizInline]


@admin.register(QuizModel)
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ['title', 'lesson']
    list_filter = ['lesson']
    search_fields = ['title']
    inlines = [QuestionInline]


@admin.register(QuestionModel)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz']
    list_filter = ['quiz']
    search_fields = ['text']


@admin.register(AnswerModel)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct']
    list_filter = ['is_correct']
    search_fields = ['text']


@admin.register(QuizResultModel)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']


@admin.register(EnrollmentModel)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['course']
    search_fields = ['user__username']


@admin.register(LessonProgressModel)
class LessonProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed']
    list_filter = ['completed']
    search_fields = ['user__username']


