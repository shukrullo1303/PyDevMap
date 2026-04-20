from src.core.models.base import *


class PlacementQuestion(BaseModel):
    TYPE_MCQ  = 'mcq'    # Ko'p tanlovli
    TYPE_CODE = 'code'   # Kod yozish

    TOPIC_BASICS      = 'basics'       # O'zgaruvchilar, operatorlar
    TOPIC_STRINGS     = 'strings'      # Satrlar
    TOPIC_LISTS       = 'lists'        # Ro'yxatlar
    TOPIC_DICTS       = 'dicts'        # Lug'atlar
    TOPIC_FUNCTIONS   = 'functions'    # Funksiyalar
    TOPIC_OOP         = 'oop'          # OOP
    TOPIC_EXCEPTIONS  = 'exceptions'   # Xatolar
    TOPIC_FILES       = 'files'        # Fayllar
    TOPIC_MODULES     = 'modules'      # Modullar
    TOPIC_ALGORITHMS  = 'algorithms'   # Algoritmlar

    TOPIC_CHOICES = [
        (TOPIC_BASICS,     'Asoslar'),
        (TOPIC_STRINGS,    'Satrlar'),
        (TOPIC_LISTS,      'Ro\'yxatlar'),
        (TOPIC_DICTS,      'Lug\'atlar'),
        (TOPIC_FUNCTIONS,  'Funksiyalar'),
        (TOPIC_OOP,        'OOP'),
        (TOPIC_EXCEPTIONS, 'Xatolar'),
        (TOPIC_FILES,      'Fayllar'),
        (TOPIC_MODULES,    'Modullar'),
        (TOPIC_ALGORITHMS, 'Algoritmlar'),
    ]

    question_text = models.TextField()
    question_type = models.CharField(max_length=10, choices=[
        (TYPE_MCQ, 'Ko\'p tanlovli'),
        (TYPE_CODE, 'Kod yozish'),
    ], default=TYPE_MCQ)

    # MCQ uchun variantlar (JSON: ["A", "B", "C", "D"])
    options = models.JSONField(default=list, blank=True)
    correct_answer = models.TextField()

    # Kod masala uchun
    code_template  = models.TextField(blank=True, default='')  # boshlang'ich kod
    expected_output = models.TextField(blank=True, default='')
    test_cases     = models.JSONField(default=list, blank=True)  # [{"input": ..., "output": ...}]

    topic      = models.CharField(max_length=30, choices=TOPIC_CHOICES, default=TOPIC_BASICS)
    difficulty = models.IntegerField(default=2)  # 1=juda oson, 2=oson, 3=o'rta, 4=qiyin, 5=expert
    points     = models.IntegerField(default=10)
    explanation = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['topic', 'difficulty']

    def __str__(self):
        return f"[{self.topic}|d{self.difficulty}] {self.question_text[:60]}"
