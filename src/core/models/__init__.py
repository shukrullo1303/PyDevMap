# from src.core.models.news import News  #### shu kabi chaqriladi

from src.core.models.base import BaseModel
from src.core.models.course.category import CategoryModel
from src.core.models.course.course import CourseModel
from src.core.models.course.enrollment import EnrollmentModel
from src.core.models.lesson.lesson import LessonModel
from src.core.models.lesson.lesson_progress import LessonProgressModel
from src.core.models.quiz.quiz import QuizModel
from src.core.models.quiz.question import QuestionModel
from src.core.models.quiz.answer import AnswerModel
from src.core.models.quiz.quiz_result import QuizResultModel
from src.core.models.quiz.question import QuestionModel


# __all__ = [
#     'BaseModel',
#     'CategoryModel',         
#     'CourseModel',
#     'LessonModel',
#     'LessonProgressModel',
#     'QuizModel',
#     'QuestionModel',
#     'AnswerModel',
#     'QuizResultModel',
# ]