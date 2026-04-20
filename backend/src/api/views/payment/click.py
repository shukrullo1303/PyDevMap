"""
Click Shop API (SHOP API 2.0)
Docs: https://docs.click.uz/

Click server → bizning server ga 2 ta so'rov yuboradi:
  prepare  — to'lov mumkinmi? (action=0)
  complete — to'lov amalga oshdi (action=1)
"""

import hashlib
import os
from src.api.views.base import *

CLICK_SERVICE_ID  = os.environ.get('CLICK_SERVICE_ID', '')
CLICK_SECRET_KEY  = os.environ.get('CLICK_SECRET_KEY', '')

CLICK_ERR_OK                 = 0
CLICK_ERR_SIGN               = -1
CLICK_ERR_ORDER_NOT_FOUND    = -5
CLICK_ERR_ALREADY_PAID       = -4
CLICK_ERR_CANCELLED          = -9


def _verify_sign(click_trans_id, service_id, secret_key, merchant_trans_id, amount, action, sign_time, sign_string):
    source = f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{amount}{action}{sign_time}"
    expected = hashlib.md5(source.encode()).hexdigest()
    return expected == sign_string


class ClickView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        d = request.data

        click_trans_id    = d.get('click_trans_id', '')
        service_id        = d.get('service_id', '')
        merchant_trans_id = d.get('merchant_trans_id', '')  # bu bizning order.id
        amount            = d.get('amount', '')
        action            = d.get('action', '')
        sign_time         = d.get('sign_time', '')
        sign_string       = d.get('sign_string', '')

        # Imzo tekshiruvi
        if CLICK_SECRET_KEY and not _verify_sign(
            click_trans_id, service_id, CLICK_SECRET_KEY,
            merchant_trans_id, amount, action, sign_time, sign_string
        ):
            return Response({
                'error': CLICK_ERR_SIGN,
                'error_note': 'Invalid sign'
            })

        try:
            order = OrderModel.objects.get(id=merchant_trans_id)
        except OrderModel.DoesNotExist:
            return Response({
                'error': CLICK_ERR_ORDER_NOT_FOUND,
                'error_note': 'Order not found'
            })

        if int(action) == 0:
            return self._prepare(request, order, click_trans_id, amount)
        elif int(action) == 1:
            return self._complete(request, order, click_trans_id, amount)

        return Response({'error': -2, 'error_note': 'Invalid action'})

    def _prepare(self, request, order, click_trans_id, amount):
        if order.status == OrderModel.STATUS_PAID:
            return Response({'error': CLICK_ERR_ALREADY_PAID, 'error_note': 'Already paid'})

        if order.status == OrderModel.STATUS_CANCELLED:
            return Response({'error': CLICK_ERR_CANCELLED, 'error_note': 'Cancelled'})

        if int(float(amount)) != int(order.amount):
            return Response({'error': -2, 'error_note': 'Wrong amount'})

        order.transaction_id = click_trans_id
        order.provider = OrderModel.PROVIDER_CLICK
        order.save(update_fields=['transaction_id', 'provider'])

        return Response({
            'click_trans_id':    click_trans_id,
            'merchant_trans_id': str(order.id),
            'merchant_prepare_id': str(order.id),
            'error': CLICK_ERR_OK,
            'error_note': 'Success'
        })

    def _complete(self, request, order, click_trans_id, amount):
        if order.status == OrderModel.STATUS_PAID:
            return Response({
                'click_trans_id':    click_trans_id,
                'merchant_trans_id': str(order.id),
                'merchant_confirm_id': str(order.id),
                'error': CLICK_ERR_OK,
                'error_note': 'Success'
            })

        if order.status == OrderModel.STATUS_CANCELLED:
            return Response({'error': CLICK_ERR_CANCELLED, 'error_note': 'Cancelled'})

        order.status = OrderModel.STATUS_PAID
        order.save(update_fields=['status'])

        EnrollmentModel.objects.get_or_create(
            user=order.user,
            course=order.course,
            defaults={'is_paid': True}
        )

        return Response({
            'click_trans_id':    click_trans_id,
            'merchant_trans_id': str(order.id),
            'merchant_confirm_id': str(order.id),
            'error': CLICK_ERR_OK,
            'error_note': 'Success'
        })


# ── Order yaratish (frontend chaqiradi) ─────────────────────
class CreateClickOrderView(APIView):
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

        order, _ = OrderModel.objects.get_or_create(
            user=request.user,
            course=course,
            status=OrderModel.STATUS_PENDING,
            defaults={
                'amount':   course.price,
                'provider': OrderModel.PROVIDER_CLICK,
            }
        )

        # Click to'lov URL
        checkout_url = (
            f"https://my.click.uz/services/pay"
            f"?service_id={CLICK_SERVICE_ID}"
            f"&merchant_id={CLICK_SERVICE_ID}"
            f"&amount={int(order.amount)}"
            f"&transaction_param={order.id}"
            f"&return_url=https://pydevmap.com/courses"
        )

        return Response({
            'order_id':     order.id,
            'amount':       order.amount,
            'checkout_url': checkout_url,
        })
