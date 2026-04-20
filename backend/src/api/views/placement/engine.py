"""
Adaptiv test algoritmi.

Qoidalar:
1. Har topicdan kamida 2-3 ta savol beriladi
2. To'g'ri javob → bir daraja qiyin savol (shu topicdan)
3. Noto'g'ri javob → bir daraja oson savol (shu topicdan) — takrorlanmasin
4. Agar shu topicdan savol qolmasa → boshqa topicga o'tish
5. Jami 25 ta savol
"""
import random
from src.core.models.placement.question import PlacementQuestion
from src.core.models.placement.session import PlacementSession, PlacementResponse


TOTAL_QUESTIONS = 25
START_DIFFICULTY = 2  # oson boshlaydi


def _get_next_question(session: PlacementSession, exclude_ids: list) -> PlacementQuestion | None:
    """
    Session holati asosida keyingi savolni tanlaydi.
    """
    stats = session.topic_stats  # {"basics": {"correct": 2, "wrong": 1, "current_diff": 2}, ...}

    # Eng kam ko'rilgan topicni tanlash
    all_topics = [t[0] for t in PlacementQuestion.TOPIC_CHOICES]

    # Topiclarni tartibga solamiz: eng kam savol berilgani birinchi
    topic_counts = {t: stats.get(t, {}).get('asked', 0) for t in all_topics}
    # Hali ko'rilmagan topiclar bor bo'lsa — ularni ustunlik ber
    not_seen = [t for t, cnt in topic_counts.items() if cnt == 0]
    if not_seen:
        topic = random.choice(not_seen)
    else:
        # Eng past ballli topicni tanlash
        worst_topic = min(stats.keys(), key=lambda t: stats[t].get('correct', 0) / max(stats[t].get('asked', 1), 1))
        topic = worst_topic

    # Topic uchun qiyinlik darajasini aniqlash
    t_stats = stats.get(topic, {})
    current_diff = t_stats.get('current_diff', START_DIFFICULTY)
    last_correct = t_stats.get('last_correct', None)

    if last_correct is True:
        target_diff = min(current_diff + 1, 5)
    elif last_correct is False:
        target_diff = max(current_diff - 1, 1)
    else:
        target_diff = current_diff

    # Shu topic + difficulty dan savol qidirish
    qs = PlacementQuestion.objects.filter(
        topic=topic,
        difficulty=target_diff
    ).exclude(id__in=exclude_ids)

    if not qs.exists():
        # Yaqin difficulty dan qidirish
        for diff_offset in [1, -1, 2, -2]:
            alt_diff = target_diff + diff_offset
            if 1 <= alt_diff <= 5:
                qs = PlacementQuestion.objects.filter(
                    topic=topic, difficulty=alt_diff
                ).exclude(id__in=exclude_ids)
                if qs.exists():
                    break

    if not qs.exists():
        # Istalgan topicdan qidirish
        qs = PlacementQuestion.objects.exclude(id__in=exclude_ids)

    if not qs.exists():
        return None

    return random.choice(list(qs))


def _update_topic_stats(session: PlacementSession, question: PlacementQuestion, is_correct: bool):
    stats = session.topic_stats
    topic = question.topic
    if topic not in stats:
        stats[topic] = {'correct': 0, 'wrong': 0, 'asked': 0, 'current_diff': START_DIFFICULTY}

    stats[topic]['asked'] += 1
    if is_correct:
        stats[topic]['correct'] += 1
        stats[topic]['last_correct'] = True
        stats[topic]['current_diff'] = min(stats[topic].get('current_diff', START_DIFFICULTY) + 1, 5)
    else:
        stats[topic]['wrong'] += 1
        stats[topic]['last_correct'] = False
        stats[topic]['current_diff'] = max(stats[topic].get('current_diff', START_DIFFICULTY) - 1, 1)

    session.topic_stats = stats
    session.save(update_fields=['topic_stats'])


def calculate_result(session: PlacementSession) -> dict:
    """Test yakunlanganda daraja va foizni hisoblaydi."""
    responses = session.responses.all()
    total_score = sum(r.question.points for r in responses if r.is_correct)
    max_score   = sum(r.question.points for r in responses)

    percentage = (total_score / max_score * 100) if max_score else 0

    if percentage >= 85:
        level = 'expert'
        discount = 50
    elif percentage >= 65:
        level = 'advanced'
        discount = 40
    elif percentage >= 45:
        level = 'intermediate'
        discount = 30
    elif percentage >= 25:
        level = 'beginner'
        discount = 20
    else:
        level = 'beginner'
        discount = 15

    # Topic bo'yicha kuchli/zaif tomonlar
    stats = session.topic_stats
    strong  = [t for t, s in stats.items() if s.get('correct', 0) / max(s.get('asked', 1), 1) >= 0.7]
    weak    = [t for t, s in stats.items() if s.get('correct', 0) / max(s.get('asked', 1), 1) < 0.4]

    return {
        'total_score': total_score,
        'max_score':   max_score,
        'percentage':  round(percentage, 1),
        'level':       level,
        'discount':    discount,
        'strong_topics': strong,
        'weak_topics':   weak,
    }
