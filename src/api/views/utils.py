from src.api.views.base import *



def can_user_open_lesson(user, lesson):
    course = lesson.course

    # 1️⃣ Anonymous foydalanuvchi
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        # Bepul kurs: 1-dars ochiq
        if course.price == 0 and lesson.order == 1:
            return True
        # Pullik kurs yoki keyingi darslar: yopiq
        return False

    # 2️⃣ Bepul kurslar (price=0)
    if course.price == 0:
        if lesson.order == 1:
            return True
        return _previous_completed(user, lesson)

    # 3️⃣ Pullik kurslar
    enrollment = EnrollmentModel.objects.filter(user=user, course=course).first()

    if not enrollment or not enrollment.is_paid:
        # Sotib olinmagan pullik kurs → hammasi yopiq
        return False

    # Pullik kurs, sotib olingan → 1-dars ochiq, qolganlari progress bo‘yicha
    if lesson.order == 1:
        return True

    return _previous_completed(user, lesson)


def _previous_completed(user, lesson):
    prev = LessonModel.objects.filter(
        course=lesson.course,
        order=lesson.order - 1
    ).first()

    if not prev:
        return True

    # LessonProgressModel-da field nomi `completed` ekan
    return LessonProgressModel.objects.filter(
        user=user,
        lesson=prev,
        completed=True
    ).exists()

def complete_quiz(user, quiz):
    # 1️⃣ Quiz natijasini saqlash
    result, _ = QuizResultModel.objects.get_or_create(user=user, quiz=quiz)
    result.passed = True  # yoki score>=min_score bo‘lsa
    result.save()

    # 2️⃣ Lesson progressni update qilish
    lesson = quiz.lesson
    lesson_progress, _ = LessonProgressModel.objects.get_or_create(user=user, lesson=lesson)
    lesson_progress.completed = True
    lesson_progress.save()

    # 3️⃣ Keyingi darsni unlock qilish mumkin
    next_lesson = LessonModel.objects.filter(
        course=lesson.course,
        order=lesson.order + 1
    ).first()

    if next_lesson:
        # Bu yerda keyingi darsning `locked` statusi frontendga `is_locked=False` qilib yuboriladi
        pass

# Enroll qilgandan keyin lesson unlock
def enroll_user_to_course(user, course):
    enrollment, _ = EnrollmentModel.objects.get_or_create(user=user, course=course)
    enrollment.is_paid = True
    enrollment.save()

    # Kursdagi birinchi darsni ochish
    first_lesson = LessonModel.objects.filter(course=course, order=1).first()
    if first_lesson:
        first_lesson.is_locked = False
        first_lesson.save()


from rest_framework.decorators import api_view, permission_classes
from django.db.models import Count, Q

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def course_progress(request):
    user = request.user
    enrollments = EnrollmentModel.objects.filter(user=user)
    result = []

    for enroll in enrollments:
        lessons = LessonModel.objects.filter(course=enroll.course)
        total = lessons.count()
        done = LessonProgressModel.objects.filter(user=user, lesson__in=lessons, completed=True).count()
        percent = 0 if total == 0 else round(done / total * 100)
        result.append({
            'course_id': enroll.course.id,
            'course_title': enroll.course.title,
            'progress': percent
        })

    return Response(result)
