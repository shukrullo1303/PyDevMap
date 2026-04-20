from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from src.core.models.user_profile import UserProfile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    avatar_url = None
    if profile.avatar:
        try:
            avatar_url = request.build_absolute_uri(profile.avatar.url)
        except Exception:
            pass

    return Response({
        'id':           user.id,
        'username':     user.username,
        'email':        user.email,
        'first_name':   user.first_name,
        'last_name':    user.last_name,
        'is_staff':     user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined':  user.date_joined,
        'name_locked':  profile.name_locked,
        'avatar_url':   avatar_url,
    })
