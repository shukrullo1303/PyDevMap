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
    """Fon va dekorativ ramka."""
    # Asosiy fon
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Ichki fon
    c.setFillColor(NAVY2)
    c.roundRect(28, 28, W - 56, H - 56, 16, fill=1, stroke=0)

    # Tashqi oltin ramka — qalin
    c.setStrokeColor(GOLD)
    c.setLineWidth(2.2)
    c.roundRect(28, 28, W - 56, H - 56, 16, fill=0, stroke=1)

    # Ichki ingichka ramka
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.roundRect(42, 42, W - 84, H - 84, 10, fill=0, stroke=1)

    # Burchak bezaklari — toza L-shakl, aylana yo'q
    c.setLineWidth(2.2)
    c.setLineCap(0)   # butt — yassi uchli
    corners = [
        (50, 50,      1,  1),
        (W - 50, 50, -1,  1),
        (50, H - 50,  1, -1),
        (W - 50, H - 50, -1, -1),
    ]
    for cx, cy, dx, dy in corners:
        c.setStrokeColor(GOLD_LIGHT)
        c.line(cx, cy, cx + dx * 24, cy)
        c.line(cx, cy, cx, cy + dy * 24)


def _draw_logo(c, W, H):
    """PyDevMap logotipi."""
    lx = W / 2 - 110
    ly = H - 62

    # Python: ko'k doira
    c.setFillColor(PY_BLUE)
    c.circle(lx, ly, 10, fill=1, stroke=0)
    # Python: sariq doira
    c.setFillColor(PY_YELLOW)
    c.circle(lx + 14, ly, 10, fill=1, stroke=0)
    # Ustma-ust qismni yopish
    c.setFillColor(NAVY2)
    c.circle(lx + 7, ly, 5, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(lx + 28, ly - 7, "PyDevMap")

    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY)
    c._charSpace = 2
    c.drawString(lx + 29, ly - 19, "PYTHON DASTURLASH AKADEMIYASI")
    c._charSpace = 0

    # Logo ostidagi chiziq
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(80, H - 84, W - 80, H - 84)


def _draw_title(c, W, H):
    """Sertifikat sarlavhasi — sal pastroqqa tushirilgan."""
    ty = H - 132

    c.setFont("Helvetica", 8.5)
    c.setFillColor(GOLD)
    c._charSpace = 5
    c.drawCentredString(W / 2, ty + 28, "\u2736   SERTIFIKAT   \u2736")
    c._charSpace = 0

    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(WHITE)
    c.drawCentredString(W / 2, ty - 4, "MUVAFFAQIYATLI TAMOMLASH")

    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawCentredString(
        W / 2, ty - 22,
        "Ushbu sertifikat quyidagi talabaning kursni muvaffaqiyatli yakunlaganligini tasdiqlaydi"
    )


def _draw_name(c, W, name, name_y):
    """Foydalanuvchi ismi bezakli ko'rinishda."""
    c.setFont("Helvetica-Bold", 30)
    c.setFillColor(GOLD_PALE)
    c.drawCentredString(W / 2, name_y, name)

    approx_w = min(len(name) * 12, 260)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(W / 2 - approx_w, name_y - 12, W / 2 + approx_w, name_y - 12)
    # Kengaytiruvchi ingichka chiziqlar
    c.setLineWidth(0.4)
    c.line(W / 2 - approx_w - 30, name_y - 12, W / 2 - approx_w, name_y - 12)
    c.line(W / 2 + approx_w, name_y - 12, W / 2 + approx_w + 30, name_y - 12)
    # Doira bezak
    c.setFillColor(GOLD)
    c.circle(W / 2 - approx_w - 30, name_y - 12, 2, fill=1, stroke=0)
    c.circle(W / 2 + approx_w + 30, name_y - 12, 2, fill=1, stroke=0)


def _draw_course(c, W, course_title, course_y):
    """Kurs nomi bloki."""
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawCentredString(W / 2, course_y + 22, "quyidagi kursni to'liq o'zlashtirdi:")

    box_w = min(len(course_title) * 11 + 80, 520)
    box_x = W / 2 - box_w / 2

    c.setFillColor(NAVY3)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.roundRect(box_x, course_y - 16, box_w, 32, 8, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(GOLD_LIGHT)
    c.drawCentredString(W / 2, course_y - 5, course_title)


def _draw_signature(c, sig_x, sig_y):
    """Bezier imzo."""
    c.saveState()
    c.setStrokeColor(GOLD_PALE)
    c.setLineWidth(1.4)
    c.setLineCap(1)

    p = c.beginPath()
    p.moveTo(sig_x - 58, sig_y + 8)
    p.curveTo(sig_x - 45, sig_y + 22, sig_x - 28, sig_y - 4, sig_x - 12, sig_y + 14)
    p.curveTo(sig_x + 4, sig_y + 28, sig_x + 18, sig_y + 2, sig_x + 32, sig_y + 16)
    c.drawPath(p, fill=0, stroke=1)

    p2 = c.beginPath()
    p2.moveTo(sig_x - 28, sig_y + 26)
    p2.curveTo(sig_x - 22, sig_y + 4, sig_x - 10, sig_y - 10, sig_x + 5, sig_y + 10)
    c.drawPath(p2, fill=0, stroke=1)

    c.setLineWidth(1.0)
    p3 = c.beginPath()
    p3.moveTo(sig_x - 65, sig_y - 6)
    p3.curveTo(sig_x - 20, sig_y - 20, sig_x + 22, sig_y - 14, sig_x + 60, sig_y - 7)
    p3.curveTo(sig_x + 72, sig_y - 5, sig_x + 75, sig_y - 12, sig_x + 66, sig_y - 18)
    c.drawPath(p3, fill=0, stroke=1)

    c.setFillColor(GOLD)
    c.circle(sig_x - 65, sig_y - 6, 2, fill=1, stroke=0)
    c.restoreState()


def _draw_bottom(c, W, H, user, course, cert_id):
    """Pastki qism: sana, imzo, QR kod."""
    bottom_y = 92

    # Ajratuvchi chiziq
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(80, bottom_y + 60, W - 80, bottom_y + 60)

    # ── Chap: Sana ──────────────────────────────────
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GRAY)
    c._charSpace = 2
    c.drawString(82, bottom_y + 46, "SANA")
    c._charSpace = 0

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

    # ── Markaz: Imzo ────────────────────────────────
    sig_x = W / 2
    _draw_signature(c, sig_x, bottom_y + 36)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.8)
    c.line(sig_x - 78, bottom_y + 22, sig_x + 78, bottom_y + 22)

    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(GRAY)
    c._charSpace = 1.5
    c.drawCentredString(sig_x, bottom_y + 10, "RAHBARIYAT IMZOSI")
    c._charSpace = 0

    c.setFont("Helvetica", 7.5)
    c.setFillColor(GRAY_DARK)
    c.drawCentredString(sig_x, bottom_y, "PyDevMap Academy  \u2022  Bosh direktor")

    # ── O'ng: QR kod ─────────────────────────────────
    qr_url = "https://pydevmap.uz/verify/" + cert_id
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
    c._charSpace = 1
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 10, "TEKSHIRISH")
    c._charSpace = 0

    # cert_id already contains PDM- prefix — show as-is
    c.setFont("Helvetica-Bold", 7.5)
    c.setFillColor(GOLD)
    c.drawCentredString(qr_x + qr_size / 2, qr_y - 21, cert_id)

    # ── Quyi manzil satri ────────────────────────────
    c.setFont("Helvetica", 7)
    c.setFillColor(GRAY_DARK)
    c.drawCentredString(
        W / 2, 54,
        "Sertifikat raqami: " + cert_id + "   \u2022   PyDevMap Academy   \u2022   pydevmap.uz"
    )

    # ── Level badge (yuqori o'ng burchak) ─────────────
    level = getattr(course, 'level', 'Beginner') or 'Beginner'
    badge_hex = LEVEL_COLORS.get(level, '#22c55e')
    c.setFillColor(HexColor(badge_hex))
    c.roundRect(W - 170, H - 75, 98, 22, 5, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 8.5)
    c.setFillColor(WHITE)
    c._charSpace = 1
    c.drawCentredString(W - 121, H - 67, level.upper())
    c._charSpace = 0


class CertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user

        try:
            course = CourseModel.objects.get(id=course_id)
        except CourseModel.DoesNotExist:
            return Response({'error': 'Kurs topilmadi.'}, status=404)

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

        _draw_bg(c, W, H)
        _draw_logo(c, W, H)
        _draw_title(c, W, H)

        # Ism familiya (to'liq ism yo'q bo'lsa username)
        name = user.get_full_name() or user.username
        _draw_name(c, W, name, H - 262)

        _draw_course(c, W, course.title, H - 330)

        # Sertifikat ID — PDM- prefiksi bilan, QR va pastki matn mos keladi
        raw = str(user.id) + "-" + str(course_id) + "-" + datetime.now().strftime('%Y%m%d')
        cert_id = "PDM-" + hashlib.md5(raw.encode()).hexdigest()[:10].upper()

        _draw_bottom(c, W, H, user, course, cert_id)

        c.showPage()
        c.save()

        # Sertifikat olgandan keyin ism-familiyani bloklash
        from src.core.models.user_profile import UserProfile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        if not profile.name_locked:
            profile.name_locked = True
            profile.save(update_fields=['name_locked'])

        buf.seek(0)
        safe_name = (user.get_full_name() or user.username).replace(' ', '_')
        response = HttpResponse(buf.read(), content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="pydevmap_certificate_' + safe_name + '.pdf"'
        )
        return response
