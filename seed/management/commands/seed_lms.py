from django.core.management.base import BaseCommand
from faker import Faker
import random
import uuid 


from src.core.models import *

fake = Faker()
class Command(BaseCommand):
    help = "Seed LMS with courses, lessons, quizzes, questions, answers"

    NUM_CATEGORIES = 5
    NUM_COURSES = 10
    LESSONS_PER_COURSE = 10
    QUIZ_LESSON_POSITIONS = [3, 7]  # qaysi lessonlar quiz bo‘ladi
    QUESTIONS_PER_QUIZ = 5
    ANSWERS_PER_QUESTION = 4

    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        AnswerModel.objects.all().delete()
        QuestionModel.objects.all().delete()
        QuizModel.objects.all().delete()
        LessonModel.objects.all().delete()
        CourseModel.objects.all().delete()
        CategoryModel.objects.all().delete()

        self.stdout.write("Creating categories...")
        categories = []
        for _ in range(self.NUM_CATEGORIES):
            cat = CategoryModel.objects.create(
                name=fake.word().title(),
                slug=f"{fake.word()}-{uuid.uuid4().hex[:6]}"
            )
            categories.append(cat)

        self.stdout.write("Creating courses with lessons, quizzes, and answers...")
        for _ in range(self.NUM_COURSES):
            course = CourseModel.objects.create(
                category=random.choice(categories),
                title=fake.sentence(nb_words=6),
                description=fake.text(max_nb_chars=200),
                price=random.randint(0, 300000),
            )

            for i in range(1, self.LESSONS_PER_COURSE + 1):
                lesson_title = fake.sentence(nb_words=6)
                lesson_slug = f"{uuid.uuid4().hex[:8]}-{i}"
                lesson = LessonModel.objects.create(
                    course=course,
                    title=lesson_title,
                    slug=lesson_slug,
                    order=i,
                )

                if i in self.QUIZ_LESSON_POSITIONS:
                    quiz = QuizModel.objects.create(
                        lesson=lesson,
                    )
                    for _ in range(self.QUESTIONS_PER_QUIZ):
                        question_text = fake.sentence(nb_words=8)
                        question = QuestionModel.objects.create(
                            quiz=quiz,
                            text=question_text
                        )
                        correct_index = random.randint(0, self.ANSWERS_PER_QUESTION - 1)
                        for a in range(self.ANSWERS_PER_QUESTION):
                            AnswerModel.objects.create(
                                question=question,
                                text=fake.word(),
                                is_correct=(a == correct_index)
                            )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))
