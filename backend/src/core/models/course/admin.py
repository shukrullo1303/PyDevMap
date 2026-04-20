from django.contrib import admin
from src.core.models import CategoryModel, CourseModel, EnrollmentModel, OrderModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(CourseModel)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'level', 'price', 'is_free']
    list_filter = ['category', 'level', 'is_free']
    search_fields = ['title']


@admin.register(EnrollmentModel)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'course']
    list_filter = ['course']
    search_fields = ['user__username']


@admin.register(OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'course', 'amount', 'status', 'provider', 'created_at']
    list_filter = ['status', 'provider']
    search_fields = ['user__username', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
