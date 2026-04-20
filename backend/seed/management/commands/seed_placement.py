"""
python manage.py seed_placement

200+ ta placement test savoli va masalalarini yaratadi.
Adaptiv algoritm uchun har bir topic + difficulty kombinatsiyasida
kamida 4-5 ta savol bo'ladi.
"""
from django.core.management.base import BaseCommand
from src.core.models.placement.question import PlacementQuestion

Q = PlacementQuestion  # shortcut

QUESTIONS = [

    # ══════════════════════════════════════════════════════
    #  BASICS — O'zgaruvchilar, operatorlar, tiplar
    # ══════════════════════════════════════════════════════

    # difficulty=1 (juda oson)
    dict(topic='basics', difficulty=1, question_type='mcq', points=5,
         question_text="Python'da o'zgaruvchi qanday e'lon qilinadi?",
         options=["var x = 5", "x = 5", "int x = 5", "let x = 5"],
         correct_answer="x = 5",
         explanation="Python'da o'zgaruvchiga shunchaki = bilan qiymat beriladi."),

    dict(topic='basics', difficulty=1, question_type='mcq', points=5,
         question_text="Quyidagilardan qaysi biri Python'da to'g'ri izoh (comment)?",
         options=["// Bu izoh", "/* Bu izoh */", "# Bu izoh", "<!-- Bu izoh -->"],
         correct_answer="# Bu izoh",
         explanation="Python'da izohlar # belgisi bilan boshlanadi."),

    dict(topic='basics', difficulty=1, question_type='mcq', points=5,
         question_text="print(type(5)) natijasi nima?",
         options=["int", "<class 'int'>", "Integer", "number"],
         correct_answer="<class 'int'>",
         explanation="type() funksiyasi <class 'tur'> formatida qaytaradi."),

    dict(topic='basics', difficulty=1, question_type='mcq', points=5,
         question_text="x = 10; y = 3; print(x // y) natijasi?",
         options=["3.33", "3", "4", "0"],
         correct_answer="3",
         explanation="// operatori butun bo'linma (floor division) beradi."),

    dict(topic='basics', difficulty=1, question_type='mcq', points=5,
         question_text="Python'da mantiqiy (boolean) qiymatlar qaysilar?",
         options=["yes/no", "1/0", "True/False", "on/off"],
         correct_answer="True/False",
         explanation="Python'da True va False (katta harf bilan) boolean qiymatlar."),

    # difficulty=2
    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="x = 5; x += 3; print(x) natijasi?",
         options=["5", "3", "8", "53"],
         correct_answer="8",
         explanation="x += 3 bu x = x + 3 degan ma'noni anglatadi."),

    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="print(10 % 3) natijasi nima?",
         options=["3", "1", "0", "3.33"],
         correct_answer="1",
         explanation="% operatori qoldiqni beradi: 10 = 3*3 + 1"),

    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="bool('') natijasi nima?",
         options=["True", "False", "None", "Error"],
         correct_answer="False",
         explanation="Bo'sh satr, 0, None, [] kabilar False hisoblansa."),

    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="x = 2; print(x ** 3) natijasi?",
         options=["6", "8", "9", "23"],
         correct_answer="8",
         explanation="** operatori daraja hisoblaydi: 2^3 = 8."),

    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="int('42') + float('3.5') natijasi?",
         options=["4235", "45", "45.5", "Error"],
         correct_answer="45.5",
         explanation="int('42')=42, float('3.5')=3.5, yig'indisi 45.5."),

    # difficulty=3
    dict(topic='basics', difficulty=3, question_type='mcq', points=15,
         question_text="a = b = c = 5; a = 10; print(b) natijasi?",
         options=["10", "5", "15", "Error"],
         correct_answer="5",
         explanation="int muhiti — a = 10 qilganda b o'zgarmaydi."),

    dict(topic='basics', difficulty=3, question_type='mcq', points=15,
         question_text="print(0.1 + 0.2 == 0.3) natijasi?",
         options=["True", "False", "None", "Error"],
         correct_answer="False",
         explanation="Float matematik xatolari: 0.1+0.2 = 0.30000000000000004."),

    dict(topic='basics', difficulty=3, question_type='mcq', points=15,
         question_text="x = None; print(x is None) natijasi?",
         options=["True", "False", "Error", "None"],
         correct_answer="True",
         explanation="None tekshirishda 'is' operatori ishlatiladi."),

    # ══════════════════════════════════════════════════════
    #  STRINGS
    # ══════════════════════════════════════════════════════

    dict(topic='strings', difficulty=1, question_type='mcq', points=5,
         question_text="s = 'Python'; print(len(s)) natijasi?",
         options=["5", "6", "7", "Error"],
         correct_answer="6",
         explanation="'Python' satri 6 ta belgidan iborat."),

    dict(topic='strings', difficulty=1, question_type='mcq', points=5,
         question_text="s = 'hello'; print(s[0]) natijasi?",
         options=["h", "e", "hello", "Error"],
         correct_answer="h",
         explanation="Indeks 0 dan boshlanadi."),

    dict(topic='strings', difficulty=1, question_type='mcq', points=5,
         question_text="'Python' + ' ' + 'rocks' natijasi?",
         options=["PythonRocks", "Python rocks", "Error", "Python + rocks"],
         correct_answer="Python rocks",
         explanation="Satrlarni + bilan birlashtirish concatenation."),

    dict(topic='strings', difficulty=2, question_type='mcq', points=10,
         question_text="s = 'Hello World'; print(s.lower()) natijasi?",
         options=["HELLO WORLD", "hello world", "Hello world", "Error"],
         correct_answer="hello world",
         explanation=".lower() barcha harflarni kichiklashtiradi."),

    dict(topic='strings', difficulty=2, question_type='mcq', points=10,
         question_text="s = 'Python'; print(s[-1]) natijasi?",
         options=["P", "n", "y", "Error"],
         correct_answer="n",
         explanation="Manfiy indeks: -1 oxirgi belgiga ishora qiladi."),

    dict(topic='strings', difficulty=2, question_type='mcq', points=10,
         question_text="'hello'.replace('l', 'r') natijasi?",
         options=["herro", "hero", "hello", "Error"],
         correct_answer="herro",
         explanation=".replace() barcha uchrashuvlarni almashtiradi."),

    dict(topic='strings', difficulty=2, question_type='mcq', points=10,
         question_text="s = '  hello  '; print(s.strip()) natijasi?",
         options=["'  hello  '", "'hello'", "hello", "Error"],
         correct_answer="hello",
         explanation=".strip() boshidagi va oxiridagi bo'shliqlarni olib tashlaydi."),

    dict(topic='strings', difficulty=3, question_type='mcq', points=15,
         question_text="s = 'Python'; print(s[1:4]) natijasi?",
         options=["Pyt", "yth", "ytho", "Error"],
         correct_answer="yth",
         explanation="Slicing: [1:4] — 1,2,3 indekslari (4 kiritilmaydi)."),

    dict(topic='strings', difficulty=3, question_type='mcq', points=15,
         question_text="name = 'Ali'; age = 20; print(f'{name} is {age}') natijasi?",
         options=["name is age", "Ali is 20", "{name} is {age}", "Error"],
         correct_answer="Ali is 20",
         explanation="f-string interpolatsiya."),

    dict(topic='strings', difficulty=3, question_type='mcq', points=15,
         question_text="'banana'.count('a') natijasi?",
         options=["1", "2", "3", "4"],
         correct_answer="3",
         explanation="'banana' da 'a' 3 marta uchraydi."),

    dict(topic='strings', difficulty=4, question_type='mcq', points=20,
         question_text="s = 'hello'; print(s[::-1]) natijasi?",
         options=["hello", "olleh", "Error", "h"],
         correct_answer="olleh",
         explanation="[::-1] satrni teskari aylantiradi."),

    dict(topic='strings', difficulty=4, question_type='mcq', points=20,
         question_text="', '.join(['a', 'b', 'c']) natijasi?",
         options=["a,b,c", "a, b, c", "abc", "['a','b','c']"],
         correct_answer="a, b, c",
         explanation=".join() ro'yxat elementlarini belgi bilan birlashtiradi."),

    # CODE savollari
    dict(topic='strings', difficulty=3, question_type='code', points=20,
         question_text="Berilgan satrning birinchi va oxirgi belgisini birlashtiring.\nMasalan: 'hello' → 'ho'",
         code_template="def first_last(s):\n    # kod yozing\n    pass",
         correct_answer="def first_last(s):\n    return s[0] + s[-1]",
         expected_output="ho",
         test_cases=[{"input": "hello", "output": "ho"}, {"input": "python", "output": "pn"}],
         explanation="s[0] birinchi, s[-1] oxirgi belgi."),

    dict(topic='strings', difficulty=4, question_type='code', points=25,
         question_text="Satrni so'zlarga ajrating va har bir so'zni katta harf bilan boshlang.\nMasalan: 'hello world' → 'Hello World'",
         code_template="def title_case(s):\n    pass",
         correct_answer="def title_case(s):\n    return s.title()",
         expected_output="Hello World",
         test_cases=[{"input": "hello world", "output": "Hello World"}],
         explanation=".title() har so'zning birinchi harfini kattalashtiradi."),

    # ══════════════════════════════════════════════════════
    #  LISTS
    # ══════════════════════════════════════════════════════

    dict(topic='lists', difficulty=1, question_type='mcq', points=5,
         question_text="lst = [1, 2, 3]; print(lst[1]) natijasi?",
         options=["1", "2", "3", "Error"],
         correct_answer="2",
         explanation="Indeks 0 dan boshlanadi, 1-indeks 2-element."),

    dict(topic='lists', difficulty=1, question_type='mcq', points=5,
         question_text="lst = []; lst.append(5); print(lst) natijasi?",
         options=["[]", "[5]", "5", "Error"],
         correct_answer="[5]",
         explanation=".append() ro'yxat oxiriga element qo'shadi."),

    dict(topic='lists', difficulty=1, question_type='mcq', points=5,
         question_text="lst = [1,2,3,4,5]; print(len(lst)) natijasi?",
         options=["4", "5", "6", "Error"],
         correct_answer="5",
         explanation="len() elementlar sonini qaytaradi."),

    dict(topic='lists', difficulty=2, question_type='mcq', points=10,
         question_text="lst = [3,1,2]; lst.sort(); print(lst) natijasi?",
         options=["[3,1,2]", "[1,2,3]", "[3,2,1]", "Error"],
         correct_answer="[1,2,3]",
         explanation=".sort() ro'yxatni o'sish tartibida saralaydi."),

    dict(topic='lists', difficulty=2, question_type='mcq', points=10,
         question_text="lst = [1,2,3]; print(lst[-1]) natijasi?",
         options=["1", "2", "3", "Error"],
         correct_answer="3",
         explanation="Manfiy indeks: -1 oxirgi elementga ishora qiladi."),

    dict(topic='lists', difficulty=2, question_type='mcq', points=10,
         question_text="lst = [1,2,3]; lst.pop(); print(lst) natijasi?",
         options=["[1,2]", "[2,3]", "[1,2,3]", "Error"],
         correct_answer="[1,2]",
         explanation=".pop() oxirgi elementni olib tashlaydi."),

    dict(topic='lists', difficulty=2, question_type='mcq', points=10,
         question_text="lst = [1,2,3]; print(sum(lst)) natijasi?",
         options=["6", "123", "3", "Error"],
         correct_answer="6",
         explanation="sum() ro'yxat elementlarini yig'adi."),

    dict(topic='lists', difficulty=3, question_type='mcq', points=15,
         question_text="lst = [1,2,3,4,5]; print(lst[1:3]) natijasi?",
         options=["[1,2]", "[2,3]", "[2,3,4]", "Error"],
         correct_answer="[2,3]",
         explanation="Slicing: [1:3] — 1 va 2 indekslar (3 kiritilmaydi)."),

    dict(topic='lists', difficulty=3, question_type='mcq', points=15,
         question_text="a = [1,2]; b = a; b.append(3); print(a) natijasi?",
         options=["[1,2]", "[1,2,3]", "[3]", "Error"],
         correct_answer="[1,2,3]",
         explanation="b = a — bu yangi nusxa emas, bir xil ob'ektga ishora."),

    dict(topic='lists', difficulty=3, question_type='mcq', points=15,
         question_text="[x**2 for x in range(4)] natijasi?",
         options=["[0,1,2,3]", "[1,4,9,16]", "[0,1,4,9]", "Error"],
         correct_answer="[0,1,4,9]",
         explanation="List comprehension: 0^2=0, 1^2=1, 2^2=4, 3^2=9."),

    dict(topic='lists', difficulty=4, question_type='mcq', points=20,
         question_text="lst = [1,[2,3],[4,[5,6]]]; print(lst[2][1][0]) natijasi?",
         options=["4", "5", "6", "Error"],
         correct_answer="5",
         explanation="lst[2]=[4,[5,6]], [2][1]=[5,6], [2][1][0]=5."),

    dict(topic='lists', difficulty=4, question_type='mcq', points=20,
         question_text="sorted([3,1,2], reverse=True) natijasi?",
         options=["[1,2,3]", "[3,2,1]", "[3,1,2]", "Error"],
         correct_answer="[3,2,1]",
         explanation="sorted() yangi ro'yxat qaytaradi, reverse=True kamayish tartibida."),

    # CODE
    dict(topic='lists', difficulty=3, question_type='code', points=20,
         question_text="Ro'yxatdagi juft sonlarni qaytaring.\nMasalan: [1,2,3,4,5,6] → [2,4,6]",
         code_template="def even_numbers(lst):\n    pass",
         correct_answer="def even_numbers(lst):\n    return [x for x in lst if x % 2 == 0]",
         expected_output="[2, 4, 6]",
         test_cases=[{"input": "[1,2,3,4,5,6]", "output": "[2, 4, 6]"}]),

    dict(topic='lists', difficulty=4, question_type='code', points=25,
         question_text="Ro'yxatdagi takrorlanadigan elementlarni olib tashlang.\nMasalan: [1,2,2,3,3,4] → [1,2,3,4]",
         code_template="def remove_duplicates(lst):\n    pass",
         correct_answer="def remove_duplicates(lst):\n    return list(dict.fromkeys(lst))",
         expected_output="[1, 2, 3, 4]",
         test_cases=[{"input": "[1,2,2,3,3,4]", "output": "[1, 2, 3, 4]"}]),

    # ══════════════════════════════════════════════════════
    #  DICTS
    # ══════════════════════════════════════════════════════

    dict(topic='dicts', difficulty=1, question_type='mcq', points=5,
         question_text="d = {'a': 1, 'b': 2}; print(d['a']) natijasi?",
         options=["1", "2", "'a'", "Error"],
         correct_answer="1",
         explanation="Kalit bo'yicha qiymat olish."),

    dict(topic='dicts', difficulty=1, question_type='mcq', points=5,
         question_text="d = {}; d['key'] = 'value'; print(d) natijasi?",
         options=["{}", "{'key': 'value'}", "key:value", "Error"],
         correct_answer="{'key': 'value'}",
         explanation="Lug'atga yangi element qo'shish."),

    dict(topic='dicts', difficulty=2, question_type='mcq', points=10,
         question_text="d = {'a': 1, 'b': 2}; print(list(d.keys())) natijasi?",
         options=["[1, 2]", "['a', 'b']", "dict_keys(['a','b'])", "Error"],
         correct_answer="['a', 'b']",
         explanation=".keys() kalitlarni qaytaradi, list() ga o'tkazildi."),

    dict(topic='dicts', difficulty=2, question_type='mcq', points=10,
         question_text="d = {'x': 5}; print(d.get('y', 0)) natijasi?",
         options=["5", "0", "None", "Error"],
         correct_answer="0",
         explanation=".get(key, default) — kalit yo'q bo'lsa default qaytaradi."),

    dict(topic='dicts', difficulty=2, question_type='mcq', points=10,
         question_text="d = {'a': 1, 'b': 2, 'c': 3}; print(len(d)) natijasi?",
         options=["2", "3", "6", "Error"],
         correct_answer="3",
         explanation="len() lug'atdagi juftlar sonini qaytaradi."),

    dict(topic='dicts', difficulty=3, question_type='mcq', points=15,
         question_text="d = {'a': 1}; d.update({'b': 2, 'a': 10}); print(d) natijasi?",
         options=["{'a': 1, 'b': 2}", "{'a': 10, 'b': 2}", "{'a': 1}", "Error"],
         correct_answer="{'a': 10, 'b': 2}",
         explanation=".update() mavjud kalitni yangilaydi va yangisini qo'shadi."),

    dict(topic='dicts', difficulty=3, question_type='mcq', points=15,
         question_text="{k: v for k, v in [('a',1),('b',2)]} natijasi?",
         options=["Error", "{'a':1,'b':2}", "[('a',1),('b',2)]", "None"],
         correct_answer="{'a':1,'b':2}",
         explanation="Dict comprehension — tuple listdan lug'at yaratish."),

    dict(topic='dicts', difficulty=4, question_type='mcq', points=20,
         question_text="d = {'a': [1,2], 'b': [3,4]}; print(d['a'][1]) natijasi?",
         options=["1", "2", "[1,2]", "Error"],
         correct_answer="2",
         explanation="d['a'] = [1,2], [1,2][1] = 2."),

    # CODE
    dict(topic='dicts', difficulty=3, question_type='code', points=20,
         question_text="Ro'yxatdagi elementlar necha marta takrorlanganini hisoblang.\nMasalan: ['a','b','a','c','b','a'] → {'a':3,'b':2,'c':1}",
         code_template="def count_elements(lst):\n    pass",
         correct_answer="def count_elements(lst):\n    result = {}\n    for item in lst:\n        result[item] = result.get(item, 0) + 1\n    return result",
         expected_output="{'a': 3, 'b': 2, 'c': 1}",
         test_cases=[{"input": "['a','b','a','c','b','a']", "output": "{'a': 3, 'b': 2, 'c': 1}"}]),

    # ══════════════════════════════════════════════════════
    #  FUNCTIONS
    # ══════════════════════════════════════════════════════

    dict(topic='functions', difficulty=1, question_type='mcq', points=5,
         question_text="def greet(name): return 'Hello ' + name\nprint(greet('Ali')) natijasi?",
         options=["name", "Hello", "Hello Ali", "Error"],
         correct_answer="Hello Ali",
         explanation="Funksiya argumentni qabul qilib satr qaytaradi."),

    dict(topic='functions', difficulty=1, question_type='mcq', points=5,
         question_text="Funksiyasiz parametr qaysi biri to'g'ri?",
         options=["def f(x, y=10):", "def f(x=5, y):", "def f(*x, y):", "def f(**x, y):"],
         correct_answer="def f(x, y=10):",
         explanation="Default parametrlar oxirida bo'lishi shart."),

    dict(topic='functions', difficulty=2, question_type='mcq', points=10,
         question_text="def add(a, b=5): return a+b\nprint(add(3)) natijasi?",
         options=["3", "5", "8", "Error"],
         correct_answer="8",
         explanation="b=5 default qiymat, add(3) → 3+5=8."),

    dict(topic='functions', difficulty=2, question_type='mcq', points=10,
         question_text="def f(*args): return sum(args)\nprint(f(1,2,3,4)) natijasi?",
         options=["10", "[1,2,3,4]", "(1,2,3,4)", "Error"],
         correct_answer="10",
         explanation="*args ixtiyoriy sonli argumentlarni tuple ko'rinishida oladi."),

    dict(topic='functions', difficulty=3, question_type='mcq', points=15,
         question_text="x = 10\ndef f():\n    x = 20\nf()\nprint(x) natijasi?",
         options=["20", "10", "Error", "None"],
         correct_answer="10",
         explanation="Funksiya ichidagi x lokal — tashqi x o'zgarmaydi."),

    dict(topic='functions', difficulty=3, question_type='mcq', points=15,
         question_text="square = lambda x: x**2\nprint(square(5)) natijasi?",
         options=["5", "10", "25", "Error"],
         correct_answer="25",
         explanation="Lambda funksiyasi: x**2, 5**2=25."),

    dict(topic='functions', difficulty=4, question_type='mcq', points=20,
         question_text="def f(x):\n    def g():\n        return x*2\n    return g\nprint(f(5)()) natijasi?",
         options=["5", "10", "Error", "g"],
         correct_answer="10",
         explanation="Closure: g() x ni eslab qoladi, f(5)() = g() = 5*2=10."),

    dict(topic='functions', difficulty=4, question_type='mcq', points=20,
         question_text="list(map(lambda x: x*2, [1,2,3])) natijasi?",
         options=["[1,2,3]", "[2,4,6]", "[1,4,9]", "Error"],
         correct_answer="[2,4,6]",
         explanation="map() har elementga funksiya qo'llaydi."),

    dict(topic='functions', difficulty=5, question_type='mcq', points=30,
         question_text="def dec(f):\n    def wrapper(*a):\n        return f(*a) + 1\n    return wrapper\n@dec\ndef add(x,y): return x+y\nprint(add(2,3)) natijasi?",
         options=["5", "6", "Error", "None"],
         correct_answer="6",
         explanation="Decorator: add(2,3)=5, wrapper 1 qo'shadi → 6."),

    # CODE
    dict(topic='functions', difficulty=3, question_type='code', points=20,
         question_text="Faktorial hisoblovchi rekursiv funksiya yozing.\nMasalan: factorial(5) → 120",
         code_template="def factorial(n):\n    pass",
         correct_answer="def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
         expected_output="120",
         test_cases=[{"input": "5", "output": "120"}, {"input": "0", "output": "1"}]),

    dict(topic='functions', difficulty=4, question_type='code', points=25,
         question_text="Fibonacci ketma-ketligining n-elementini qaytaring (0-indeksdan).\nMasalan: fib(6) → 8",
         code_template="def fib(n):\n    pass",
         correct_answer="def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)",
         expected_output="8",
         test_cases=[{"input": "6", "output": "8"}, {"input": "0", "output": "0"}]),

    # ══════════════════════════════════════════════════════
    #  OOP
    # ══════════════════════════════════════════════════════

    dict(topic='oop', difficulty=2, question_type='mcq', points=10,
         question_text="class Dog:\n    def bark(self): return 'Woof'\nd = Dog()\nprint(d.bark()) natijasi?",
         options=["bark", "Woof", "Dog", "Error"],
         correct_answer="Woof",
         explanation="Ob'ektdan metod chaqirish."),

    dict(topic='oop', difficulty=2, question_type='mcq', points=10,
         question_text="__init__ metodi nima uchun ishlatiladi?",
         options=["Ob'ektni o'chirish", "Ob'ektni yaratishda", "Metodlarni chaqirish", "Merosni belgilash"],
         correct_answer="Ob'ektni yaratishda",
         explanation="__init__ — konstruktor, ob'ekt yaratilganda avtomatik chaqiriladi."),

    dict(topic='oop', difficulty=3, question_type='mcq', points=15,
         question_text="class A:\n    x = 10\nclass B(A): pass\nprint(B.x) natijasi?",
         options=["Error", "None", "10", "0"],
         correct_answer="10",
         explanation="B A dan meros oladi, A.x ni meros qilib oladi."),

    dict(topic='oop', difficulty=3, question_type='mcq', points=15,
         question_text="class A:\n    def hello(self): return 'A'\nclass B(A):\n    def hello(self): return 'B'\nprint(B().hello()) natijasi?",
         options=["A", "B", "AB", "Error"],
         correct_answer="B",
         explanation="Method overriding: B.hello() A.hello() ni ustidan yozadi."),

    dict(topic='oop', difficulty=4, question_type='mcq', points=20,
         question_text="@property decorator nima uchun ishlatiladi?",
         options=["Metodni statik qilish", "Atributga funksiya kabi murojaat", "Ob'ektni o'chirish", "Meros"],
         correct_answer="Atributga funksiya kabi murojaat",
         explanation="@property metodni atribut kabi chaqirish imkonini beradi."),

    dict(topic='oop', difficulty=4, question_type='mcq', points=20,
         question_text="isinstance([], list) natijasi?",
         options=["True", "False", "Error", "None"],
         correct_answer="True",
         explanation="isinstance() ob'ektning turini tekshiradi."),

    dict(topic='oop', difficulty=5, question_type='mcq', points=30,
         question_text="__str__ va __repr__ farqi nima?",
         options=["Farqi yo'q",
                  "__str__ odamlar uchun, __repr__ dasturchilar uchun",
                  "__repr__ odamlar uchun, __str__ dasturchilar uchun",
                  "__str__ faqat print() uchun"],
         correct_answer="__str__ odamlar uchun, __repr__ dasturchilar uchun",
         explanation="__str__ foydalanuvchiga ko'rinadigan, __repr__ debug uchun."),

    # CODE
    dict(topic='oop', difficulty=4, question_type='code', points=25,
         question_text="Rectangle klassi yozing: kengligi va balandligi bo'lsin, area() maydoni qaytarsin.\nMasalan: Rectangle(4,5).area() → 20",
         code_template="class Rectangle:\n    def __init__(self, width, height):\n        pass\n    def area(self):\n        pass",
         correct_answer="class Rectangle:\n    def __init__(self, w, h):\n        self.w = w\n        self.h = h\n    def area(self):\n        return self.w * self.h",
         expected_output="20"),

    # ══════════════════════════════════════════════════════
    #  EXCEPTIONS
    # ══════════════════════════════════════════════════════

    dict(topic='exceptions', difficulty=2, question_type='mcq', points=10,
         question_text="try:\n    x = 1/0\nexcept ZeroDivisionError:\n    print('zero')\nnatijasi?",
         options=["Error", "zero", "1/0", "None"],
         correct_answer="zero",
         explanation="ZeroDivisionError ushlanadi va 'zero' chiqariladi."),

    dict(topic='exceptions', difficulty=2, question_type='mcq', points=10,
         question_text="try-except-finally blokida finally qachon bajariladi?",
         options=["Faqat xato bo'lsa", "Faqat xato bo'lmasa", "Har doim", "Hech qachon"],
         correct_answer="Har doim",
         explanation="finally xato bo'ladimi yoki yo'qmi — har doim bajariladi."),

    dict(topic='exceptions', difficulty=3, question_type='mcq', points=15,
         question_text="raise ValueError('bad') qilganda nima bo'ladi?",
         options=["Dastur to'xtaydi", "ValueError istisnosi ko'tariladi", "None qaytadi", "print('bad')"],
         correct_answer="ValueError istisnosi ko'tariladi",
         explanation="raise istisno ko'taradi."),

    dict(topic='exceptions', difficulty=4, question_type='mcq', points=20,
         question_text="try:\n    int('abc')\nexcept (ValueError, TypeError) as e:\n    print(type(e).__name__)\nnatijasi?",
         options=["Error", "TypeError", "ValueError", "Exception"],
         correct_answer="ValueError",
         explanation="int('abc') ValueError ko'taradi."),

    # ══════════════════════════════════════════════════════
    #  FILES
    # ══════════════════════════════════════════════════════

    dict(topic='files', difficulty=2, question_type='mcq', points=10,
         question_text="Faylni o'qish uchun qaysi mod ishlatiladi?",
         options=["'w'", "'r'", "'a'", "'x'"],
         correct_answer="'r'",
         explanation="'r' = read, 'w' = write, 'a' = append, 'x' = create."),

    dict(topic='files', difficulty=3, question_type='mcq', points=15,
         question_text="with open('f.txt', 'w') as f: f.write('hi')\nBu nimani anglatadi?",
         options=["Faylni o'chiradi", "Faylga yozadi va avtomatik yopadi",
                  "Faylni o'qiydi", "Faylga qo'shadi"],
         correct_answer="Faylga yozadi va avtomatik yopadi",
         explanation="with context manager faylni avtomatik yopadi."),

    dict(topic='files', difficulty=3, question_type='mcq', points=15,
         question_text=".readlines() va .read() farqi nima?",
         options=["Farqi yo'q",
                  ".readlines() qator ro'yxati, .read() butun matn",
                  ".read() qator ro'yxati, .readlines() butun matn",
                  ".readlines() faqat birinchi qator"],
         correct_answer=".readlines() qator ro'yxati, .read() butun matn",
         explanation=".readlines() har bir qatorni list elementi sifatida qaytaradi."),

    # ══════════════════════════════════════════════════════
    #  MODULES
    # ══════════════════════════════════════════════════════

    dict(topic='modules', difficulty=1, question_type='mcq', points=5,
         question_text="import random; random.randint(1,10) nima qaytaradi?",
         options=["1 dan 10 gacha float", "1 dan 10 gacha integer (chegaralar bilan)",
                  "0 dan 9 gacha integer", "Error"],
         correct_answer="1 dan 10 gacha integer (chegaralar bilan)",
         explanation="randint(a,b) a dan b gacha (ikkalasi ham kiradi) butun son."),

    dict(topic='modules', difficulty=2, question_type='mcq', points=10,
         question_text="from math import sqrt; print(sqrt(16)) natijasi?",
         options=["4", "4.0", "16", "Error"],
         correct_answer="4.0",
         explanation="math.sqrt() float qaytaradi."),

    dict(topic='modules', difficulty=2, question_type='mcq', points=10,
         question_text="import os; os.getcwd() nima qaytaradi?",
         options=["OS nomi", "Joriy papka yo'li", "Fayllar ro'yxati", "Error"],
         correct_answer="Joriy papka yo'li",
         explanation="os.getcwd() = get current working directory."),

    dict(topic='modules', difficulty=3, question_type='mcq', points=15,
         question_text="from datetime import datetime; datetime.now() nima qaytaradi?",
         options=["Sana (faqat)", "Vaqt (faqat)", "Sana va vaqt", "Error"],
         correct_answer="Sana va vaqt",
         explanation="datetime.now() joriy sana va vaqtni qaytaradi."),

    dict(topic='modules', difficulty=3, question_type='mcq', points=15,
         question_text="import json; json.dumps({'a': 1}) natijasi?",
         options=["{'a': 1}", '\'{"a": 1}\'', "a=1", "Error"],
         correct_answer='\'{"a": 1}\'',
         explanation="json.dumps() Python ob'ektini JSON string ga o'tkazadi."),

    # ══════════════════════════════════════════════════════
    #  ALGORITHMS
    # ══════════════════════════════════════════════════════

    dict(topic='algorithms', difficulty=3, question_type='mcq', points=15,
         question_text="Bubble sort vaqt murakkabligi (worst case)?",
         options=["O(n)", "O(n log n)", "O(n²)", "O(1)"],
         correct_answer="O(n²)",
         explanation="Bubble sort har juftni n marta solishtiradi → O(n²)."),

    dict(topic='algorithms', difficulty=3, question_type='mcq', points=15,
         question_text="Binary search ishlashi uchun ro'yxat qanday bo'lishi kerak?",
         options=["Istalgan tartibda", "Saralangan", "Faqat sonlardan iborat", "Bo'sh bo'lmagan"],
         correct_answer="Saralangan",
         explanation="Binary search faqat saralangan ro'yxatda ishlaydi."),

    dict(topic='algorithms', difficulty=4, question_type='mcq', points=20,
         question_text="Rekursiv funksiyada base case nima uchun kerak?",
         options=["Tezlashtirish", "Cheksiz rekursiyani oldini olish", "Xotira tejash", "Sintaksis"],
         correct_answer="Cheksiz rekursiyani oldini olish",
         explanation="Base case rekursiyani to'xtatuvchi shart."),

    dict(topic='algorithms', difficulty=4, question_type='mcq', points=20,
         question_text="Stack ma'lumotlar tuzilmasi qaysi tamoyil bo'yicha ishlaydi?",
         options=["FIFO", "LIFO", "Random", "Priority"],
         correct_answer="LIFO",
         explanation="Stack = Last In First Out — oxirgi kirgan birinchi chiqadi."),

    dict(topic='algorithms', difficulty=5, question_type='mcq', points=30,
         question_text="Dynamic programming va rekursiyaning asosiy farqi?",
         options=["DP tezroq chunki natijalarni eslab qoladi (memoization)",
                  "Rekursiya tezroq",
                  "DP faqat graflarda ishlaydi",
                  "Farqi yo'q"],
         correct_answer="DP tezroq chunki natijalarni eslab qoladi (memoization)",
         explanation="DP = avval hisoblangan natijalarni qayta ishlatish."),

    # CODE
    dict(topic='algorithms', difficulty=3, question_type='code', points=20,
         question_text="Ro'yxatni bubble sort bilan saraling.\nMasalan: [3,1,2] → [1,2,3]",
         code_template="def bubble_sort(lst):\n    pass",
         correct_answer="def bubble_sort(lst):\n    n = len(lst)\n    for i in range(n):\n        for j in range(0, n-i-1):\n            if lst[j] > lst[j+1]:\n                lst[j], lst[j+1] = lst[j+1], lst[j]\n    return lst",
         expected_output="[1, 2, 3]",
         test_cases=[{"input": "[3,1,2]", "output": "[1, 2, 3]"}]),

    dict(topic='algorithms', difficulty=4, question_type='code', points=25,
         question_text="Binary search funksiyasini yozing. Element topilsa indeksini, topilmasa -1 qaytarsin.\nMasalan: binary_search([1,2,3,4,5], 3) → 2",
         code_template="def binary_search(lst, target):\n    pass",
         correct_answer="def binary_search(lst, target):\n    lo, hi = 0, len(lst)-1\n    while lo <= hi:\n        mid = (lo+hi)//2\n        if lst[mid] == target: return mid\n        elif lst[mid] < target: lo = mid+1\n        else: hi = mid-1\n    return -1",
         expected_output="2",
         test_cases=[{"input": "[1,2,3,4,5], 3", "output": "2"}, {"input": "[1,2,3], 9", "output": "-1"}]),

    dict(topic='algorithms', difficulty=5, question_type='code', points=30,
         question_text="Berilgan satr palindrom ekanligini tekshiring (katta-kichik harf farqi yo'q).\nMasalan: 'Racecar' → True, 'hello' → False",
         code_template="def is_palindrome(s):\n    pass",
         correct_answer="def is_palindrome(s):\n    s = s.lower()\n    return s == s[::-1]",
         expected_output="True",
         test_cases=[{"input": "'Racecar'", "output": "True"}, {"input": "'hello'", "output": "False"}]),

    # ══════════════════════════════════════════════════════
    #  Qo'shimcha savollar (har topic uchun)
    # ══════════════════════════════════════════════════════

    # BASICS qo'shimcha
    dict(topic='basics', difficulty=2, question_type='mcq', points=10,
         question_text="print(type(3.14)) natijasi?",
         options=["<class 'int'>", "<class 'float'>", "<class 'number'>", "Error"],
         correct_answer="<class 'float'>",
         explanation="3.14 — float tur."),

    dict(topic='basics', difficulty=3, question_type='mcq', points=15,
         question_text="x = [1,2,3]; y = x.copy(); y.append(4); print(x) natijasi?",
         options=["[1,2,3,4]", "[1,2,3]", "[4]", "Error"],
         correct_answer="[1,2,3]",
         explanation=".copy() sayoz nusxa yaratadi, y o'zgarmaydi x uchun."),

    dict(topic='basics', difficulty=4, question_type='mcq', points=20,
         question_text="id(a) == id(b) nima tekshiradi?",
         options=["Qiymat tengligi", "Bir xil ob'ektga ishora qilishmi", "Tur tengligi", "Uzunlik tengligi"],
         correct_answer="Bir xil ob'ektga ishora qilishmi",
         explanation="id() ob'ektning xotira manzilini qaytaradi."),

    # STRINGS qo'shimcha
    dict(topic='strings', difficulty=2, question_type='mcq', points=10,
         question_text="'Python'.startswith('Py') natijasi?",
         options=["True", "False", "Py", "Error"],
         correct_answer="True",
         explanation=".startswith() satr shu bilan boshlanishini tekshiradi."),

    dict(topic='strings', difficulty=3, question_type='mcq', points=15,
         question_text="'hello world'.split() natijasi?",
         options=["'hello', 'world'", "['hello', 'world']", "['hello world']", "Error"],
         correct_answer="['hello', 'world']",
         explanation=".split() bo'shliq bo'yicha ajratadi, list qaytaradi."),

    dict(topic='strings', difficulty=4, question_type='mcq', points=20,
         question_text="s = 'abcde'; print(s[::2]) natijasi?",
         options=["abcde", "ace", "bdf", "Error"],
         correct_answer="ace",
         explanation="[::2] har ikkinchi belgini oladi: a(0), c(2), e(4)."),

    # LISTS qo'shimcha
    dict(topic='lists', difficulty=2, question_type='mcq', points=10,
         question_text="lst = [1,2,3]; lst.insert(1, 10); print(lst) natijasi?",
         options=["[10,1,2,3]", "[1,10,2,3]", "[1,2,3,10]", "Error"],
         correct_answer="[1,10,2,3]",
         explanation=".insert(i, x) i-indeksga x ni qo'yadi."),

    dict(topic='lists', difficulty=3, question_type='mcq', points=15,
         question_text="list(range(2, 10, 3)) natijasi?",
         options=["[2,5,8]", "[2,3,4,5,6,7,8,9]", "[2,4,6,8]", "Error"],
         correct_answer="[2,5,8]",
         explanation="range(2,10,3): 2, 2+3=5, 5+3=8, 8+3=11 (>10 to'xtaydi)."),

    # FUNCTIONS qo'shimcha
    dict(topic='functions', difficulty=2, question_type='mcq', points=10,
         question_text="filter(lambda x: x>3, [1,2,3,4,5]) — list qilsak?",
         options=["[1,2,3]", "[4,5]", "[3,4,5]", "Error"],
         correct_answer="[4,5]",
         explanation="filter() shartga to'g'ri kelganlarni saqlaydi: 4>3, 5>3."),

    dict(topic='functions', difficulty=3, question_type='mcq', points=15,
         question_text="def f(**kwargs): return kwargs\nprint(f(a=1,b=2)) natijasi?",
         options=["(1, 2)", "{'a':1,'b':2}", "[1, 2]", "Error"],
         correct_answer="{'a':1,'b':2}",
         explanation="**kwargs kalit-qiymat juftlarini dict ko'rinishida oladi."),

    # OOP qo'shimcha
    dict(topic='oop', difficulty=3, question_type='mcq', points=15,
         question_text="@staticmethod decorator nima qiladi?",
         options=["self parametrsiz metod yaratadi",
                  "Ob'ektni o'chiradi",
                  "Merosni bloklaydi",
                  "Atributni yashiradi"],
         correct_answer="self parametrsiz metod yaratadi",
         explanation="@staticmethod self yoki cls olmaydi, oddiy funksiya kabi."),

    dict(topic='oop', difficulty=4, question_type='mcq', points=20,
         question_text="__len__ va __str__ kabi metodlar nima deb ataladi?",
         options=["Magic methods (dunder)", "Private methods", "Static methods", "Abstract methods"],
         correct_answer="Magic methods (dunder)",
         explanation="__ bilan boshlanuvchi metodlar magic/dunder metodlar."),

    # ALGORITHMS qo'shimcha
    dict(topic='algorithms', difficulty=3, question_type='mcq', points=15,
         question_text="Two Sum masalasi: [2,7,11,15], target=9. Javob?",
         options=["[0,1]", "[1,2]", "[0,2]", "[2,3]"],
         correct_answer="[0,1]",
         explanation="2+7=9, indekslari 0 va 1."),

    dict(topic='algorithms', difficulty=4, question_type='mcq', points=20,
         question_text="Merge sort vaqt murakkabligi?",
         options=["O(n)", "O(n²)", "O(n log n)", "O(log n)"],
         correct_answer="O(n log n)",
         explanation="Merge sort barcha holatlarda O(n log n) ishlaydi."),

    # CODE qo'shimcha
    dict(topic='algorithms', difficulty=3, question_type='code', points=20,
         question_text="Ikkita saralangan ro'yxatni birlashtiring (natija ham saralangan bo'lsin).\nMasalan: [1,3,5],[2,4,6] → [1,2,3,4,5,6]",
         code_template="def merge_sorted(a, b):\n    pass",
         correct_answer="def merge_sorted(a, b):\n    return sorted(a + b)",
         expected_output="[1, 2, 3, 4, 5, 6]"),

    dict(topic='functions', difficulty=4, question_type='code', points=25,
         question_text="Memoization bilan Fibonacci funksiyasi yozing.\nfib(10) → 55",
         code_template="def fib_memo(n, memo={}):\n    pass",
         correct_answer="def fib_memo(n, memo={}):\n    if n in memo: return memo[n]\n    if n <= 1: return n\n    memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)\n    return memo[n]",
         expected_output="55"),

    dict(topic='lists', difficulty=4, question_type='code', points=25,
         question_text="Ro'yxatni ikki qismga bo'ling: juft va toq sonlar.\nMasalan: [1,2,3,4,5] → ([2,4],[1,3,5])",
         code_template="def split_even_odd(lst):\n    pass",
         correct_answer="def split_even_odd(lst):\n    evens = [x for x in lst if x%2==0]\n    odds  = [x for x in lst if x%2!=0]\n    return (evens, odds)",
         expected_output="([2, 4], [1, 3, 5])"),

    dict(topic='dicts', difficulty=4, question_type='code', points=25,
         question_text="Ikkita lug'atni birlashtiring (ikkinchisi ustunlik qilsin).\nMasalan: {'a':1,'b':2}, {'b':3,'c':4} → {'a':1,'b':3,'c':4}",
         code_template="def merge_dicts(d1, d2):\n    pass",
         correct_answer="def merge_dicts(d1, d2):\n    return {**d1, **d2}",
         expected_output="{'a': 1, 'b': 3, 'c': 4}"),

    dict(topic='strings', difficulty=4, question_type='code', points=25,
         question_text="Satrda so'zlar necha marta takrorlanganini hisoblang.\nMasalan: 'hello world hello' → {'hello':2,'world':1}",
         code_template="def word_count(s):\n    pass",
         correct_answer="def word_count(s):\n    words = s.split()\n    return {w: words.count(w) for w in set(words)}",
         expected_output="{'hello': 2, 'world': 1}"),

    dict(topic='oop', difficulty=5, question_type='code', points=30,
         question_text="Stack klassini yozing: push, pop, peek, is_empty metodlari bilan.\nStack([]).is_empty() → True",
         code_template="class Stack:\n    def __init__(self):\n        pass\n    def push(self, item):\n        pass\n    def pop(self):\n        pass\n    def peek(self):\n        pass\n    def is_empty(self):\n        pass",
         correct_answer="class Stack:\n    def __init__(self):\n        self.data=[]\n    def push(self,x): self.data.append(x)\n    def pop(self): return self.data.pop()\n    def peek(self): return self.data[-1]\n    def is_empty(self): return len(self.data)==0",
         expected_output="True"),

    dict(topic='exceptions', difficulty=4, question_type='code', points=25,
         question_text="Xavfsiz bo'linma funksiyasi yozing: nolga bo'lishda 0 qaytarsin.\nsafe_divide(10, 2) → 5.0, safe_divide(5, 0) → 0",
         code_template="def safe_divide(a, b):\n    pass",
         correct_answer="def safe_divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return 0",
         expected_output="5.0"),

    dict(topic='modules', difficulty=3, question_type='code', points=20,
         question_text="Joriy sanani 'YYYY-MM-DD' formatida qaytaring.\nMasalan: '2024-01-15'",
         code_template="from datetime import datetime\ndef today_str():\n    pass",
         correct_answer="from datetime import datetime\ndef today_str():\n    return datetime.now().strftime('%Y-%m-%d')",
         expected_output="2024-01-15"),

]


class Command(BaseCommand):
    help = "200+ ta placement test savolini yaratadi"

    def handle(self, *args, **kwargs):
        created = 0
        skipped = 0
        for q in QUESTIONS:
            obj, is_new = PlacementQuestion.objects.get_or_create(
                question_text=q['question_text'],
                defaults={k: v for k, v in q.items() if k != 'question_text'}
            )
            if is_new:
                created += 1
            else:
                skipped += 1

        total = PlacementQuestion.objects.count()
        self.stdout.write(self.style.SUCCESS(
            f"OK: {created} ta savol yaratildi, {skipped} ta mavjud. Jami: {total} ta."
        ))
