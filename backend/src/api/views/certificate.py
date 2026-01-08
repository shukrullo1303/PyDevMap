from src.api.views.base import *
from reportlab.lib.utils import ImageReader
from config.settings import base
import os

class CertificateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user
        # Kurs 100% tugallanganini tekshirish
        lessons = LessonProgressModel.objects.filter(user=user, lesson__course_id=course_id)
        
        if lessons.exists() and lessons.filter(completed=False).count() == 0:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="certificate_{user.username}.pdf"'

            # Sahifa o'lchami
            w, h = 600, 400
            c = canvas.Canvas(response, pagesize=(w, h))

            # --- 1. BACKGROUND IMAGE (Eng birinchi chiziladi) ---
            # static/background.jpg (yoki .png) faylingiz bor deb hisoblaymiz
            bg_path = os.path.join(base.BASE_DIR.parent, 'src', 'static', 'background.png')
            print(bg_path)
            if os.path.exists(bg_path):
                bg_img = ImageReader(bg_path)
                c.drawImage(bg_img, 0, 0, width=w, height=h)
            
            # --- 2. DEKORATSIYA (Agar rasm ustidan ramka kerak bo'lsa) ---


            # --- 3. MATNLAR ---
            # Sarlavha
            c.setFont("Helvetica-Bold", 25)
            c.setFillColorRGB(0.1, 0.2, 0.3) # To'q rangli matn
            c.drawCentredString(300, 285, "CERTIFICATE OF COMPLETION")

            # "This is to certify that" matni
            c.setFont("Helvetica", 14)
            c.drawCentredString(300, 250, "This is to certify that")

            # User ismi
            c.setFont("Helvetica-Bold", 22)
            c.drawCentredString(300, 215, f"{user.get_full_name() or user.username}")

            # Kurs haqida ma'lumot
            c.setFont("Helvetica", 14)
            c.drawCentredString(300, 185, "has successfully completed the course")
            
            # Kurs nomi (agar CourseModel bo'lsa)
            # course_name = lessons.first().lesson.course.title
            # c.drawCentredString(300, 195, f"'{course_name}'")

            # Sana
            date_str = timezone.now().strftime("%B %d, %Y")
            c.setFont("Helvetica-Oblique", 12)
            c.drawCentredString(300, 150, f"Date: {date_str}")

            # --- 4. IMZO ---
            signature_path = os.path.join(base.BASE_DIR.parent, 'src', 'static', 'signature.png')
            if os.path.exists(signature_path):
                im = ImageReader(signature_path)
                # Imzoni markazga yoki bir chetga qo'yish
                c.drawImage(im, 250, 60, width=100, height=50, mask='auto')
                
                # Imzo ostidagi chiziq
                c.setLineWidth(1)
                c.line(240, 55, 360, 55)
                c.setFont("Helvetica", 10)
                c.drawCentredString(300, 40, "Authorized Signature")

            c.showPage()
            c.save()
            return response

        return Response({'error': 'Course not completed yet.'}, status=400)