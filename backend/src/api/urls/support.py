from django.urls import path
from src.api.views.support import (
    UserSupportView,
    AdminSupportListView,
    AdminSupportReplyView,
    AdminMarkReadView,
)

urlpatterns = [
    path('',              UserSupportView.as_view(),      name='support-user'),
    path('admin/',        AdminSupportListView.as_view(), name='support-admin-list'),
    path('<int:pk>/reply/', AdminSupportReplyView.as_view(), name='support-admin-reply'),
    path('<int:pk>/read/', AdminMarkReadView.as_view(),   name='support-admin-read'),
]
