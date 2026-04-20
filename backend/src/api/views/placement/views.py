import os
import secrets
import string
from datetime import timedelta
from django.utils import timezone
from src.api.views.base import *
from src.core.models.placement import PlacementQuestion, PlacementSession, PlacementResponse, DiscountCoupon
from src.api.views.placement.engine import _get_next_question, _update_topic_stats, calculate_result


def _claude_analyze(session: PlacementSession, result: dict) -> str:
    """AI orqali natijani tahlil qilish va kurs tavsiyasi."""
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if not api_key:
        return _fallback_analysis(result)

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        weak  = ', '.join(result['weak_topics'])  or 'yo\'q'
        strong = ', '.join(result['strong_topics']) or 'yo\'q'

        prompt = f"""Python placement test natijasi:
- Ball: {result['percentage']:.1f}%
- Daraja: {result['level']}
- Kuchli mavzular: {strong}
- Zaif mavzular: {weak}

O'zbek tilida qisqa tahlil ber (3-5 jumlada):
1. Foydalanuvchi darajasini baholang
2. Zaif mavzularga asoslangan kurs tavsiyasi bering
3. Motivatsion so'z
Javob qisqa, aniq, do'stona bo'lsin."""

        msg = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )
        return msg.content[0].text
    except Exception:
        return _fallback_analysis(result)


def _fallback_analysis(result: dict) -> str:
    level = result['level']
    weak  = result['weak_topics']
    pct   = result['percentage']

    msgs = {
        'expert':       f"Ajoyib natija — {pct:.0f}%! Siz Python'ni juda yaxshi bilasiz.",
        'advanced':     f"Zo'r — {pct:.0f}%! Bilimlaringiz mustahkam.",
        'intermediate': f"Yaxshi — {pct:.0f}%. Ko'p narsalarni bilasiz, davom eting!",
        'beginner':     f"Boshlang'ich daraja — {pct:.0f}%. Asoslarni mustahkamlash kerak.",
    }
    base = msgs.get(level, f"{pct:.0f}% natija.")
    if weak:
        base += f" Ayniqsa {', '.join(weak)} mavzulariga e'tibor bering."
    return base


def _generate_coupon(user, session, discount: int) -> DiscountCoupon:
    existing = DiscountCoupon.objects.filter(session=session).first()
    if existing:
        return existing
    chars = string.ascii_uppercase + string.digits
    code = 'PDM-' + ''.join(secrets.choice(chars) for _ in range(8))
    return DiscountCoupon.objects.create(
        code=code,
        user=user,
        percentage=discount,
        valid_until=timezone.now() + timedelta(days=30),
        session=session,
    )


def _recommend_courses(session: PlacementSession, result: dict) -> list:
    """Zaif mavzularga mos kurslarni tavsiya qilish."""
    weak = result.get('weak_topics', [])
    level = result.get('level', 'beginner')

    from src.core.models import CourseModel
    courses = CourseModel.objects.all()

    # Daraja bo'yicha filtrlash
    level_map = {
        'beginner':     ['beginner', 'Beginner'],
        'intermediate': ['intermediate', 'Intermediate'],
        'advanced':     ['advanced', 'Advanced'],
        'expert':       ['advanced', 'Advanced'],
    }
    level_filters = level_map.get(level, ['beginner'])
    recommended = list(courses.filter(level__in=level_filters).values('id', 'title', 'price', 'is_free')[:6])
    return recommended


# ── Views ─────────────────────────────────────────────────

class StartTestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Tugallanmagan sessiyani davom ettirish
        session = PlacementSession.objects.filter(
            user=request.user, status=PlacementSession.STATUS_IN_PROGRESS
        ).first()

        if not session:
            session = PlacementSession.objects.create(user=request.user)

        asked_ids = list(session.responses.values_list('question_id', flat=True))
        question = _get_next_question(session, asked_ids)

        if not question:
            return Response({'error': 'Savol topilmadi'}, status=404)

        return Response({
            'session_id':    session.id,
            'question_num':  session.current_q_num + 1,
            'total':         session.total_questions,
            'question': {
                'id':            question.id,
                'text':          question.question_text,
                'type':          question.question_type,
                'options':       question.options,
                'code_template': question.code_template,
                'topic':         question.topic,
                'difficulty':    question.difficulty,
                'points':        question.points,
            }
        })


class AnswerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        session_id  = request.data.get('session_id')
        question_id = request.data.get('question_id')
        user_answer = request.data.get('answer', '')
        time_spent  = request.data.get('time_spent', 0)

        try:
            session  = PlacementSession.objects.get(id=session_id, user=request.user)
            question = PlacementQuestion.objects.get(id=question_id)
        except (PlacementSession.DoesNotExist, PlacementQuestion.DoesNotExist):
            return Response({'error': 'Topilmadi'}, status=404)

        if session.status != PlacementSession.STATUS_IN_PROGRESS:
            return Response({'error': 'Test allaqachon tugagan'}, status=400)

        # Javobni tekshirish
        is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()

        # Saqlash
        PlacementResponse.objects.create(
            session=session, question=question,
            user_answer=user_answer, is_correct=is_correct,
            time_spent=time_spent, question_num=session.current_q_num + 1,
        )

        # Topic stats yangilash
        _update_topic_stats(session, question, is_correct)
        session.current_q_num += 1
        session.save(update_fields=['current_q_num'])

        # Test tugadimi?
        if session.current_q_num >= session.total_questions:
            return self._finish(session, request)

        # Keyingi savol
        asked_ids = list(session.responses.values_list('question_id', flat=True))
        next_q    = _get_next_question(session, asked_ids)

        return Response({
            'is_correct':  is_correct,
            'explanation': question.explanation,
            'progress':    session.current_q_num,
            'total':       session.total_questions,
            'finished':    False,
            'next_question': {
                'id':            next_q.id,
                'text':          next_q.question_text,
                'type':          next_q.question_type,
                'options':       next_q.options,
                'code_template': next_q.code_template,
                'topic':         next_q.topic,
                'difficulty':    next_q.difficulty,
                'points':        next_q.points,
            } if next_q else None
        })

    def _finish(self, session, request):
        result = calculate_result(session)
        ai_text = _claude_analyze(session, result)
        recommended = _recommend_courses(session, result)

        session.status         = PlacementSession.STATUS_COMPLETED
        session.total_score    = result['total_score']
        session.max_score      = result['max_score']
        session.percentage     = result['percentage']
        session.result_level   = result['level']
        session.ai_analysis    = ai_text
        session.recommended_courses = [c['id'] for c in recommended]
        session.save()

        coupon = _generate_coupon(request.user, session, result['discount'])

        return Response({
            'finished': True,
            'result': {
                'percentage':    result['percentage'],
                'level':         result['level'],
                'total_score':   result['total_score'],
                'max_score':     result['max_score'],
                'strong_topics': result['strong_topics'],
                'weak_topics':   result['weak_topics'],
                'ai_analysis':   ai_text,
                'discount':      result['discount'],
                'coupon_code':   coupon.code,
                'coupon_until':  coupon.valid_until.strftime('%d.%m.%Y'),
                'recommended_courses': recommended,
            }
        })


class TestResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        session = PlacementSession.objects.filter(
            user=request.user, status=PlacementSession.STATUS_COMPLETED
        ).order_by('-created_at').first()

        if not session:
            return Response({'has_result': False})

        from src.core.models import CourseModel
        rec_courses = list(CourseModel.objects.filter(
            id__in=session.recommended_courses
        ).values('id', 'title', 'price', 'is_free', 'level'))

        coupon = DiscountCoupon.objects.filter(session=session).first()

        return Response({
            'has_result': True,
            'percentage':  session.percentage,
            'level':       session.result_level,
            'ai_analysis': session.ai_analysis,
            'topic_stats': session.topic_stats,
            'coupon': {
                'code':       coupon.code,
                'percentage': coupon.percentage,
                'valid_until': coupon.valid_until.strftime('%d.%m.%Y'),
                'is_used':    coupon.is_used,
            } if coupon else None,
            'recommended_courses': rec_courses,
        })


class ValidateCouponView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code      = request.data.get('code', '').strip().upper()
        course_id = request.data.get('course_id')

        try:
            coupon = DiscountCoupon.objects.get(code=code, user=request.user)
        except DiscountCoupon.DoesNotExist:
            return Response({'valid': False, 'error': 'Kupon topilmadi'})

        if coupon.is_used:
            return Response({'valid': False, 'error': 'Kupon allaqachon ishlatilgan'})

        if timezone.now() > coupon.valid_until:
            return Response({'valid': False, 'error': 'Kupon muddati o\'tgan'})

        try:
            from src.core.models import CourseModel
            course = CourseModel.objects.get(id=course_id)
            discounted_price = int(course.price * (1 - coupon.percentage / 100))
        except Exception:
            discounted_price = None

        return Response({
            'valid':      True,
            'percentage': coupon.percentage,
            'discounted_price': discounted_price,
            'valid_until': coupon.valid_until.strftime('%d.%m.%Y'),
        })
