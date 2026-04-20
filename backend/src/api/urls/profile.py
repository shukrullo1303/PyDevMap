from django.urls import path
from src.api.views.profile import UpdateProfileView, ChangePasswordView, UploadAvatarView

urlpatterns = [
    path('profile/',  UpdateProfileView.as_view(),  name='update-profile'),
    path('password/', ChangePasswordView.as_view(), name='change-password'),
    path('avatar/',   UploadAvatarView.as_view(),   name='upload-avatar'),
]
