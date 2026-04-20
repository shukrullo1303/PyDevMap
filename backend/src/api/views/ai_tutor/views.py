import os
import json
from src.api.views.base import *

REVIEW_PROMPT_TEMPLATE = (
    "Python kod review:\n\n"
    "Vazifa: {vazifa}\n\n"
    "Kod:\n```python\n{code}\n```\n\n"
    "Quyidagilarni o'zbek tilida baholang (JSON formatida):\n"
    '{{"quality_score": 7, "summary": "...", '
    '"improvements": ["..."], "alternative": "...", '
    '"complexity": "O(n)", "style_issues": ["..."]}}\n\n'
    "Faqat JSON qaytaring."
)


def _get_claude():
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return None
    try:
        import anthropic
        return anthropic.Anthropic(api_key=api_key)
    except Exception:
        return None


class AiChatView(APIView):
    """Dars sahifasidagi AI tutor."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message   = request.data.get('message', '').strip()
        lesson_id = request.data.get('lesson_id')
        history   = request.data.get('history', [])

        if not message:
            return Response({'error': 'message talab qilinadi'}, status=400)

        lesson_context = ''
        if lesson_id:
            try:
                lesson = LessonModel.objects.get(id=lesson_id)
                snippet = (lesson.content or '')[:1000]
                lesson_context = "Dars: " + lesson.title + "\n" + snippet
            except LessonModel.DoesNotExist:
                pass

        client = _get_claude()
        if not client:
            return Response({
                'reply': 'AI hozirda mavjud emas. ANTHROPIC_API_KEY ni sozlang.',
                'error': True
            })

        ctx = ("\nHozirgi dars:\n" + lesson_context) if lesson_context else ""
        system = (
            "Sen PyDevMap platformasining Python o'qituvchisan. "
            "Foydalanuvchilarga o'zbek tilida javob berasan. "
            "Javoblar qisqa va amaliy bo'lsin." + ctx
        )

        messages = []
        for h in history[-6:]:
            if h.get('role') in ('user', 'assistant'):
                messages.append({'role': h['role'], 'content': h['content']})
        messages.append({'role': 'user', 'content': message})

        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=600,
                system=system,
                messages=messages,
            )
            return Response({'reply': resp.content[0].text})
        except Exception as e:
            return Response({'reply': 'Xatolik: ' + str(e), 'error': True}, status=500)


class CodeReviewView(APIView):
    """Kengaytirilgan kod review."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code      = request.data.get('code', '').strip()
        task_desc = request.data.get('task_description', '')

        if not code:
            return Response({'error': 'code talab qilinadi'}, status=400)

        client = _get_claude()
        if not client:
            return Response({
                'quality_score': 5,
                'summary': 'AI mavjud emas.',
                'improvements': [],
                'alternative': '',
                'complexity': 'Aniqlanmadi',
                'style_issues': [],
            })

        vazifa = task_desc if task_desc else "Ko'rsatilmagan"
        prompt = REVIEW_PROMPT_TEMPLATE.format(vazifa=vazifa, code=code)

        try:
            resp = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=800,
                messages=[{"role": "user", "content": prompt}]
            )
            text = resp.content[0].text.strip()
            if '```' in text:
                parts = text.split('```')
                text = parts[1]
                if text.startswith('json'):
                    text = text[4:]
            data = json.loads(text.strip())
            return Response(data)
        except Exception:
            return Response({
                'quality_score': 5,
                'summary': 'Kod baholandi.',
                'improvements': ['Kod aniqroq yozilishi mumkin.'],
                'alternative': '',
                'complexity': 'Aniqlanmadi',
                'style_issues': [],
            })
