from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from src.core.models.support import SupportMessage


def _msg_dict(msg):
    return {
        'id':         msg.id,
        'message':    msg.message,
        'reply':      msg.reply,
        'replied_at': msg.replied_at,
        'is_read':    msg.is_read,
        'created_at': msg.created_at,
        'username':   msg.user.username,
        'user_id':    msg.user_id,
    }


class UserSupportView(APIView):
    """GET mening xabarlarim / POST yangi xabar yuborish."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        msgs = SupportMessage.objects.filter(user=request.user)
        return Response([_msg_dict(m) for m in msgs])

    def post(self, request):
        text = request.data.get('message', '').strip()
        if not text:
            return Response({'error': 'Xabar bo\'sh bo\'lishi mumkin emas'}, status=400)
        msg = SupportMessage.objects.create(user=request.user, message=text)
        return Response(_msg_dict(msg), status=201)


class AdminSupportListView(APIView):
    """Admin: barcha xabarlar ro'yxati."""
    permission_classes = [IsAdminUser]

    def get(self, request):
        msgs = SupportMessage.objects.select_related('user').all()
        return Response([_msg_dict(m) for m in msgs])


class AdminSupportReplyView(APIView):
    """Admin: bitta xabarga javob berish.
    POST /api/support/<id>/reply/  { reply: '...' }
    """
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            msg = SupportMessage.objects.get(id=pk)
        except SupportMessage.DoesNotExist:
            return Response({'error': 'Xabar topilmadi'}, status=404)

        reply_text = request.data.get('reply', '').strip()
        if not reply_text:
            return Response({'error': 'Javob matni bo\'sh bo\'lishi mumkin emas'}, status=400)

        msg.reply      = reply_text
        msg.replied_at = timezone.now()
        msg.is_read    = True
        msg.save(update_fields=['reply', 'replied_at', 'is_read'])
        return Response(_msg_dict(msg))

    def delete(self, request, pk):
        """Admin: xabarni o'chirish."""
        try:
            msg = SupportMessage.objects.get(id=pk)
        except SupportMessage.DoesNotExist:
            return Response({'error': 'Xabar topilmadi'}, status=404)
        msg.delete()
        return Response({'success': True})


class AdminMarkReadView(APIView):
    """Admin: xabarni o'qildi deb belgilash."""
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        try:
            msg = SupportMessage.objects.get(id=pk)
        except SupportMessage.DoesNotExist:
            return Response({'error': 'Xabar topilmadi'}, status=404)
        msg.is_read = True
        msg.save(update_fields=['is_read'])
        return Response({'success': True})
