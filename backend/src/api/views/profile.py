from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from src.core.models.user_profile import UserProfile


def _profile_data(request, user):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    avatar_url = None
    if profile.avatar:
        try:
            avatar_url = request.build_absolute_uri(profile.avatar.url)
        except Exception:
            avatar_url = None
    return {
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
    }


class UpdateProfileView(APIView):
    """PATCH /api/auth/profile/ — username, first_name, last_name."""
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user    = request.user
        profile, _ = UserProfile.objects.get_or_create(user=user)
        data    = request.data

        # Ism/familiya o'zgartirish — sertifikat olingan bo'lsa bloklash
        if ('first_name' in data or 'last_name' in data) and profile.name_locked:
            return Response(
                {'error': "Sertifikat olgandan keyin ism-familiyani o'zgartirish mumkin emas."},
                status=400
            )

        if 'username' in data:
            new_uname = data['username'].strip()
            if not new_uname:
                return Response({'error': 'Username bo\'sh bo\'lishi mumkin emas'}, status=400)
            if User.objects.filter(username=new_uname).exclude(id=user.id).exists():
                return Response({'error': 'Bu username allaqachon band'}, status=400)
            user.username = new_uname

        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()

        user.save()
        return Response({'success': True, **_profile_data(request, user)})


class ChangePasswordView(APIView):
    """POST /api/auth/password/ — parolni almashtirish."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user         = request.user
        old_password = request.data.get('old_password', '')
        new_password = request.data.get('new_password', '')

        if not user.check_password(old_password):
            return Response({'error': 'Joriy parol noto\'g\'ri'}, status=400)
        if len(new_password) < 8:
            return Response({'error': 'Yangi parol kamida 8 ta belgidan iborat bo\'lishi kerak'}, status=400)

        user.set_password(new_password)
        user.save()
        return Response({'success': True})


class UploadAvatarView(APIView):
    """POST /api/auth/avatar/ — profil rasmini yuklash."""
    permission_classes = [IsAuthenticated]
    parser_classes     = [MultiPartParser, FormParser]

    def post(self, request):
        file = request.FILES.get('avatar')
        if not file:
            return Response({'error': 'Fayl yuklanmadi'}, status=400)

        # Faqat rasm fayllarini qabul qilish
        allowed = ('image/jpeg', 'image/png', 'image/webp', 'image/gif')
        if file.content_type not in allowed:
            return Response({'error': 'Faqat JPG, PNG, WEBP, GIF formatlar qabul qilinadi'}, status=400)

        if file.size > 5 * 1024 * 1024:  # 5 MB
            return Response({'error': 'Fayl hajmi 5 MB dan oshmasligi kerak'}, status=400)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar = file
        profile.save(update_fields=['avatar'])

        avatar_url = request.build_absolute_uri(profile.avatar.url)
        return Response({'success': True, 'avatar_url': avatar_url})
