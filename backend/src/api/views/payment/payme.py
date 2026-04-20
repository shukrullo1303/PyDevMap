"""
Payme Merchant API (Subscribe API)
Docs: https://developer.paycom.uz/

Payme server → bizning server ga quyidagi metodlarni chaqiradi:
  CheckPerformTransaction  — to'lov mumkinmi?
  CreateTransaction        — tranzaksiya yaratish
  PerformTransaction       — to'lovni tasdiqlash (mablag' o'tkazildi)
  CancelTransaction        — bekor qilish
  CheckTransaction         — tranzaksiya holati
  GetStatement             — hisobot
"""

import base64
import os
from src.api.views.base import *


PAYME_ID  = os.environ.get('PAYME_ID', '')
PAYME_KEY = os.environ.get('PAYME_KEY', '')

ERR_INVALID_JSON        = -32700
ERR_METHOD_NOT_FOUND    = -32601
ERR_INVALID_AMOUNT      = -31001
ERR_ORDER_NOT_FOUND     = -31050
ERR_ALREADY_PAID        = -31051
ERR_TRANSACTION_EXISTS  = -31052
ERR_CANT_PERFORM        = -31008
ERR_CANT_CANCEL         = -31007


def _auth_ok(request):
    auth = request.headers.get('Authorization', '')
    if not auth.startswith('Basic '):
        return False
    try:
        decoded = base64.b64decode(auth[6:]).decode()
        _, key = decoded.split(':', 1)
        return key == PAYME_KEY
    except Exception:
        return False


class PaymeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if not _auth_ok(request):
            return Response({
                'error': {'code': -32504, 'message': 'Unauthorized'},
                'id': request.data.get('id')
            }, status=401)

        data   = request.data
        method = data.get('method')
        params = data.get('params', {})
        rpc_id = data.get('id')

        handler = {
            'CheckPerformTransaction': self._check_perform,
            'CreateTransaction':       self._create,
            'PerformTransaction':      self._perform,
            'CancelTransaction':       self._cancel,
            'CheckTransaction':        self._check,
            'GetStatement':            self._statement,
        }.get(method)

        if not handler:
            return Response({
                'error': {'code': ERR_METHOD_NOT_FOUND, 'message': 'Method not found'},
                'id': rpc_id
            })

        return handler(params, rpc_id)

    # ── CheckPerformTransaction ──────────────────────────────
    def _check_perform(self, params, rpc_id):
        order_id = params.get('account', {}).get('order_id')
        amount   = params.get('amount')  # tiyin

        try:
            order = OrderModel.objects.get(id=order_id, status=OrderModel.STATUS_PENDING)
        except OrderModel.DoesNotExist:
            return Response({'error': {'code': ERR_ORDER_NOT_FOUND, 'message': 'Order not found'}, 'id': rpc_id})

        expected_tiyin = int(order.amount) * 100
        if int(amount) != expected_tiyin:
            return Response({'error': {'code': ERR_INVALID_AMOUNT, 'message': 'Wrong amount'}, 'id': rpc_id})

        return Response({'result': {'allow': True}, 'id': rpc_id})

    # ── CreateTransaction ────────────────────────────────────
    def _create(self, params, rpc_id):
        order_id       = params.get('account', {}).get('order_id')
        amount         = params.get('amount')
        transaction_id = params.get('id')
        create_time    = params.get('time')

        try:
            order = OrderModel.objects.get(id=order_id)
        except OrderModel.DoesNotExist:
            return Response({'error': {'code': ERR_ORDER_NOT_FOUND, 'message': 'Order not found'}, 'id': rpc_id})

        if order.status == OrderModel.STATUS_PAID:
            return Response({'error': {'code': ERR_ALREADY_PAID, 'message': 'Already paid'}, 'id': rpc_id})

        expected_tiyin = int(order.amount) * 100
        if int(amount) != expected_tiyin:
            return Response({'error': {'code': ERR_INVALID_AMOUNT, 'message': 'Wrong amount'}, 'id': rpc_id})

        # Mavjud tranzaksiyani tekshir
        if order.transaction_id and order.transaction_id != transaction_id:
            return Response({'error': {'code': ERR_TRANSACTION_EXISTS, 'message': 'Transaction exists'}, 'id': rpc_id})

        order.transaction_id = transaction_id
        order.save(update_fields=['transaction_id'])

        return Response({
            'result': {
                'create_time': create_time,
                'transaction': str(order.id),
                'state': 1,
            },
            'id': rpc_id
        })

    # ── PerformTransaction ───────────────────────────────────
    def _perform(self, params, rpc_id):
        transaction_id = params.get('id')

        try:
            order = OrderModel.objects.get(transaction_id=transaction_id)
        except OrderModel.DoesNotExist:
            return Response({'error': {'code': ERR_ORDER_NOT_FOUND, 'message': 'Order not found'}, 'id': rpc_id})

        if order.status == OrderModel.STATUS_PAID:
            pass  # idempotent — yana qaytaramiz
        elif order.status == OrderModel.STATUS_PENDING:
            order.status = OrderModel.STATUS_PAID
            order.save(update_fields=['status'])
            # Enrollment yaratish
            EnrollmentModel.objects.get_or_create(
                user=order.user,
                course=order.course,
                defaults={'is_paid': True}
            )

        import time
        return Response({
            'result': {
                'transaction': str(order.id),
                'perform_time': int(time.time() * 1000),
                'state': 2,
            },
            'id': rpc_id
        })

    # ── CancelTransaction ────────────────────────────────────
    def _cancel(self, params, rpc_id):
        transaction_id = params.get('id')
        reason         = params.get('reason', 0)

        try:
            order = OrderModel.objects.get(transaction_id=transaction_id)
        except OrderModel.DoesNotExist:
            return Response({'error': {'code': ERR_ORDER_NOT_FOUND, 'message': 'Order not found'}, 'id': rpc_id})

        if order.status == OrderModel.STATUS_PAID:
            # To'langan buyurtmani bekor qilib bo'lmaydi (kurs boshlangan bo'lishi mumkin)
            return Response({'error': {'code': ERR_CANT_CANCEL, 'message': 'Cannot cancel paid order'}, 'id': rpc_id})

        order.status = OrderModel.STATUS_CANCELLED
        order.save(update_fields=['status'])

        import time
        return Response({
            'result': {
                'transaction': str(order.id),
                'cancel_time': int(time.time() * 1000),
                'state': -1,
            },
            'id': rpc_id
        })

    # ── CheckTransaction ─────────────────────────────────────
    def _check(self, params, rpc_id):
        transaction_id = params.get('id')

        try:
            order = OrderModel.objects.get(transaction_id=transaction_id)
        except OrderModel.DoesNotExist:
            return Response({'error': {'code': ERR_ORDER_NOT_FOUND, 'message': 'Order not found'}, 'id': rpc_id})

        state_map = {
            OrderModel.STATUS_PENDING:   1,
            OrderModel.STATUS_PAID:      2,
            OrderModel.STATUS_CANCELLED: -1,
        }
        return Response({
            'result': {
                'create_time': int(order.created_at.timestamp() * 1000),
                'perform_time': int(order.updated_at.timestamp() * 1000) if order.status == OrderModel.STATUS_PAID else 0,
                'cancel_time': int(order.updated_at.timestamp() * 1000) if order.status == OrderModel.STATUS_CANCELLED else 0,
                'transaction': str(order.id),
                'state': state_map.get(order.status, 1),
                'reason': None,
            },
            'id': rpc_id
        })

    # ── GetStatement ─────────────────────────────────────────
    def _statement(self, params, rpc_id):
        from_ts = params.get('from', 0) / 1000
        to_ts   = params.get('to', 0) / 1000
        from datetime import datetime, timezone as tz

        orders = OrderModel.objects.filter(
            provider=OrderModel.PROVIDER_PAYME,
            status=OrderModel.STATUS_PAID,
            created_at__gte=datetime.fromtimestamp(from_ts, tz=tz.utc),
            created_at__lte=datetime.fromtimestamp(to_ts, tz=tz.utc),
        )
        transactions = []
        for o in orders:
            transactions.append({
                'id': o.transaction_id,
                'time': int(o.created_at.timestamp() * 1000),
                'amount': int(o.amount) * 100,
                'account': {'order_id': str(o.id)},
                'create_time': int(o.created_at.timestamp() * 1000),
                'perform_time': int(o.updated_at.timestamp() * 1000),
                'cancel_time': 0,
                'transaction': str(o.id),
                'state': 2,
                'reason': None,
            })
        return Response({'result': {'transactions': transactions}, 'id': rpc_id})


# ── Order yaratish (frontend chaqiradi) ─────────────────────
class CreatePaymeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get('course_id')
        try:
            course = CourseModel.objects.get(id=course_id)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Kurs topilmadi'}, status=404)

        if course.is_free or course.price == 0:
            enrollment, _ = EnrollmentModel.objects.get_or_create(
                user=request.user, course=course, defaults={'is_paid': True}
            )
            return Response({'enrolled': True, 'free': True})

        if EnrollmentModel.objects.filter(user=request.user, course=course).exists():
            return Response({'enrolled': True})

        # Eski pending orderni topamiz yoki yangisini yaratamiz
        order, _ = OrderModel.objects.get_or_create(
            user=request.user,
            course=course,
            status=OrderModel.STATUS_PENDING,
            defaults={
                'amount':   course.price,
                'provider': OrderModel.PROVIDER_PAYME,
            }
        )

        # Payme checkout URL (sum = tiyin)
        import base64
        amount_tiyin = int(order.amount) * 100
        payload = f"m={PAYME_ID};ac.order_id={order.id};a={amount_tiyin}"
        encoded = base64.b64encode(payload.encode()).decode()
        checkout_url = f"https://checkout.paycom.uz/{encoded}"

        return Response({
            'order_id':     order.id,
            'amount':       order.amount,
            'checkout_url': checkout_url,
        })
