from django.contrib import admin
from src.core.models import CategoryModel, CourseModel, EnrollmentModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CourseModel)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'price']
    list_filter = ['category', 'level']
    search_fields = ['title']


@admin.register(EnrollmentModel)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['course']
    search_fields = ['user__username']
