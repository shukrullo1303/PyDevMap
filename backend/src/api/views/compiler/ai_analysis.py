"""
AI tahlil endpoint:
  1. Moslashuvchan natija solishtirish (flexible compare)
  2. AI yozgan / user yozgan kod aniqlash (heuristics)
  3. Natija noto'g'ri bo'lsa — tuzatish tavsiyasi (Claude API)
"""
import re
import ast
import os

from src.api.views.base import *


# ──────────────────────────────────────────────────────────
#  YORDAMCHI FUNKSIYALAR
# ──────────────────────────────────────────────────────────

def _tokenize(text: str) -> list:
    """Matnni tokenlarga ajratib, raqam/matn normalizatsiyasi."""
    text = text.strip()
    tokens = re.split(r'[\s,\[\](){}\'"]+', text)
    result = []
    for t in tokens:
        t = t.strip()
        if not t:
            continue
        try:
            result.append(str(int(t)))
            continue
        except ValueError:
            pass
        try:
            result.append(str(float(t)))
            continue
        except ValueError:
            pass
        result.append(t.lower())
    return result


def flexible_compare(expected: str, actual: str) -> bool:
    """
    Natijalarni moslashuvchan solishtirish.
    Misollar:
      '5 2 3'  ==  '5\n2\n3'    → True
      '[5,2,3]' == '5, 2, 3'    → True
      'True'   == 'true'         → True
    """
    if expected.strip() == actual.strip():
        return True

    exp_tokens = _tokenize(expected)
    act_tokens = _tokenize(actual)
    if exp_tokens == act_tokens:
        return True

    # Bool normalizatsiya
    _bool_map = {'true': 'true', 'false': 'false', '1': 'true', '0': 'false'}
    exp_norm = [_bool_map.get(t, t) for t in exp_tokens]
    act_norm = [_bool_map.get(t, t) for t in act_tokens]
    if exp_norm == act_norm:
        return True

    return False


def detect_ai_code(code: str) -> dict:
    """
    Oddiy heuristikalar orqali kod AI tomonidan yozilganini aniqlash.
    Qaytaradi: {'is_ai': bool, 'score': int (0-100), 'reasons': [...]}
    """
    score = 0
    reasons = []

    lines = [l for l in code.splitlines() if l.strip()]
    if not lines:
        return {'is_ai': False, 'score': 0, 'reasons': []}

    # 1. Har bir funksiyaga docstring
    has_docstring = '"""' in code or "'''" in code
    if has_docstring:
        score += 25
        reasons.append("Har bir funksiyada docstring bor")

    # 2. Type annotations
    has_types = bool(re.search(r'def \w+\([^)]*:\s*\w+', code)) or '->' in code
    if has_types:
        score += 20
        reasons.append("Type annotatsiyalar ishlatilgan")

    # 3. Izohlar soni nisbatan ko'p
    comment_lines = sum(1 for l in code.splitlines() if l.strip().startswith('#'))
    if comment_lines > 0 and len(lines) > 0:
        ratio = comment_lines / len(lines)
        if ratio > 0.3:
            score += 20
            reasons.append(f"Izohlar ko'p ({comment_lines} ta — {ratio:.0%} qator)")

    # 4. Juda ko'p qator — AI ko'pincha verbose bo'ladi
    if len(lines) > 20:
        score += 10
        reasons.append(f"Kod juda uzun ({len(lines)} qator)")

    # 5. if __name__ == '__main__' — AI ko'pincha qo'shadi
    if "__name__" in code:
        score += 10
        reasons.append("if __name__ == '__main__' bloki bor")

    # 6. "# Step N:" pattern — AI ko'pincha shunday izoh yozadi
    step_comments = re.findall(r'#\s*(step|part|phase|approach)\s*\d*', code, re.IGNORECASE)
    if step_comments:
        score += 15
        reasons.append("'Step/Part/Phase' izohlar topildi — AI stili")

    # 7. Juda uzun o'zgaruvchi nomlari
    long_names = re.findall(r'\b[a-z][a-z_]{12,}\b', code)
    if len(long_names) > 2:
        score += 10
        reasons.append(f"Uzun o'zgaruvchi nomlari: {long_names[:3]}")

    is_ai = score >= 40
    return {'is_ai': is_ai, 'score': min(score, 100), 'reasons': reasons}


def get_claude_suggestion(code: str, description: str, expected: str, actual: str) -> str:
    """
    Claude API yordamida kod tuzatish tavsiyasi.
    Agar ANTHROPIC_API_KEY bo'lmasa — rule-based tavsiya qaytaradi.
    """
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')

    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            prompt = (
                f"Python masalasi:\n{description}\n\n"
                f"Kutilgan natija: {expected}\n"
                f"User kod natijasi: {actual}\n\n"
                f"User kodi:\n```python\n{code}\n```\n\n"
                "Muammoni aniqlang va qanday tuzatish kerakligini o'zbek tilida qisqa tushuntiring. "
                "Javob 3-4 jumladan ko'p bo'lmasin. Kerakli bo'lsa to'g'ri kod qismini ko'rsating."
            )
            msg = client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )
            return msg.content[0].text
        except Exception as e:
            pass  # fallback below

    # Rule-based tavsiya (API yo'q bo'lsa)
    hints = []

    if expected.strip().lower() in ('true', 'false'):
        hints.append("Funksiya True/False qaytarishi kerak. return ifodasini tekshiring.")
    elif re.match(r'^\[', expected.strip()):
        hints.append("Natija list ko'rinishida bo'lishi kerak. return [] foydalaning.")
    elif re.match(r'^\{', expected.strip()):
        hints.append("Natija dict ko'rinishida bo'lishi kerak. return {} foydalaning.")
    elif actual.strip() == '':
        hints.append("Kod hech narsa chiqarmoqda. return ifodasini qo'shing — print emas, return.")
    else:
        hints.append(f"Kutilgan: '{expected.strip()}', Sizniki: '{actual.strip()}'")
        hints.append("Hisoblash mantiqini qayta tekshiring.")

    return ' '.join(hints)


# ──────────────────────────────────────────────────────────
#  API VIEW
# ──────────────────────────────────────────────────────────

@api_view(['POST'])
@permission_classes([AllowAny])
def analyze_code(request):
    """
    Body:
        user_code      - foydalanuvchi yozgan kod
        actual_output  - kodni ishlatib chiqgan natija
        task_id        - task ID (expected_output olish uchun)
    """
    user_code = request.data.get('user_code', '')
    actual_output = request.data.get('actual_output', '')
    task_id = request.data.get('task_id')

    if not user_code:
        return Response({'error': 'user_code talab qilinadi'}, status=400)

    # Task topish
    expected_output = request.data.get('expected_output', '')
    task_description = request.data.get('task_description', '')

    if task_id:
        try:
            task = TaskModel.objects.get(id=task_id)
            expected_output = task.expected_output
            task_description = task.description
        except TaskModel.DoesNotExist:
            pass

    # 1. Moslashuvchan solishtirish
    is_correct = None
    if task_id:
        try:
            task_obj = TaskModel.objects.get(id=task_id)
            if task_obj.test_code and 'unittest' in task_obj.test_code:
                # unittest stderr ga yozadi, "OK" bilan tugasa — to'g'ri
                is_correct = bool(
                    actual_output and
                    'Ran ' in actual_output and
                    actual_output.rstrip().endswith('OK')
                )
            elif expected_output:
                is_correct = flexible_compare(expected_output, actual_output)
        except TaskModel.DoesNotExist:
            pass
    elif expected_output:
        is_correct = flexible_compare(expected_output, actual_output)

    # 2. AI detection
    ai_info = detect_ai_code(user_code)

    # 3. Tavsiya (faqat noto'g'ri bo'lsa)
    suggestion = ''
    if is_correct is False and actual_output is not None:
        suggestion = get_claude_suggestion(
            user_code, task_description, expected_output, actual_output
        )

    return Response({
        'is_correct': is_correct,
        'ai_detection': {
            'is_ai_generated': ai_info['is_ai'],
            'confidence_score': ai_info['score'],
            'reasons': ai_info['reasons'],
        },
        'suggestion': suggestion,
        'expected_output': expected_output,
        'actual_output': actual_output,
    })
