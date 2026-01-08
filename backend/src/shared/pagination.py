# paginations.py
from rest_framework.pagination import PageNumberPagination

class LessonPagination(PageNumberPagination):
    page_size = 1              # har sahifada nechta lesson ko‘rinadi

