from django.core.management.base import BaseCommand
from django.utils.text import slugify
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
    QUESTIONS_PER_QUIZ = 5
    ANSWERS_PER_QUESTION = 4

    def _generate_random_task_data(self, lesson):
        """Generate a simple random compiler task for a given lesson."""
        # Oddiy, tushunarli masalalar shablonlari
        templates = []

        # 1) Hello World
        templates.append({
            "title": f"Hello World – Lesson {lesson.order}",
            "description": (
                "Python funksiyasi yozing: solve(), u hech narsa chop etmasin, "
                "faqat 'Hello, World!' stringini qaytarsin."
            ),
            "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_solve(self):
        from __main__ import solve
        assert callable(solve)
        self.assertEqual(solve(), "Hello, World!")

if __name__ == "__main__":
    unittest.main()
""",
        })

        # 2) Ikki sonni yig'indisi
        templates.append({
            "title": f"Sum of Two Numbers – Lesson {lesson.order}",
            "description": (
                "solve(a, b) funksiyasini yozing, u berilgan ikkita butun sonning yig'indisini "
                "qaytarsin. print ishlatish shart emas, faqat qiymatni return qiling."
            ),
            "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_small_numbers(self):
        from __main__ import solve
        self.assertEqual(solve(1, 2), 3)

    def test_negative(self):
        from __main__ import solve
        self.assertEqual(solve(-5, 5), 0)

if __name__ == "__main__":
    unittest.main()
""",
        })

        # 3) Ro'yxatdagi eng katta son
        templates.append({
            "title": f"Max in List – Lesson {lesson.order}",
            "description": (
                "solve(numbers) funksiyasini yozing, numbers ro'yxatidagi eng katta sonni "
                "qaytarsin. len(numbers) kamida bitta elementdan iborat bo'ladi."
            ),
            "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_simple(self):
        from __main__ import solve
        self.assertEqual(solve([1, 2, 3]), 3)

    def test_mixed(self):
        from __main__ import solve
        self.assertEqual(solve([-10, 0, 10]), 10)

if __name__ == "__main__":
    unittest.main()
""",
        })

        return random.choice(templates)

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
            name = fake.word().title()
            raw_slug = f"{fake.word()}-{uuid.uuid4().hex[:6]}"
            cat = CategoryModel.objects.create(
                name=name,
                slug=raw_slug[:50],  # SlugField default max_length is 50
            )
            categories.append(cat)

        self.stdout.write("Creating courses with lessons, quizzes, and answers...")
        for _ in range(self.NUM_COURSES):
            title = fake.sentence(nb_words=6)
            base_slug = slugify(title)
            # Reserve space for -uuid suffix to keep total length <= 50
            safe_base = base_slug[:40]
            course_slug = f"{safe_base}-{uuid.uuid4().hex[:6]}"[:50]
            course = CourseModel.objects.create(
                category=random.choice(categories),
                title=title,
                slug=course_slug,
                description=fake.text(max_nb_chars=200),
                price=random.randint(0, 300000),
            )

            for i in range(1, self.LESSONS_PER_COURSE + 1):
                lesson_title = fake.sentence(nb_words=6)
                lesson_slug = f"{uuid.uuid4().hex[:8]}-{i}"[:50]
                lesson = LessonModel.objects.create(
                    course=course,
                    title=lesson_title,
                    slug=lesson_slug,
                    order=i,
                )

                # Har bir darsga random tarzda: quiz YOKI task
                if random.choice(["quiz", "task"]) == "quiz":
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
                else:
                    task_data = self._generate_random_task_data(lesson)
                    TaskModel.objects.create(
                        title=task_data["title"],
                        description=task_data["description"],
                        test_code=task_data["test_code"],
                    )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully!"))

