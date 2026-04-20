import os
import json
from src.api.views.base import *


CAREER_PATHS = {
    'web':         ['HTML', 'CSS', 'JavaScript', 'Django', 'React', 'API', 'REST'],
    'data':        ['NumPy', 'Pandas', 'Matplotlib', 'SQL', 'Statistics', 'Machine Learning'],
    'ml':          ['NumPy', 'Pandas', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Deep Learning'],
    'backend':     ['Django', 'FastAPI', 'PostgreSQL', 'Redis', 'Docker', 'REST API'],
    'automation':  ['Selenium', 'BeautifulSoup', 'Scrapy', 'Requests', 'Pandas'],
    'devops':      ['Linux', 'Docker', 'Kubernetes', 'CI/CD', 'Bash', 'Python scripting'],
    'cybersecurity': ['Networking', 'Linux', 'Python', 'Cryptography', 'Ethical Hacking'],
    'mobile':      ['Kivy', 'Flutter', 'React Native', 'API integration'],
    'game':        ['Pygame', 'Unity', 'C#', 'Game Logic', 'Physics'],
    'finance':     ['NumPy', 'Pandas', 'QuantLib', 'Statistics', 'Algorithmic Trading'],
}


class AiAdvisorView(APIView):
    """
    Foydalanuvchi maqsadini aytadi → AI yo'nalish va kurslar tavsiya qiladi.
    POST /ai/advisor/
    Body: { message: str, history: [...] }
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get('message', '').strip()
        history = request.data.get('history', [])

        if not message:
            return Response({'error': 'message talab qilinadi'}, status=400)

        # Platformadagi kurslar ro'yxati
        courses = list(CourseModel.objects.values('id', 'title', 'level', 'price', 'is_free')[:30])
        course_list = '\n'.join(
            f" - {c['title']} ({c['level']}) — {'bepul' if c['is_free'] else (str(c['price']) + ' som' if c['price'] else 'narx korsatilmagan')}"
            for c in courses
        )

        api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        if not api_key:
            return self._fallback(message, courses)

        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)

            system = (
                "Sen PyDevMap platformasining AI karyera maslahatchiisan.\n"
                "Foydalanuvchi maqsadini eshitib, o'zbek tilida:\n"
                "1. Qaysi yo'nalish ekanligini aniqla\n"
                "2. O'rganish yo'l xaritasini (roadmap) ber\n"
                "3. Platformadagi mos kurslarni tavsiya qil (ID bilan)\n"
                "4. Birinchi qadamni aynan nima qilish kerakligini ko'rsat\n\n"
                "Platformadagi kurslar:\n" + course_list + "\n\n"
                "Javob formatini JSON qilib ber:\n"
                '{"reply": "matn ...", "recommended_course_ids": [1, 2, 3], "roadmap": ["qadam 1", "qadam 2"]}'
            )

            msgs = []
            for h in history[-6:]:
                if h.get('role') in ('user', 'assistant'):
                    msgs.append({'role': h['role'], 'content': h['content']})
            msgs.append({'role': 'user', 'content': message})

            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=800,
                system=system,
                messages=msgs,
            )
            text = resp.content[0].text.strip()
            if '```' in text:
                parts = text.split('```')
                text = parts[1]
                if text.startswith('json'):
                    text = text[4:]
            data = json.loads(text.strip())

            # Tavsiya qilingan kurslarni to'liq ma'lumot bilan qaytarish
            rec_ids = data.get('recommended_course_ids', [])
            rec_courses = list(CourseModel.objects.filter(id__in=rec_ids).values(
                'id', 'title', 'level', 'price', 'is_free', 'description'
            ))

            return Response({
                'reply':       data.get('reply', ''),
                'roadmap':     data.get('roadmap', []),
                'recommended_courses': rec_courses,
            })

        except Exception as e:
            return self._fallback(message, courses)

    def _fallback(self, message, courses):
        msg_lower = message.lower()
        matched_path = None
        for path, keywords in CAREER_PATHS.items():
            if any(k.lower() in msg_lower for k in keywords + [path]):
                matched_path = path
                break

        reply_map = {
            'web':    "Web dasturlash uchun Django (backend) va React (frontend) o'rganing.",
            'data':   "Data analitik uchun: Python asoslari → NumPy → Pandas → Matplotlib → SQL.",
            'ml':     "Machine Learning uchun: Python → NumPy → Pandas → Scikit-learn → TensorFlow.",
            'backend': "Backend uchun: Python → Django → REST API → PostgreSQL → Docker.",
            None:      "Maqsadingizni aniqroq aytib bering: web, data, ML, backend yoki boshqa yo'nalish.",
        }
        reply = reply_map.get(matched_path, reply_map[None])

        # Hamma kurslarni qaytarish (AI yo'q bo'lganda)
        rec = courses[:4]
        return Response({'reply': reply, 'roadmap': [], 'recommended_courses': rec})

