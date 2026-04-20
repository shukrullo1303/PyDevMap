from src.api.views.base import *
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor
import io
import qrcode
import hashlib
from datetime import datetime

# ── Ranglar ──────────────────────────────────────────
NAVY       = HexColor('#0a0c1a')
NAVY2      = HexColor('#12152a')
NAVY3      = HexColor('#1a1d35')
GOLD       = HexColor('#c99a20')
GOLD_LIGHT = HexColor('#e8b84b')
GOLD_PALE  = HexColor('#f5e6b8')
WHITE      = HexColor('#ffffff')
GRAY       = HexColor('#9a9cb0')
GRAY_DARK  = HexColor('#4a4c6a')
PY_BLUE    = HexColor('#3776ab')
PY_YELLOW  = HexColor('#ffd343')

LEVEL_COLORS = {
    'Beginner':     '#22c55e',
    'Intermediate': '#e8b84b',
    'Professional': '#ef4444',
}


def _draw_bg(c, W, H):
    """Fon va dekorativ ramkalar."""
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    c.setFillColor(NAVY2)
    c.roundRect(28, 28, W - 56, H - 56, 14, fill=1, stroke=0)

    # Tashqi oltin ramka
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.0)
    c.roundRect(28, 28, W - 56, H - 56, 14, fill=0, stroke=1)

    # Ichki ingichka ramka
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.roundRect(40, 40, W - 80, H - 80, 8, fill=0, stroke=1)

    # Burchak bezaklari
    for cx, cy, fx, fy in [
        (46, 46, 1, 1), (W - 46, 46, -1, 1),
        (46, H - 46, 1, -1), (W - 46, H - 46, -1, -1),
    ]:
        c.saveState()
        c.translate(cx, cy)
        c.scale(fx, fy)
        c.setStrokeColor(GOLD_LIGHT)
        c.setLineWidth(1.6)
        c.line(0, 0, 28, 0)
        c.line(0, 0, 0, 28)
        c.setFillColor(GOLD_LIGHT)
        c.circle(0, 0, 3, fill=1, stroke=0)
        c.setFillColor(GOLD)
        c.circle(14, 0, 1.5, fill=1, stroke=0)
        c.circle(0, 14, 1.5, fill=1, stroke=0)
        c.restoreState()

    # Yon bezak chiziqlari
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.4)
    c.setDash([3, 5])
    c.line(46, H / 2, 54, H / 2)
    c.line(W - 54, H / 2, W - 46, H / 2)
    c.setDash([])


def _draw_logo(c, W, H):
    """PyDevMap logotipi — Python ikkita doira + matn."""
    lx = W / 2 - 115
    ly = H - 65

    # Python logosi: ko'k doira
    c.setFillColor(PY_BLUE)
    c.circle(lx, ly, 10, fill=1, stroke=0)
    # Python logosi: sariq doira (biroz ustma-ust)
    c.setFillColor(PY_YELLOW)
    c.circle(lx + 14, ly, 10, fill=1, stroke=0)
    # Ustma-ust qismni yopish (NAVY2 rangida)
    c.setFillColor(NAVY2)
    c.circle(lx + 7, ly, 5, fill=1, stroke=0)

    # Platforma nomi
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(lx + 28, ly - 7, "PyDevMap")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY)
    c.setCharSpace(2)
    c.drawString(lx + 29, ly - 19, "PYTHON DASTURLASH AKADEMIYASI")
    c.setCharSpace(0)

    # Logo ostidagi chiziq
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(80, H - 82, W - 80, H - 82)


def _draw_title(c, W, H):
    """Sertifikat sarlavhasi."""
    ty = H - 118

    c.setFont("Helvetica", 8.5)
    c.setFillColor(GOLD)
    c.setCharSpace(5)
    c.drawCentredString(W / 2, ty + 28, "✦   SERTIFIKAT   ✦")
    c.setCharSpace(0)

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, ty - 4, "MUVAFFAQIYATLI TAMOMLASH")

    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawCentredString(W / 2, ty - 22,
                        "This is to certify that the following student has successfully completed the course")


def _draw_name(c, W, name, name_y):
    """Foydalanuvchi ismi bezakli ko'rinishda."""
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(GOLD_PALE)
    c.drawCentredString(W / 2, name_y, name)

    # Ism ostidagi bezak chiziqlari
    approx_w = min(len(name) * 13, 260)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(W / 2 - approx_w, name_y - 12, W / 2 + approx_w, name_y - 12)
    c.setLineWidth(0.3)
    c.line(W / 2 - approx_w - 25, name_y - 12, W / 2 - approx_w, name_y - 12)
    c.line(W / 2 + approx_w, name_y - 12, W / 2 + approx_w + 25, name_y - 12)
    # Uchburchak bezak
    c.setFillColor(GOLD)
    c.circle(W / 2 - approx_w - 25, name_y - 12, 2, fill=1, stroke=0)
    c.circle(W / 2 + approx_w + 25, name_y - 12, 2, fill=1, stroke=0)


def _draw_course(c, W, course_title, course_y):
    """Kurs nomi bloki."""
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawCentredString(W / 2, course_y + 20, "quyidagi kursni to'liq o'zlashtirdi:")

    box_w = min(len(course_title) * 11 + 80, 520)
    box_x = W / 2 - box_w / 2

    c.setFillColor(NAVY3)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(box_x, course_y - 16, box_w, 32, 8, fill=1, stroke=1)

    # Kurs nomini ikki chekkadan gold chiziq
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.5)
    c.line(box_x, course_y, box_x, course_y + 16)
    c.line(box_x + box_w, course_y, box_x + box_w, course_y + 16)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, course_y - 5, course_title)


def _draw_signature(c, sig_x, sig_y):
    """Qo'lda yozilgan imzo bezier egrilari orqali."""
    c.saveState()
    c.setStrokeColor(GOLD_PALE)
    c.setLineWidth(1.4)
    c.setLineCap(1)  # round

    # Birinchi harf "S" shakli
    p = c.beginPath()
    p.moveTo(sig_x - 58, sig_y + 8)
    p.curveTo(sig_x - 45, sig_y + 22, sig_x - 28, sig_y - 4, sig_x - 12, sig_y + 14)
    p.curveTo(sig_x + 4, sig_y + 28, sig_x + 18, sig_y + 2, sig_x + 32, sig_y + 16)
    c.drawPath(p, fill=0, stroke=1)

    # Vertikal chiziq "h"
    p2 = c.beginPath()
    p2.moveTo(sig_x - 28, sig_y + 26)
    p2.curveTo(sig_x - 22, sig_y + 4, sig_x - 10, sig_y - 10, sig_x + 5, sig_y + 10)
    c.drawPath(p2, fill=0, stroke=1)

    # Uzun pastki chiziq-flourish
    c.setLineWidth(1.0)
    p3 = c.beginPath()
    p3.moveTo(sig_x - 65, sig_y - 6)
    p3.curveTo(sig_x - 20, sig_y - 20, sig_x + 22, sig_y - 14, sig_x + 60, sig_y - 7)
    p3.curveTo(sig_x + 72, sig_y - 5, sig_x + 75, sig_y - 12, sig_x + 66, sig_y - 18)
    c.drawPath(p3, fill=0, stroke=1)

    # Nuqta bezak
    c.setFillColor(GOLD)
    c.circle(sig_x - 65, sig_y - 6, 2, fill=1, stroke=0)

    c.restoreState()


def _draw_bottom(c, W, H, user, course, cert_id):
    """Pastki qism: sana, imzo, QR kod."""
    bottom_y = 92

    # Yuqori chiziq
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(80, bottom_y + 60, W - 80, bottom_y + 60)

    # ── Chap: Sana ──────────────────────────────
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GRAY)
    c.setCharSpace(2)
    c.drawString(82, bottom_y + 46, "SANA")
    c.setCharSpace(0)

    date_str = datetime.now().strftime("%d %B %Y")
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(WHITE)
    c.drawString(82, bottom_y + 28, date_str)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(82, bottom_y + 22, 230, bottom_y + 22)

    c.setFont("Helvetica", 8)
    c.setFillColor(GRAY)
    c.drawString(82, bottom_y + 10, "Berilgan sana")

    # ── Markaz: Imzo ─────────────────────────────
    sig_x = W / 2
    _draw_signature(c, sig_x, bottom_y + 36)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(sig_x - 78, bottom_y + 22, sig_x + 78, bottom_y + 22)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GRAY)
    c.setCharSpace(1.5)
    c.drawCentredString(sig_x, bottom_y + 10, "RAHBARIYAT IMZOSI")
    c.setCharSpace(0)

    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY_DARK)
    c.drawCentredString(sig_x, bottom_y, "PyDevMap Academy  •  Bosh direktor")

    # ── O'ng: QR kod ─────────────────────────────
    qr_url = f"https://pydevmap.com/verify/{cert_id}"
    qr = qrcode.QRCode(
        version=2, box_size=4, border=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#c99a20", back_color="#12152a")

    qr_buf = io.BytesIO()
    qr_img.save(qr_buf, format='PNG')
    qr_buf.seek(0)

    qr_size = 72
    qr_x = W - 82 - qr_size
    qr_y = bottom_y - 12

    c.drawImage(ImageReader(qr_buf), qr_x, qr_y, width=qr_size, height=qr_size)

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(GRAY)
    c.setCharSpace(1)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "TEKSHIRISH")
    c.setCharSpace(0)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GOLD)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 20, cert_id)

    # ── Quyi: Sertifikat raqami ───────────────────
    c.setFont("Helvetica", 7)
    c.setFillColor(GRAY_DARK)
    c.drawCentredString(W / 2, 54,
        f"Sertifikat raqami: PDM-{cert_id}   •   PyDevMap Academy   •   pydevmap.com")

    # ── Level badge (yuqori o'ng burchak) ─────────
    level = getattr(course, 'level', 'Beginner') or 'Beginner'
    badge_hex = LEVEL_COLORS.get(level, '#22c55e')
    c.setFillColor(HexColor(badge_hex))
    c.roundRect(W - 170, H - 75, 98, 22, 5, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(WHITE)
    c.setCharSpace(1)
    c.drawCentredString(W - 121, H - 67, level.upper())
    c.setCharSpace(0)


class CertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user

        try:
            course = CourseModel.objects.get(id=course_id)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Kurs topilmadi.'}, status=404)

        # 100% tugallanganini tekshirish
        total = LessonModel.objects.filter(course=course).count()
        done  = LessonProgressModel.objects.filter(
            user=user, lesson__course=course, completed=True
        ).count()

        if total == 0 or done < total:
            return Response({
                'error': 'Kurs hali tugallanmagan.',
                'completed': done,
                'total': total,
            }, status=400)

        # ── PDF yaratish ──────────────────────────────
        buf = io.BytesIO()
        W, H = landscape(A4)   # 841.89 × 595.28 pt
        c = canvas.Canvas(buf, pagesize=(W, H))

        # 1. Fon + ramkalar
        _draw_bg(c, W, H)

        # 2. Logotip
        _draw_logo(c, W, H)

        # 3. Sarlavha
        _draw_title(c, W, H)

        # 4. Foydalanuvchi ismi
        name = user.get_full_name() or user.username
        _draw_name(c, W, name, H - 240)

        # 5. Kurs nomi
        _draw_course(c, W, course.title, H - 305)

        # 6. Sertifikat ID
        raw = f"{user.id}-{course_id}-{datetime.now().strftime('%Y%m%d')}"
        cert_id = hashlib.md5(raw.encode()).hexdigest()[:12].upper()

        # 7. Pastki qism: sana + imzo + QR
        _draw_bottom(c, W, H, user, course, cert_id)

        c.showPage()
        c.save()

        buf.seek(0)
        safe = (user.username or 'user').replace(' ', '_')
        response = HttpResponse(buf.read(), content_type='application/pdf')
        response['Content-Disposition'] = (
            f'attachment; filename="pydevmap_certificate_{safe}.pdf"'
        )
        return response
