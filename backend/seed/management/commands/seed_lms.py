"""
Seed script: real Python kurslar, YouTube videolar, tasklar bilan.
"""
from django.core.management.base import BaseCommand
from django.utils.text import slugify
import uuid

from src.core.models import *


# ─────────────────────────────────────────────
#  KURSLAR
# ─────────────────────────────────────────────
PYTHON_COURSES = [
    {
        "title": "Python Asoslari",
        "description": (
            "Python dasturlash tilining asosiy tushunchalari: o'zgaruvchilar, "
            "ma'lumot turlari (int, float, str, bool), shartli operatorlar (if/elif/else), "
            "sikllar (for, while) va asosiy kiritish/chiqarish operatsiyalari. "
            "Ushbu kurs Python bilan tanishish uchun eng yaxshi boshlang'ich nuqta."
        ),
        "price": 0,
        "level": "Beginner",
        "lessons": [
            {
                "title": "Python'ga Kirish va O'rnatish",
                "order": 1,
                "content": (
                    "=== Python nima? ===\n"
                    "Python - 1991-yilda Guido van Rossum tomonidan yaratilgan, "
                    "o'qilishi oson va kuchli dasturlash tili.\n\n"
                    "=== Python'ni o'rnatish ===\n"
                    "1. python.org saytidan yuklab oling\n"
                    "2. O'rnatish vaqtida 'Add Python to PATH' belgisini qo'ying\n"
                    "3. Terminalda tekshiring:\n\n"
                    "python --version\n"
                    "# Python 3.11.0\n\n"
                    "=== Birinchi dastur ===\n"
                    "# hello.py faylini oching va yozing:\n"
                    "print('Salom, Dunyo!')\n"
                    "print('Python o\\'rganish boshlandi!')\n\n"
                    "# Ishga tushirish:\n"
                    "# python hello.py\n\n"
                    "=== Python Interpreter (REPL) ===\n"
                    "# Terminalda python yozing:\n"
                    ">>> 2 + 3\n"
                    "5\n"
                    ">>> print('Salom')\n"
                    "Salom\n"
                    ">>> 'Python' * 3\n"
                    "'PythonPythonPython'\n\n"
                    "=== Izohlar (Comments) ===\n"
                    "# Bu bir qatorli izoh\n"
                    "x = 5  # bu ham izoh\n\n"
                    "'''\n"
                    "Bu ko'p qatorli\n"
                    "izoh (docstring)\n"
                    "'''\n\n"
                    "=== Asosiy terminlar ===\n"
                    "# statement - bajariladigan buyruq\n"
                    "# expression - qiymat beradigan ifoda\n"
                    "# syntax - til qoidalari\n"
                    "# indentation - bo'sh joy (Python'da muhim!)\n"
                    "if True:\n"
                    "    print('Indentation muhim!')  # 4 ta bo'sh joy"
                ),
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
            },
            {
                "title": "O'zgaruvchilar va Ma'lumot Turlari",
                "order": 2,
                "content": (
                    "=== O'zgaruvchi (Variable) ===\n"
                    "O'zgaruvchi - ma'lumotni saqlash uchun ishlatiladigan nom.\n\n"
                    "ism = 'Ali'        # str - matn\n"
                    "yosh = 20          # int - butun son\n"
                    "narx = 19.99       # float - kasr son\n"
                    "aktiv = True       # bool - mantiqiy qiymat\n\n"
                    "=== int (butun sonlar) ===\n"
                    "a = 10\n"
                    "b = -5\n"
                    "katta = 1_000_000  # minglik ajratgich\n"
                    "print(type(a))     # <class 'int'>\n"
                    "print(a + b)       # 5\n"
                    "print(a * b)       # -50\n"
                    "print(a // 3)      # 3 (butun bo'linma)\n"
                    "print(a % 3)       # 1 (qoldiq)\n"
                    "print(a ** 2)      # 100 (daraja)\n\n"
                    "=== float (kasr sonlar) ===\n"
                    "pi = 3.14159\n"
                    "temp = -0.5\n"
                    "print(round(pi, 2))  # 3.14\n"
                    "print(int(pi))       # 3 (butun qismga o'tkazish)\n\n"
                    "=== str (matn) ===\n"
                    "ism = 'Sarvar'\n"
                    "shahar = \"Toshkent\"\n"
                    "print(len(ism))     # 6 (harflar soni)\n"
                    "print(ism + ' Xasanov')  # 'Sarvar Xasanov'\n"
                    "print(ism.upper())  # 'SARVAR'\n\n"
                    "=== bool (mantiqiy) ===\n"
                    "togri = True\n"
                    "xato = False\n"
                    "print(togri and xato)  # False\n"
                    "print(togri or xato)   # True\n"
                    "print(not togri)       # False\n\n"
                    "=== Tur aniqlash va o'zgartirish ===\n"
                    "x = 42\n"
                    "print(type(x))       # <class 'int'>\n"
                    "print(str(x))        # '42'\n"
                    "print(float(x))      # 42.0\n"
                    "print(bool(0))       # False\n"
                    "print(bool(1))       # True\n"
                    "print(bool(''))      # False\n"
                    "print(bool('text'))  # True\n\n"
                    "=== Ko'p o'zgaruvchi birlikda ===\n"
                    "a, b, c = 1, 2, 3\n"
                    "x = y = z = 0\n"
                    "a, b = b, a  # qayta almashtirish"
                ),
                "video_url": "https://www.youtube.com/watch?v=khKv-8q7YmY",
            },
            {
                "title": "Matn (String) bilan Ishlash",
                "order": 3,
                "content": (
                    "Python'da matn (string) bilan ishlashning asosiy usullari.\n\n"
                    "=== String yaratish ===\n"
                    "s = 'Salom, dunyo!'\n"
                    "s2 = \"Python juda ajoyib\"\n"
                    "ko'p_qatorli = '''Bu\n"
                    "ko'p qatorli\n"
                    "matn'''\n\n"
                    "=== Asosiy metodlar ===\n"
                    "s = 'python dasturlash'\n"
                    "print(s.upper())         # 'PYTHON DASTURLASH'\n"
                    "print(s.lower())         # 'python dasturlash'\n"
                    "print(s.title())         # 'Python Dasturlash'\n"
                    "print(s.capitalize())    # 'Python dasturlash'\n\n"
                    "=== Qidirish va almashtirish ===\n"
                    "s = 'Salom, dunyo!'\n"
                    "print(s.find('dunyo'))   # 7 (indeks)\n"
                    "print(s.count('l'))      # 1\n"
                    "print(s.replace('dunyo', 'Python'))  # 'Salom, Python!'\n"
                    "print('dunyo' in s)      # True\n\n"
                    "=== Split va Join ===\n"
                    "matn = 'alma banan gilos'\n"
                    "mevalar = matn.split()        # ['alma', 'banan', 'gilos']\n"
                    "birlashgan = ', '.join(mevalar)  # 'alma, banan, gilos'\n\n"
                    "=== f-string (Format string) ===\n"
                    "ism = 'Ali'\n"
                    "yosh = 20\n"
                    "print(f'{ism} {yosh} yoshda')  # 'Ali 20 yoshda'\n"
                    "print(f'Pi = {3.14159:.2f}')   # 'Pi = 3.14'\n\n"
                    "=== Strip (bo'sh joylarni olib tashlash) ===\n"
                    "s = '   salom   '\n"
                    "print(s.strip())    # 'salom'\n"
                    "print(s.lstrip())   # 'salom   '\n"
                    "print(s.rstrip())   # '   salom'\n\n"
                    "=== Indeks va Slicing ===\n"
                    "s = 'Python'\n"
                    "print(s[0])     # 'P'\n"
                    "print(s[-1])    # 'n'\n"
                    "print(s[0:3])   # 'Pyt'\n"
                    "print(s[::-1])  # 'nohtyP' (teskari)\n\n"
                    "=== Tekshirish metodlari ===\n"
                    "print('123'.isdigit())    # True\n"
                    "print('abc'.isalpha())    # True\n"
                    "print('Abc'.isupper())    # False\n"
                    "print('abc'.startswith('ab'))  # True\n"
                    "print('abc'.endswith('bc'))    # True"
                ),
                "video_url": "https://www.youtube.com/watch?v=k9TUPpGqYTo",
                "required_task": True,  # Bu darsga majburiy masala bog'lanadi
            },
            {
                "title": "Shartli Operatorlar (if/elif/else)",
                "order": 4,
                "content": (
                    "=== Shartli operator ===\n"
                    "Dastur bajarilish yo'nalishini shartga qarab tanlaydi.\n\n"
                    "=== Asosiy if/else ===\n"
                    "yosh = 18\n"
                    "if yosh >= 18:\n"
                    "    print('Voyaga yetgan')\n"
                    "else:\n"
                    "    print('Voyaga yetmagan')\n\n"
                    "=== if/elif/else ===\n"
                    "ball = 75\n"
                    "if ball >= 90:\n"
                    "    baho = 'A'\n"
                    "elif ball >= 75:\n"
                    "    baho = 'B'\n"
                    "elif ball >= 60:\n"
                    "    baho = 'C'\n"
                    "else:\n"
                    "    baho = 'F'\n"
                    "print(f'Baho: {baho}')  # Baho: B\n\n"
                    "=== Taqqoslash operatorlari ===\n"
                    "x = 10\n"
                    "print(x == 10)   # True  (teng)\n"
                    "print(x != 5)    # True  (teng emas)\n"
                    "print(x > 5)     # True  (katta)\n"
                    "print(x < 20)    # True  (kichik)\n"
                    "print(x >= 10)   # True  (katta-teng)\n"
                    "print(x <= 10)   # True  (kichik-teng)\n\n"
                    "=== Mantiqiy operatorlar ===\n"
                    "a, b = 5, 10\n"
                    "print(a > 0 and b > 0)   # True  (ikkalasi ham)\n"
                    "print(a > 10 or b > 5)   # True  (bittasi)\n"
                    "print(not a > 10)         # True  (inkor)\n\n"
                    "=== Ternary (bir qatorli) ===\n"
                    "son = 7\n"
                    "natija = 'juft' if son % 2 == 0 else 'toq'\n"
                    "print(natija)  # toq\n\n"
                    "=== in operatori ===\n"
                    "mevalar = ['olma', 'banan', 'gilos']\n"
                    "if 'olma' in mevalar:\n"
                    "    print('Olma bor!')\n"
                    "ism = 'Python'\n"
                    "if 'Py' in ism:\n"
                    "    print('Py bor!')"
                ),
                "video_url": "https://www.youtube.com/watch?v=DZwmZ8Usvnk",
            },
            {
                "title": "for Sikli va range()",
                "order": 5,
                "content": (
                    "=== for sikli ===\n"
                    "Ketma-ketlik (list, string, range) bo'yicha takrorlash uchun.\n\n"
                    "=== Asosiy for ===\n"
                    "for i in range(5):\n"
                    "    print(i, end=' ')  # 0 1 2 3 4\n\n"
                    "=== range() funksiyasi ===\n"
                    "range(5)       # 0,1,2,3,4\n"
                    "range(1, 6)    # 1,2,3,4,5\n"
                    "range(0, 10, 2) # 0,2,4,6,8 (qadam=2)\n"
                    "range(10, 0, -1) # 10,9,...,1 (teskari)\n\n"
                    "for i in range(1, 6):\n"
                    "    print(f'{i} x 3 = {i*3}')\n"
                    "# 1 x 3 = 3\n"
                    "# 2 x 3 = 6  ...\n\n"
                    "=== List ustida for ===\n"
                    "mevalar = ['olma', 'banan', 'gilos']\n"
                    "for meva in mevalar:\n"
                    "    print(meva.upper())\n"
                    "# OLMA  BANAN  GILOS\n\n"
                    "=== enumerate() bilan indeks ===\n"
                    "for i, meva in enumerate(mevalar):\n"
                    "    print(f'{i}: {meva}')\n"
                    "# 0: olma  1: banan  2: gilos\n\n"
                    "=== String ustida for ===\n"
                    "for harf in 'Python':\n"
                    "    print(harf, end='-')  # P-y-t-h-o-n-\n\n"
                    "=== break va continue ===\n"
                    "for i in range(10):\n"
                    "    if i == 3:\n"
                    "        continue   # 3 ni o'tkazib yuboradi\n"
                    "    if i == 7:\n"
                    "        break      # 7 da to'xtaydi\n"
                    "    print(i, end=' ')  # 0 1 2 4 5 6\n\n"
                    "=== Ichma-ich for ===\n"
                    "for i in range(1, 4):\n"
                    "    for j in range(1, 4):\n"
                    "        print(f'{i}x{j}={i*j}', end='  ')\n"
                    "    print()"
                ),
                "video_url": "https://www.youtube.com/watch?v=0ZvaDa8eT5s",
            },
            {
                "title": "while Sikli va break/continue",
                "order": 6,
                "content": (
                    "=== while sikli ===\n"
                    "Shart to'g'ri bo'lguncha takrorlanadi.\n\n"
                    "=== Asosiy while ===\n"
                    "n = 1\n"
                    "while n <= 5:\n"
                    "    print(n, end=' ')  # 1 2 3 4 5\n"
                    "    n += 1\n\n"
                    "=== while True (cheksiz) + break ===\n"
                    "count = 0\n"
                    "while True:\n"
                    "    count += 1\n"
                    "    if count >= 5:\n"
                    "        break\n"
                    "print(f'Jami: {count}')  # Jami: 5\n\n"
                    "=== continue (keyingisiga o'tish) ===\n"
                    "i = 0\n"
                    "while i < 10:\n"
                    "    i += 1\n"
                    "    if i % 2 == 0:\n"
                    "        continue    # juft sonlarni o'tkazib yuboradi\n"
                    "    print(i, end=' ')  # 1 3 5 7 9\n\n"
                    "=== while/else ===\n"
                    "# else bloki while normal tugaganida ishlaydi (break bo'lmaganda)\n"
                    "n = 0\n"
                    "while n < 3:\n"
                    "    print(n)\n"
                    "    n += 1\n"
                    "else:\n"
                    "    print('Sikl tugadi')\n\n"
                    "=== Topish o'yini misoli ===\n"
                    "maxfiy = 7\n"
                    "urinish = 0\n"
                    "tahmin = 0\n"
                    "while tahmin != maxfiy:\n"
                    "    tahmin = int(input('Son kiring: '))\n"
                    "    urinish += 1\n"
                    "    if tahmin < maxfiy:\n"
                    "        print('Kattaroq!')\n"
                    "    elif tahmin > maxfiy:\n"
                    "        print('Kichikroq!')\n"
                    "print(f'{urinish} ta urinishda topdingiz!')"
                ),
                "video_url": "https://www.youtube.com/watch?v=6iF8Xb7Z3wQ",
            },
            {
                "title": "Kiritish va Chiqarish (input/print)",
                "order": 7,
                "content": (
                    "=== print() funksiyasi ===\n"
                    "Ekranga ma'lumot chiqarish.\n\n"
                    "print('Salom!')                  # Salom!\n"
                    "print(42)                        # 42\n"
                    "print('a', 'b', 'c')             # a b c\n"
                    "print('a', 'b', sep='-')         # a-b\n"
                    "print('Birinchi', end=' ')        # Bo'sh joy bilan\n"
                    "print('Ikkinchi')                # bitta satrda\n\n"
                    "=== f-string bilan chiqarish ===\n"
                    "ism = 'Kamol'\n"
                    "yosh = 22\n"
                    "print(f'Ism: {ism}, Yosh: {yosh}')    # Ism: Kamol, Yosh: 22\n"
                    "print(f'Pi = {3.14159:.2f}')           # Pi = 3.14\n"
                    "print(f'{100:>10}')                    # '       100' (o'ngga)\n"
                    "print(f'{100:<10}')                    # '100       ' (chapga)\n\n"
                    "=== input() funksiyasi ===\n"
                    "ism = input('Ismingizni kiriting: ')\n"
                    "print(f'Salom, {ism}!')\n\n"
                    "=== Sonli kiritish ===\n"
                    "# input() har doim string qaytaradi!\n"
                    "yosh = int(input('Yoshingiz: '))     # stringni int ga\n"
                    "narx = float(input('Narx: '))        # stringni float ga\n\n"
                    "=== Xatolarni boshqarish ===\n"
                    "try:\n"
                    "    son = int(input('Son kiriting: '))\n"
                    "    print(f'Kvadrati: {son**2}')\n"
                    "except ValueError:\n"
                    "    print('Xato: Iltimos son kiriting!')\n\n"
                    "=== Ko'p qiymat kiritish ===\n"
                    "# 'ali 20 toshkent' formatida kiritish\n"
                    "ma_lumot = input('Ism yosh shahar: ').split()\n"
                    "ism, yosh, shahar = ma_lumot\n"
                    "print(f'{ism} {yosh} yoshda, {shahar}da yashaydi')"
                ),
                "video_url": "https://www.youtube.com/watch?v=Bv-8JTgfPVE",
            },
            {
                "title": "Amaliy Loyiha: Kalkulyator",
                "order": 8,
                "content": (
                    "=== Oddiy Kalkulyator Loyihasi ===\n"
                    "O'rganilgan bilimlarni qo'llab, to'liq ishlaydigan kalkulyator.\n\n"
                    "=== 1-qadam: Asosiy amallar ===\n"
                    "def qoshish(a, b):     return a + b\n"
                    "def ayirish(a, b):     return a - b\n"
                    "def koptirish(a, b):   return a * b\n"
                    "def bolish(a, b):\n"
                    "    if b == 0:\n"
                    "        return 'Xato: 0 ga bolish mumkin emas'\n"
                    "    return a / b\n\n"
                    "=== 2-qadam: Foydalanuvchi interfeysi ===\n"
                    "def kalkulyator():\n"
                    "    print('=== Kalkulyator ===')\n"
                    "    print('Amallar: + - * /')\n\n"
                    "    while True:\n"
                    "        try:\n"
                    "            a = float(input('1-son: '))\n"
                    "            amal = input('Amal (+, -, *, /): ')\n"
                    "            b = float(input('2-son: '))\n"
                    "        except ValueError:\n"
                    "            print('Xato: Son kiriting!')\n"
                    "            continue\n\n"
                    "        if amal == '+':\n"
                    "            natija = qoshish(a, b)\n"
                    "        elif amal == '-':\n"
                    "            natija = ayirish(a, b)\n"
                    "        elif amal == '*':\n"
                    "            natija = koptirish(a, b)\n"
                    "        elif amal == '/':\n"
                    "            natija = bolish(a, b)\n"
                    "        else:\n"
                    "            print('Noma\\'lum amal!')\n"
                    "            continue\n\n"
                    "        print(f'Natija: {a} {amal} {b} = {natija}')\n\n"
                    "        yana = input('Davom etasizmi? (ha/yoq): ')\n"
                    "        if yana.lower() != 'ha':\n"
                    "            print('Xayr!')\n"
                    "            break\n\n"
                    "kalkulyator()"
                ),
                "video_url": "https://www.youtube.com/watch?v=NqALzStgBKM",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Python'da o'zgaruvchi e'lon qilish uchun qaysi kalit so'z ishlatiladi?",
                 "answers": ["var", "let", "Kalit so'z kerak emas", "define"], "correct": 2},
                {"text": "print(\"Salom\") buyrug'i nima qiladi?",
                 "answers": ["Faylga yozadi", "Ekranga chiqaradi", "O'zgaruvchi yaratadi", "Xatolik beradi"], "correct": 1},
                {"text": "Python'da butun sonlar qaysi tur bilan ifodalanadi?",
                 "answers": ["str", "float", "int", "bool"], "correct": 2},
                {"text": "if-else konstruksiyasi nima uchun ishlatiladi?",
                 "answers": ["Sikllar uchun", "Shartli operatorlar uchun", "Funksiyalar uchun", "Import uchun"], "correct": 1},
                {"text": "for sikli nima uchun ishlatiladi?",
                 "answers": ["Funksiya yaratish", "Takrorlanuvchi amallar", "O'zgaruvchi e'lon qilish", "Dasturni to'xtatish"], "correct": 1},
            ]
        }
    },
    {
        "title": "Funksiyalar va Modullar",
        "description": (
            "Funksiyalar yaratish, parametrlar va ularning turlari, "
            "return qiymatlari, rekursiya, lambda funksiyalar. Python'ning standart "
            "modullari: math, random, datetime, os bilan ishlash."
        ),
        "price": 49000,
        "level": "Beginner",
        "lessons": [
            {
                "title": "Funksiya Yaratish (def)",
                "order": 1,
                "content": (
                    "=== Funksiya nima? ===\n"
                    "Funksiya - qayta ishlatilishi mumkin bo'lgan kod bloki.\n\n"
                    "=== Asosiy sintaksis ===\n"
                    "def salomlash():\n"
                    "    print('Salom, Dunyo!')\n\n"
                    "salomlash()   # chaqirish\n"
                    "salomlash()   # qayta chaqirish\n\n"
                    "=== Parametrli funksiya ===\n"
                    "def salomlash(ism):\n"
                    "    print(f'Salom, {ism}!')\n\n"
                    "salomlash('Ali')    # Salom, Ali!\n"
                    "salomlash('Sarvar') # Salom, Sarvar!\n\n"
                    "=== Return bilan funksiya ===\n"
                    "def kvadrat(n):\n"
                    "    return n * n\n\n"
                    "natija = kvadrat(5)\n"
                    "print(natija)          # 25\n"
                    "print(kvadrat(10))     # 100\n\n"
                    "=== Funksiyaning afzalliklari ===\n"
                    "# 1. Kodni qayta ishlatish\n"
                    "# 2. Kodni modullash\n"
                    "# 3. Kodni o'qilishi osonlashtirish\n"
                    "# 4. Xatolarni topishni osonlashtirish\n\n"
                    "=== Misol: BMI hisoblash ===\n"
                    "def bmi_hisoblash(vazn, boy):\n"
                    "    bmi = vazn / (boy ** 2)\n"
                    "    if bmi < 18.5:\n"
                    "        holat = 'Ozish'\n"
                    "    elif bmi < 25:\n"
                    "        holat = 'Normal'\n"
                    "    elif bmi < 30:\n"
                    "        holat = 'Ortiqcha vazn'\n"
                    "    else:\n"
                    "        holat = 'Semizlik'\n"
                    "    return bmi, holat\n\n"
                    "bmi, holat = bmi_hisoblash(70, 1.75)\n"
                    "print(f'BMI: {bmi:.1f} - {holat}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=9Os0o3wzS_I",
            },
            {
                "title": "Parametrlar va Argumentlar",
                "order": 2,
                "content": (
                    "=== Parametr turlari ===\n\n"
                    "=== 1. Pozitsional parametrlar ===\n"
                    "def yig_indi(a, b, c):\n"
                    "    return a + b + c\n\n"
                    "print(yig_indi(1, 2, 3))   # 6\n\n"
                    "=== 2. Default (standart) qiymat ===\n"
                    "def salomlash(ism, kutish='Xush kelibsiz'):\n"
                    "    print(f'{ism}: {kutish}')\n\n"
                    "salomlash('Ali')                  # Ali: Xush kelibsiz\n"
                    "salomlash('Sarvar', 'Salom!')     # Sarvar: Salom!\n\n"
                    "=== 3. Kalit so'z argumentlari ===\n"
                    "def to_liq_ism(ism, familiya, yosh):\n"
                    "    return f'{ism} {familiya}, {yosh} yosh'\n\n"
                    "# Tartibi farq qilmaydi:\n"
                    "print(to_liq_ism(familiya='Karimov', yosh=25, ism='Sardor'))\n\n"
                    "=== 4. *args (o'zgaruvchan sonli) ===\n"
                    "def yig_indi(*sonlar):\n"
                    "    jami = 0\n"
                    "    for son in sonlar:\n"
                    "        jami += son\n"
                    "    return jami\n\n"
                    "print(yig_indi(1, 2, 3))        # 6\n"
                    "print(yig_indi(1, 2, 3, 4, 5))  # 15\n\n"
                    "=== 5. **kwargs (kalit-qiymat) ===\n"
                    "def ma_lumot(**kwargs):\n"
                    "    for kalit, qiymat in kwargs.items():\n"
                    "        print(f'{kalit}: {qiymat}')\n\n"
                    "ma_lumot(ism='Ali', yosh=20, shahar='Toshkent')\n"
                    "# ism: Ali\n"
                    "# yosh: 20\n"
                    "# shahar: Toshkent"
                ),
                "video_url": "https://www.youtube.com/watch?v=WB4hJJkfmL8",
            },
            {
                "title": "Return Qiymati",
                "order": 3,
                "content": (
                    "=== return kalit so'zi ===\n"
                    "Funksiyadan qiymat qaytarish va ijroni to'xtatish.\n\n"
                    "=== Bitta qiymat qaytarish ===\n"
                    "def kvadrat(n):\n"
                    "    return n * n\n\n"
                    "x = kvadrat(4)\n"
                    "print(x)          # 16\n"
                    "print(kvadrat(7)) # 49\n\n"
                    "=== Bir nechta qiymat qaytarish ===\n"
                    "def min_max(lst):\n"
                    "    return min(lst), max(lst)\n\n"
                    "kichik, katta = min_max([3, 1, 7, 2, 9])\n"
                    "print(f'Min: {kichik}, Max: {katta}')  # Min: 1, Max: 9\n\n"
                    "=== return None ===\n"
                    "def xabar_chiqar(matn):\n"
                    "    if not matn:\n"
                    "        return   # None qaytaradi va to'xtatadi\n"
                    "    print(matn)\n\n"
                    "natija = xabar_chiqar('')\n"
                    "print(natija)  # None\n\n"
                    "=== Erta return (early return) ===\n"
                    "def absolyut_qiymat(n):\n"
                    "    if n >= 0:\n"
                    "        return n\n"
                    "    return -n\n\n"
                    "print(absolyut_qiymat(-5))  # 5\n"
                    "print(absolyut_qiymat(3))   # 3\n\n"
                    "=== Misol: Eng katta son ===\n"
                    "def eng_katta(a, b, c):\n"
                    "    if a >= b and a >= c:\n"
                    "        return a\n"
                    "    elif b >= c:\n"
                    "        return b\n"
                    "    return c\n\n"
                    "print(eng_katta(10, 25, 15))  # 25"
                ),
                "video_url": "https://www.youtube.com/watch?v=9Os0o3wzS_I",
            },
            {
                "title": "Lambda Funksiyalar",
                "order": 4,
                "content": (
                    "=== Lambda nima? ===\n"
                    "Bir qatorli anonim (nomsiz) funksiya.\n\n"
                    "=== Asosiy sintaksis ===\n"
                    "# lambda parametr: ifoda\n\n"
                    "kvadrat = lambda x: x ** 2\n"
                    "print(kvadrat(5))   # 25\n\n"
                    "qo_sh = lambda a, b: a + b\n"
                    "print(qo_sh(3, 4))  # 7\n\n"
                    "=== map() bilan ===\n"
                    "# Har bir elementga funksiya qo'llash\n"
                    "sonlar = [1, 2, 3, 4, 5]\n"
                    "kvadratlar = list(map(lambda x: x**2, sonlar))\n"
                    "print(kvadratlar)  # [1, 4, 9, 16, 25]\n\n"
                    "ismlar = ['ali', 'sarvar', 'kamol']\n"
                    "katta = list(map(lambda s: s.upper(), ismlar))\n"
                    "print(katta)  # ['ALI', 'SARVAR', 'KAMOL']\n\n"
                    "=== filter() bilan ===\n"
                    "# Shartga mos elementlarni tanlash\n"
                    "sonlar = [1, 2, 3, 4, 5, 6, 7, 8]\n"
                    "juftlar = list(filter(lambda x: x % 2 == 0, sonlar))\n"
                    "print(juftlar)  # [2, 4, 6, 8]\n\n"
                    "=== sorted() bilan ===\n"
                    "# Maxsus tartib bo'yicha saralash\n"
                    "talabalar = [('Ali', 90), ('Sarvar', 75), ('Kamol', 88)]\n"
                    "# Ball bo'yicha saralash:\n"
                    "saralangan = sorted(talabalar, key=lambda x: x[1], reverse=True)\n"
                    "print(saralangan)\n"
                    "# [('Ali', 90), ('Kamol', 88), ('Sarvar', 75)]"
                ),
                "video_url": "https://www.youtube.com/watch?v=Ob9rY6PQMfI",
            },
            {
                "title": "Rekursiya",
                "order": 5,
                "content": (
                    "=== Rekursiya nima? ===\n"
                    "Funksiyaning o'zini o'zi chaqirishi.\n\n"
                    "=== Asosiy tuzilma ===\n"
                    "def rekursiv_funksiya(n):\n"
                    "    if n <= 0:           # Base case (to'xtash sharti)\n"
                    "        return\n"
                    "    print(n)\n"
                    "    rekursiv_funksiya(n - 1)  # O'zini chaqirish\n\n"
                    "rekursiv_funksiya(5)  # 5 4 3 2 1\n\n"
                    "=== Faktoriyel ===\n"
                    "def faktoriyel(n):\n"
                    "    if n == 0 or n == 1:   # Base case\n"
                    "        return 1\n"
                    "    return n * faktoriyel(n - 1)  # Rekursiv qadam\n\n"
                    "print(faktoriyel(5))   # 120\n"
                    "print(faktoriyel(10))  # 3628800\n\n"
                    "=== Fibonacci ===\n"
                    "def fib(n):\n"
                    "    if n <= 1:\n"
                    "        return n\n"
                    "    return fib(n-1) + fib(n-2)\n\n"
                    "for i in range(8):\n"
                    "    print(fib(i), end=' ')  # 0 1 1 2 3 5 8 13\n\n"
                    "=== Yig'indi (rekursiv) ===\n"
                    "def yig_indi(lst):\n"
                    "    if not lst:            # Bo'sh list - base case\n"
                    "        return 0\n"
                    "    return lst[0] + yig_indi(lst[1:])\n\n"
                    "print(yig_indi([1, 2, 3, 4, 5]))  # 15\n\n"
                    "=== Muhim: RecursionError ===\n"
                    "# Python standart rekursiya chuqurligii 1000\n"
                    "# Katta n uchun iterativ usul tezroq!\n"
                    "import sys\n"
                    "print(sys.getrecursionlimit())  # 1000"
                ),
                "video_url": "https://www.youtube.com/watch?v=ngCos392W4w",
            },
            {
                "title": "math va random Modullari",
                "order": 6,
                "content": (
                    "=== math moduli ===\n"
                    "import math\n\n"
                    "print(math.pi)           # 3.141592653589793\n"
                    "print(math.e)            # 2.718281828459045\n"
                    "print(math.sqrt(16))     # 4.0 (kvadrat ildiz)\n"
                    "print(math.pow(2, 10))   # 1024.0\n"
                    "print(math.floor(3.7))   # 3 (quyi butun)\n"
                    "print(math.ceil(3.2))    # 4 (yuqori butun)\n"
                    "print(math.abs(-5))      # 5 (absolyut qiymat)\n"
                    "print(math.factorial(5)) # 120\n"
                    "print(math.log(100, 10)) # 2.0\n"
                    "print(math.sin(math.pi/2))  # 1.0\n\n"
                    "=== random moduli ===\n"
                    "import random\n\n"
                    "print(random.random())         # 0.0 dan 1.0 gacha\n"
                    "print(random.randint(1, 100))  # 1 dan 100 gacha butun son\n"
                    "print(random.uniform(1.0, 5.0)) # 1.0-5.0 oralig'ida kasr\n\n"
                    "mevalar = ['olma', 'banan', 'gilos']\n"
                    "print(random.choice(mevalar))  # tasodifiy bitta\n"
                    "random.shuffle(mevalar)        # aralashtirish\n"
                    "print(mevalar)\n"
                    "print(random.sample(mevalar, 2)) # tasodifiy 2 ta\n\n"
                    "=== from ... import ===\n"
                    "from math import sqrt, pi\n"
                    "print(sqrt(25))  # 5.0 (math. siz)\n"
                    "print(pi)        # 3.14159...\n\n"
                    "from random import randint, choice\n"
                    "print(randint(1, 6))  # zar otish"
                ),
                "video_url": "https://www.youtube.com/watch?v=CqvZ3vGoGs0",
            },
            {
                "title": "datetime Moduli",
                "order": 7,
                "content": (
                    "=== datetime moduli ===\n"
                    "from datetime import datetime, date, timedelta\n\n"
                    "=== Hozirgi sana va vaqt ===\n"
                    "hozir = datetime.now()\n"
                    "print(hozir)             # 2024-01-15 14:30:25.123456\n"
                    "print(hozir.year)        # 2024\n"
                    "print(hozir.month)       # 1\n"
                    "print(hozir.day)         # 15\n"
                    "print(hozir.hour)        # 14\n"
                    "print(hozir.minute)      # 30\n\n"
                    "=== Sana yaratish ===\n"
                    "tug_ilgan = date(2000, 5, 15)\n"
                    "print(tug_ilgan)  # 2000-05-15\n\n"
                    "=== Formatlash (strftime) ===\n"
                    "print(hozir.strftime('%d.%m.%Y'))      # 15.01.2024\n"
                    "print(hozir.strftime('%H:%M'))          # 14:30\n"
                    "print(hozir.strftime('%d-%B-%Y'))       # 15-January-2024\n\n"
                    "=== Stringdan datetime (strptime) ===\n"
                    "sana_str = '15.01.2024'\n"
                    "sana = datetime.strptime(sana_str, '%d.%m.%Y')\n"
                    "print(sana)  # 2024-01-15 00:00:00\n\n"
                    "=== timedelta (farq) ===\n"
                    "bugun = date.today()\n"
                    "7_kun_keyin = bugun + timedelta(days=7)\n"
                    "print(7_kun_keyin)\n\n"
                    "tug_ilgan = date(2000, 5, 15)\n"
                    "yosh = (date.today() - tug_ilgan).days // 365\n"
                    "print(f'Yoshingiz: {yosh}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=eirjjyP2qcQ",
            },
            {
                "title": "Amaliy Loyiha: Sonlar O'yini",
                "order": 8,
                "content": (
                    "=== Sonni Topish O'yini ===\n"
                    "Kompyuter 1-100 orasida son tanlaydi, siz topishingiz kerak.\n\n"
                    "import random\n\n"
                    "def sonlar_oyini():\n"
                    "    maxfiy = random.randint(1, 100)\n"
                    "    urinishlar = 0\n"
                    "    max_urinish = 7\n\n"
                    "    print('=== Sonni Toping ===')\n"
                    "    print(f'1 dan 100 gacha son o\\'yladim.')\n"
                    "    print(f'Sizda {max_urinish} ta urinish bor!')\n\n"
                    "    while urinishlar < max_urinish:\n"
                    "        try:\n"
                    "            tahmin = int(input(f'Urinish {urinishlar+1}: '))\n"
                    "        except ValueError:\n"
                    "            print('Faqat son kiriting!')\n"
                    "            continue\n\n"
                    "        urinishlar += 1\n\n"
                    "        if tahmin == maxfiy:\n"
                    "            print(f'Tabriklaymiz! {urinishlar} ta urinishda topdingiz!')\n"
                    "            return True\n"
                    "        elif tahmin < maxfiy:\n"
                    "            qolgan = max_urinish - urinishlar\n"
                    "            print(f'Kattaroq! {qolgan} urinish qoldi.')\n"
                    "        else:\n"
                    "            qolgan = max_urinish - urinishlar\n"
                    "            print(f'Kichikroq! {qolgan} urinish qoldi.')\n\n"
                    "    print(f'Yutqazdingiz! Son {maxfiy} edi.')\n"
                    "    return False\n\n"
                    "# O'yinni ishga tushirish:\n"
                    "sonlar_oyini()"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Funksiya yaratish uchun qaysi kalit so'z ishlatiladi?",
                 "answers": ["function", "def", "func", "create"], "correct": 1},
                {"text": "return kalit so'zi nima qiladi?",
                 "answers": ["Funksiyani to'xtatadi", "Qiymat qaytaradi", "Xatolik beradi", "Sikl boshlaydi"], "correct": 1},
                {"text": "import math buyrug'i nima qiladi?",
                 "answers": ["Yangi funksiya yaratadi", "math modulini ulaydi", "Matematik amal bajaradi", "O'zgaruvchi yaratadi"], "correct": 1},
                {"text": "Lambda funksiya nima?",
                 "answers": ["Ko'p qatorli funksiya", "Anonim bir qatorli funksiya", "Rekursiv funksiya", "Modul"], "correct": 1},
                {"text": "Rekursiya nima?",
                 "answers": ["Funksiya ichida sikl", "Funksiyaning o'zini chaqirishi", "Moduldan import", "Qaytarish qiymati"], "correct": 1},
            ]
        }
    },
    {
        "title": "Ma'lumotlar Tuzilmalari",
        "description": (
            "Python'ning asosiy ma'lumotlar tuzilmalari: list, tuple, set, dictionary. "
            "Ularni yaratish, o'zgartirish, qidirish va saralash. "
            "List comprehension, dictionary comprehension va generator iboralar."
        ),
        "price": 59000,
        "level": "Beginner",
        "lessons": [
            {
                "title": "Listlar (List) — asoslari",
                "order": 1,
                "content": (
                    "=== List nima? ===\n"
                    "Tartibli va o'zgartirilishi mumkin bo'lgan kolleksiya.\n\n"
                    "=== List yaratish ===\n"
                    "bo_sh = []\n"
                    "sonlar = [1, 2, 3, 4, 5]\n"
                    "aralash = [1, 'salom', 3.14, True]\n"
                    "ichma_ich = [[1, 2], [3, 4], [5, 6]]\n\n"
                    "=== Elementlarga murojaat ===\n"
                    "mevalar = ['olma', 'banan', 'gilos', 'limon']\n"
                    "print(mevalar[0])   # 'olma' (birinchi)\n"
                    "print(mevalar[-1])  # 'limon' (oxirgi)\n"
                    "print(mevalar[1])   # 'banan'\n\n"
                    "=== Slicing (kesim) ===\n"
                    "print(mevalar[1:3])   # ['banan', 'gilos']\n"
                    "print(mevalar[:2])    # ['olma', 'banan']\n"
                    "print(mevalar[2:])    # ['gilos', 'limon']\n"
                    "print(mevalar[::2])   # ['olma', 'gilos'] (har 2-chi)\n"
                    "print(mevalar[::-1])  # teskari tartib\n\n"
                    "=== Uzunlik va tekshirish ===\n"
                    "print(len(mevalar))        # 4\n"
                    "print('olma' in mevalar)   # True\n"
                    "print('nok' in mevalar)    # False\n\n"
                    "=== O'zgartirish ===\n"
                    "mevalar[0] = 'anor'\n"
                    "print(mevalar)  # ['anor', 'banan', 'gilos', 'limon']"
                ),
                "video_url": "https://www.youtube.com/watch?v=W8KRzm-HUcc",
            },
            {
                "title": "List Metodlari",
                "order": 2,
                "content": (
                    "=== Qo'shish ===\n"
                    "lst = [1, 2, 3]\n"
                    "lst.append(4)        # oxiriga: [1,2,3,4]\n"
                    "lst.insert(0, 0)     # boshiga: [0,1,2,3,4]\n"
                    "lst.extend([5, 6])   # kengaytirish: [0,1,2,3,4,5,6]\n\n"
                    "=== O'chirish ===\n"
                    "lst = [1, 2, 3, 2, 4]\n"
                    "lst.remove(2)    # birinchi 2 ni o'chiradi: [1,3,2,4]\n"
                    "chiqarildi = lst.pop()   # oxirgisini: 4\n"
                    "chiqarildi = lst.pop(0)  # 0-indeksni: 1\n"
                    "lst.clear()      # hammasini tozalash: []\n\n"
                    "=== Qidirish ===\n"
                    "lst = [10, 20, 30, 20]\n"
                    "print(lst.index(20))   # 1 (birinchi o'rni)\n"
                    "print(lst.count(20))   # 2 (necha marta)\n\n"
                    "=== Saralash ===\n"
                    "sonlar = [3, 1, 4, 1, 5, 9, 2, 6]\n"
                    "sonlar.sort()               # o'zi o'zgaradi: [1,1,2,3,4,5,6,9]\n"
                    "sonlar.sort(reverse=True)   # teskari: [9,6,5,4,3,2,1,1]\n\n"
                    "yangi = sorted([3,1,2])     # yangi list qaytaradi\n\n"
                    "=== Boshqa ===\n"
                    "lst = [1, 2, 3]\n"
                    "lst.reverse()    # teskari aylantirish: [3,2,1]\n"
                    "nusxa = lst.copy()   # nusxa olish\n"
                    "lst2 = lst[:]        # ham nusxa\n\n"
                    "=== + va * operatorlari ===\n"
                    "a = [1, 2]\n"
                    "b = [3, 4]\n"
                    "print(a + b)      # [1, 2, 3, 4]\n"
                    "print(a * 3)      # [1, 2, 1, 2, 1, 2]"
                ),
                "video_url": "https://www.youtube.com/watch?v=W8KRzm-HUcc",
            },
            {
                "title": "Tuplar (Tuple)",
                "order": 3,
                "content": (
                    "=== Tuple nima? ===\n"
                    "O'zgartirilmaydigan (immutable) tartibli kolleksiya.\n\n"
                    "=== Yaratish ===\n"
                    "bo_sh = ()\n"
                    "bitta = (1,)          # bitta element - vergul kerak!\n"
                    "koordinat = (10, 20)\n"
                    "aralash = (1, 'salom', 3.14)\n\n"
                    "=== List vs Tuple ===\n"
                    "# List - o'zgaradi [mutable]\n"
                    "# Tuple - o'zgarmaydi [immutable]\n"
                    "lst = [1, 2, 3]\n"
                    "lst[0] = 99    # Ishlaydi!\n\n"
                    "tpl = (1, 2, 3)\n"
                    "# tpl[0] = 99  # TypeError!\n\n"
                    "=== Elementlarga murojaat ===\n"
                    "ranglar = ('qizil', 'yashil', 'ko\\'k')\n"
                    "print(ranglar[0])    # 'qizil'\n"
                    "print(ranglar[-1])   # 'ko\\'k'\n"
                    "print(len(ranglar))  # 3\n\n"
                    "=== Unpacking (yoyish) ===\n"
                    "x, y = (10, 20)\n"
                    "a, b, c = (1, 2, 3)\n"
                    "birinchi, *qolganlari = (1, 2, 3, 4, 5)\n"
                    "print(birinchi)    # 1\n"
                    "print(qolganlari)  # [2, 3, 4, 5]\n\n"
                    "=== Tuple afzalliklari ===\n"
                    "# 1. Tezroq (list dan)\n"
                    "# 2. Xavfsizroq (o'zgarmasligi)\n"
                    "# 3. Dictionary kaliti bo'la oladi\n"
                    "d = {(0,0): 'marraz', (1,0): 'o\\'ng'}\n\n"
                    "=== named tuple ===\n"
                    "from collections import namedtuple\n"
                    "Nuqta = namedtuple('Nuqta', ['x', 'y'])\n"
                    "n = Nuqta(3, 4)\n"
                    "print(n.x, n.y)  # 3 4"
                ),
                "video_url": "https://www.youtube.com/watch?v=NI26dqhs2Rk",
            },
            {
                "title": "To'plamlar (Set)",
                "order": 4,
                "content": (
                    "=== Set nima? ===\n"
                    "Noyob elementlar to'plami (tartibi yo'q, takror yo'q).\n\n"
                    "=== Yaratish ===\n"
                    "bo_sh = set()           # {} emas!\n"
                    "sonlar = {1, 2, 3, 4, 5}\n"
                    "takrorli = {1, 1, 2, 2, 3}  # {1, 2, 3}\n"
                    "listdan = set([1, 2, 2, 3])  # {1, 2, 3}\n\n"
                    "=== Elementlar qo'shish va o'chirish ===\n"
                    "s = {1, 2, 3}\n"
                    "s.add(4)       # {1, 2, 3, 4}\n"
                    "s.discard(2)   # {1, 3, 4} (topilmasa xato yo'q)\n"
                    "s.remove(3)    # {1, 4} (topilmasa KeyError)\n\n"
                    "=== To'plam amallari ===\n"
                    "a = {1, 2, 3, 4}\n"
                    "b = {3, 4, 5, 6}\n\n"
                    "print(a | b)   # {1,2,3,4,5,6} birlashma\n"
                    "print(a & b)   # {3,4} kesishma\n"
                    "print(a - b)   # {1,2} farq (a da bor, b da yo'q)\n"
                    "print(a ^ b)   # {1,2,5,6} simmetrik farq\n\n"
                    "=== Tekshirish ===\n"
                    "print(3 in a)      # True\n"
                    "print(a.issubset({1,2,3,4,5}))   # True\n"
                    "print(a.issuperset({1,2}))        # True\n\n"
                    "=== Amaliy misol: takrorlarsiz ===\n"
                    "so_zlar = ['olma', 'banan', 'olma', 'gilos', 'banan']\n"
                    "noyob = set(so_zlar)\n"
                    "print(noyob)  # {'olma', 'banan', 'gilos'}"
                ),
                "video_url": "https://www.youtube.com/watch?v=W8KRzm-HUcc",
            },
            {
                "title": "Lug'atlar (Dictionary)",
                "order": 5,
                "content": (
                    "=== Dictionary nima? ===\n"
                    "Kalit-qiymat (key-value) juftliklari to'plami.\n\n"
                    "=== Yaratish ===\n"
                    "bo_sh = {}\n"
                    "talaba = {'ism': 'Ali', 'yosh': 20, 'ball': 95}\n"
                    "narxlar = dict(olma=5000, banan=8000, gilos=15000)\n\n"
                    "=== Elementlarga murojaat ===\n"
                    "print(talaba['ism'])           # 'Ali'\n"
                    "print(talaba.get('yosh'))      # 20\n"
                    "print(talaba.get('ota', 'N/A'))  # 'N/A' (yo'q bo'lsa)\n\n"
                    "=== Qo'shish va o'zgartirish ===\n"
                    "talaba['shahar'] = 'Toshkent'  # yangi kalit\n"
                    "talaba['yosh'] = 21            # o'zgartirish\n"
                    "talaba.update({'sinf': '11A', 'ball': 98})\n\n"
                    "=== O'chirish ===\n"
                    "del talaba['ball']          # kalit o'chirish\n"
                    "chiqdi = talaba.pop('yosh') # o'chirib qaytarish\n\n"
                    "=== Iteratsiya ===\n"
                    "for kalit in talaba:\n"
                    "    print(kalit)            # faqat kalitlar\n\n"
                    "for kalit, qiymat in talaba.items():\n"
                    "    print(f'{kalit}: {qiymat}')\n\n"
                    "print(talaba.keys())    # dict_keys([...])\n"
                    "print(talaba.values())  # dict_values([...])\n"
                    "print(talaba.items())   # dict_items([...])\n\n"
                    "=== Tekshirish ===\n"
                    "print('ism' in talaba)   # True\n"
                    "print(len(talaba))       # elementlar soni"
                ),
                "video_url": "https://www.youtube.com/watch?v=daefaLgNkw0",
            },
            {
                "title": "List Comprehension",
                "order": 6,
                "content": (
                    "=== List Comprehension nima? ===\n"
                    "List yaratishning qisqa va samarali usuli.\n\n"
                    "=== Asosiy shakl ===\n"
                    "# [ifoda for element in ketma-ketlik]\n\n"
                    "=== Oddiy misol ===\n"
                    "# For sikli bilan:\n"
                    "kvadratlar = []\n"
                    "for x in range(1, 6):\n"
                    "    kvadratlar.append(x**2)\n\n"
                    "# List comprehension bilan:\n"
                    "kvadratlar = [x**2 for x in range(1, 6)]\n"
                    "print(kvadratlar)  # [1, 4, 9, 16, 25]\n\n"
                    "=== Shartli LC ===\n"
                    "# [ifoda for element in ketma-ketlik if shart]\n"
                    "juftlar = [x for x in range(20) if x % 2 == 0]\n"
                    "print(juftlar)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]\n\n"
                    "=== String LC ===\n"
                    "so_zlar = ['Python', 'Django', 'Flask', 'FastAPI']\n"
                    "uzun = [s for s in so_zlar if len(s) > 5]\n"
                    "print(uzun)  # ['Python', 'Django', 'FastAPI']\n\n"
                    "katta = [s.upper() for s in so_zlar]\n"
                    "print(katta)  # ['PYTHON', 'DJANGO', 'FLASK', 'FASTAPI']\n\n"
                    "=== Ichma-ich LC ===\n"
                    "matritsa = [[i*j for j in range(1,4)] for i in range(1,4)]\n"
                    "# [[1,2,3],[2,4,6],[3,6,9]]\n\n"
                    "=== Ternary bilan ===\n"
                    "sonlar = range(-5, 6)\n"
                    "natijalar = ['musbat' if x > 0 else 'manfiy' if x < 0 else 'nol'\n"
                    "             for x in sonlar]\n"
                    "print(natijalar)"
                ),
                "video_url": "https://www.youtube.com/watch?v=3dt4OGnU5sM",
            },
            {
                "title": "Dictionary Comprehension",
                "order": 7,
                "content": (
                    "=== Dictionary Comprehension ===\n"
                    "# {kalit: qiymat for element in ketma-ketlik}\n\n"
                    "=== Asosiy misol ===\n"
                    "kvadratlar = {x: x**2 for x in range(1, 6)}\n"
                    "print(kvadratlar)\n"
                    "# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}\n\n"
                    "=== List dan dict ===\n"
                    "ismlar = ['Ali', 'Sarvar', 'Kamol']\n"
                    "uzunliklar = {ism: len(ism) for ism in ismlar}\n"
                    "print(uzunliklar)\n"
                    "# {'Ali': 3, 'Sarvar': 6, 'Kamol': 5}\n\n"
                    "=== Shartli dict comprehension ===\n"
                    "sonlar = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}\n"
                    "juft_qiymatlar = {k: v for k, v in sonlar.items() if v % 2 == 0}\n"
                    "print(juft_qiymatlar)  # {'b': 2, 'd': 4}\n\n"
                    "=== Kalit va qiymatni almashtirish ===\n"
                    "asl = {'a': 1, 'b': 2, 'c': 3}\n"
                    "teskari = {v: k for k, v in asl.items()}\n"
                    "print(teskari)  # {1: 'a', 2: 'b', 3: 'c'}\n\n"
                    "=== Set comprehension ===\n"
                    "sonlar = [1, 2, 2, 3, 3, 4]\n"
                    "noyob = {x**2 for x in sonlar}\n"
                    "print(noyob)  # {1, 4, 9, 16}"
                ),
                "video_url": "https://www.youtube.com/watch?v=3dt4OGnU5sM",
            },
            {
                "title": "Amaliy Loyiha: Talabalar Jurnali",
                "order": 8,
                "content": (
                    "=== Talabalar Jurnali Loyihasi ===\n"
                    "Dictionary va list yordamida talabalar ma'lumotlarini boshqarish.\n\n"
                    "journal = {}  # {ism: [ballar]}\n\n"
                    "def talaba_qo_sh(ism):\n"
                    "    if ism not in journal:\n"
                    "        journal[ism] = []\n"
                    "        print(f'{ism} qo\\'shildi.')\n"
                    "    else:\n"
                    "        print(f'{ism} allaqachon bor.')\n\n"
                    "def ball_qo_sh(ism, ball):\n"
                    "    if ism in journal:\n"
                    "        journal[ism].append(ball)\n"
                    "        print(f'{ism}: {ball} ball qo\\'shildi.')\n"
                    "    else:\n"
                    "        print(f'{ism} topilmadi!')\n\n"
                    "def o_rtacha_ball(ism):\n"
                    "    if ism in journal and journal[ism]:\n"
                    "        return sum(journal[ism]) / len(journal[ism])\n"
                    "    return 0\n\n"
                    "def hisobot():\n"
                    "    print('\\n=== Talabalar Jurnali ===')\n"
                    "    for ism, ballar in journal.items():\n"
                    "        ort = o_rtacha_ball(ism)\n"
                    "        baho = 'A' if ort >= 90 else 'B' if ort >= 75 else 'C'\n"
                    "        print(f'{ism}: {ballar} | O\\'rtacha: {ort:.1f} | Baho: {baho}')\n\n"
                    "# Test qilish:\n"
                    "talaba_qo_sh('Ali')\n"
                    "talaba_qo_sh('Sarvar')\n"
                    "ball_qo_sh('Ali', 95)\n"
                    "ball_qo_sh('Ali', 87)\n"
                    "ball_qo_sh('Sarvar', 78)\n"
                    "hisobot()"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "List yaratish uchun qaysi qavslar ishlatiladi?",
                 "answers": ["()", "{}", "[]", "<>"], "correct": 2},
                {"text": "Dictionary (lug'at) nima saqlaydi?",
                 "answers": ["Faqat sonlar", "Kalit-qiymat juftliklari", "Faqat matnlar", "Faqat listlar"], "correct": 1},
                {"text": "Set nima?",
                 "answers": ["Tartiblangan ketma-ketlik", "Noyob elementlar to'plami", "O'zgartirilmaydigan list", "Lug'at turi"], "correct": 1},
                {"text": "list.append() nima qiladi?",
                 "answers": ["Elementni o'chiradi", "Listni tozalaydi", "Oxiriga element qo'shadi", "Saralaydi"], "correct": 2},
                {"text": "[x*2 for x in range(5)] nima?",
                 "answers": ["Funksiya", "List comprehension", "Generator", "Lambda"], "correct": 1},
            ]
        }
    },
    {
        "title": "OOP - Obyektga Yo'naltirilgan Dasturlash",
        "description": (
            "Klasslar va obyektlar, konstruktor (__init__), instance/class metodlar, "
            "inkapsulyatsiya, meros olish (inheritance), polimorfizm va "
            "mavhum klasslar. Real dasturlash loyihalarida OOP qo'llash."
        ),
        "price": 99000,
        "level": "Professional",
        "lessons": [
            {
                "title": "Klass va Obyekt Tushunchasi",
                "order": 1,
                "content": (
                    "=== OOP nima? ===\n"
                    "Obyektga yo'naltirilgan dasturlash - real dunyo narsalarini kod bilan modellash.\n\n"
                    "=== Klass - shablon ===\n"
                    "class Mashina:\n"
                    "    rang = 'oq'          # klass atributi\n\n"
                    "    def yugur(self):\n"
                    "        print('Mashina yurayapti!')\n\n"
                    "=== Obyekt - nusxa ===\n"
                    "mening_mashinam = Mashina()    # obyekt yaratish\n"
                    "uning_mashinasi = Mashina()    # yana bir obyekt\n\n"
                    "mening_mashinam.yugur()  # Mashina yurayapti!\n\n"
                    "=== Atributlar ===\n"
                    "mening_mashinam.rang = 'qizil'  # instance atribut\n"
                    "print(mening_mashinam.rang)      # 'qizil'\n"
                    "print(uning_mashinasi.rang)      # 'oq' (klass atribut)\n\n"
                    "=== OOP 4 tamoyili ===\n"
                    "# 1. Inkapsulyatsiya - ma'lumotni yashirish\n"
                    "# 2. Meros olish - klassdan meros\n"
                    "# 3. Polimorfizm - turli xil xatti-harakat\n"
                    "# 4. Abstraksiya - muhimini ko'rsatish"
                ),
                "video_url": "https://www.youtube.com/watch?v=JeznW_7DlB0",
            },
            {
                "title": "__init__ Konstruktor va self",
                "order": 2,
                "content": (
                    "=== __init__ nima? ===\n"
                    "Obyekt yaratilganda avtomatik chaqiriladigan metod.\n\n"
                    "=== Asosiy sintaksis ===\n"
                    "class Talaba:\n"
                    "    def __init__(self, ism, yosh, ball):\n"
                    "        self.ism = ism\n"
                    "        self.yosh = yosh\n"
                    "        self.ball = ball\n\n"
                    "    def tanishtir(self):\n"
                    "        print(f'Ism: {self.ism}, Yosh: {self.yosh}')\n\n"
                    "=== Obyekt yaratish ===\n"
                    "t1 = Talaba('Ali', 20, 95)\n"
                    "t2 = Talaba('Sarvar', 22, 85)\n\n"
                    "t1.tanishtir()  # Ism: Ali, Yosh: 20\n"
                    "print(t2.ball)  # 85\n\n"
                    "=== self nima? ===\n"
                    "# self - joriy obyektga havola\n"
                    "# Har bir metod birinchi parametr sifatida self oladi\n"
                    "# Python uni avtomatik uzatadi\n\n"
                    "class Hisoblagich:\n"
                    "    def __init__(self, boshlang_ich=0):\n"
                    "        self.qiymat = boshlang_ich\n\n"
                    "    def oshir(self, miqdor=1):\n"
                    "        self.qiymat += miqdor\n\n"
                    "    def ko_rsat(self):\n"
                    "        print(f'Qiymat: {self.qiymat}')\n\n"
                    "h = Hisoblagich(10)\n"
                    "h.oshir(5)\n"
                    "h.ko_rsat()  # Qiymat: 15"
                ),
                "video_url": "https://www.youtube.com/watch?v=apACNr7DC_s",
            },
            {
                "title": "Instance, Class va Static Metodlar",
                "order": 3,
                "content": (
                    "=== 1. Instance Metod ===\n"
                    "# self parametri bor, obyekt bilan ishlaydi\n"
                    "class Krug:\n"
                    "    def __init__(self, radius):\n"
                    "        self.radius = radius\n\n"
                    "    def yuza(self):\n"
                    "        import math\n"
                    "        return math.pi * self.radius ** 2\n\n"
                    "k = Krug(5)\n"
                    "print(k.yuza())   # 78.53...\n\n"
                    "=== 2. Class Metod ===\n"
                    "# @classmethod - klass bilan ishlaydi\n"
                    "class Talaba:\n"
                    "    soni = 0\n\n"
                    "    def __init__(self, ism):\n"
                    "        self.ism = ism\n"
                    "        Talaba.soni += 1\n\n"
                    "    @classmethod\n"
                    "    def necha_talaba(cls):\n"
                    "        return f'Talabalar soni: {cls.soni}'\n\n"
                    "Talaba('Ali')\n"
                    "Talaba('Sarvar')\n"
                    "print(Talaba.necha_talaba())  # Talabalar soni: 2\n\n"
                    "=== 3. Static Metod ===\n"
                    "# @staticmethod - mustaqil, self yoki cls yo'q\n"
                    "class Matematik:\n"
                    "    @staticmethod\n"
                    "    def juftmi(n):\n"
                    "        return n % 2 == 0\n\n"
                    "    @staticmethod\n"
                    "    def absolyut(n):\n"
                    "        return n if n >= 0 else -n\n\n"
                    "print(Matematik.juftmi(4))     # True\n"
                    "print(Matematik.absolyut(-7))  # 7"
                ),
                "video_url": "https://www.youtube.com/watch?v=PIKiHq1O9vk",
            },
            {
                "title": "Inkapsulyatsiya va Property",
                "order": 4,
                "content": (
                    "=== Inkapsulyatsiya ===\n"
                    "Ma'lumotni yashirish va nazorat qilish.\n\n"
                    "=== Xususiy atributlar ===\n"
                    "class BankHisob:\n"
                    "    def __init__(self, egasi, balans):\n"
                    "        self.egasi = egasi\n"
                    "        self.__balans = balans  # __ = xususiy\n\n"
                    "    def balans_ko_rsat(self):\n"
                    "        return self.__balans\n\n"
                    "    def pul_qo_sh(self, miqdor):\n"
                    "        if miqdor > 0:\n"
                    "            self.__balans += miqdor\n\n"
                    "hisob = BankHisob('Ali', 1000000)\n"
                    "# print(hisob.__balans)  # AttributeError!\n"
                    "print(hisob.balans_ko_rsat())  # 1000000\n\n"
                    "=== @property ===\n"
                    "class Doira:\n"
                    "    def __init__(self, radius):\n"
                    "        self.__radius = radius\n\n"
                    "    @property\n"
                    "    def radius(self):\n"
                    "        return self.__radius\n\n"
                    "    @radius.setter\n"
                    "    def radius(self, qiymat):\n"
                    "        if qiymat < 0:\n"
                    "            raise ValueError('Radius manfiy bolaolmaydi!')\n"
                    "        self.__radius = qiymat\n\n"
                    "    @property\n"
                    "    def yuza(self):\n"
                    "        import math\n"
                    "        return math.pi * self.__radius ** 2\n\n"
                    "d = Doira(5)\n"
                    "print(d.radius)  # 5\n"
                    "print(d.yuza)    # 78.53...\n"
                    "d.radius = 10    # setter chaqiriladi"
                ),
                "video_url": "https://www.youtube.com/watch?v=jCzT9XFZ5bw",
            },
            {
                "title": "Meros Olish (Inheritance)",
                "order": 5,
                "content": (
                    "=== Meros olish ===\n"
                    "Mavjud klassdan yangi klass yaratish.\n\n"
                    "=== Asosiy meros ===\n"
                    "class Hayvon:\n"
                    "    def __init__(self, ism, yoshi):\n"
                    "        self.ism = ism\n"
                    "        self.yoshi = yoshi\n\n"
                    "    def ovqatlan(self):\n"
                    "        print(f'{self.ism} ovqatlanmoqda')\n\n"
                    "class It(Hayvon):  # Hayvondan meros\n"
                    "    def __init__(self, ism, yoshi, zoti):\n"
                    "        super().__init__(ism, yoshi)  # ota konstruktor\n"
                    "        self.zoti = zoti\n\n"
                    "    def vov_de(self):\n"
                    "        print(f'{self.ism}: Vov-vov!')\n\n"
                    "it = It('Sharik', 3, 'Labrador')\n"
                    "it.ovqatlan()  # Hayvondan meros: Sharik ovqatlanmoqda\n"
                    "it.vov_de()    # O'zining: Sharik: Vov-vov!\n\n"
                    "=== Ko'p meros ===\n"
                    "class A:\n"
                    "    def salom(self):\n"
                    "        return 'A dan salom'\n\n"
                    "class B:\n"
                    "    def xayr(self):\n"
                    "        return 'B dan xayr'\n\n"
                    "class C(A, B):\n"
                    "    pass\n\n"
                    "c = C()\n"
                    "print(c.salom())  # A dan salom\n"
                    "print(c.xayr())   # B dan xayr\n\n"
                    "=== isinstance va issubclass ===\n"
                    "print(isinstance(it, It))      # True\n"
                    "print(isinstance(it, Hayvon))  # True\n"
                    "print(issubclass(It, Hayvon))  # True"
                ),
                "video_url": "https://www.youtube.com/watch?v=Cn7AkDb4pIU",
            },
            {
                "title": "Polimorfizm va Method Overriding",
                "order": 6,
                "content": (
                    "=== Polimorfizm ===\n"
                    "Bir xil interfeys - turli xil xatti-harakat.\n\n"
                    "=== Method Overriding ===\n"
                    "class Shakl:\n"
                    "    def yuza(self):\n"
                    "        return 0\n\n"
                    "    def ta_rifla(self):\n"
                    "        print(f'Yuza: {self.yuza()}')\n\n"
                    "class Kvadrat(Shakl):\n"
                    "    def __init__(self, tomon):\n"
                    "        self.tomon = tomon\n\n"
                    "    def yuza(self):         # override!\n"
                    "        return self.tomon ** 2\n\n"
                    "class Doira(Shakl):\n"
                    "    def __init__(self, radius):\n"
                    "        self.radius = radius\n\n"
                    "    def yuza(self):         # override!\n"
                    "        import math\n"
                    "        return math.pi * self.radius ** 2\n\n"
                    "shakllar = [Kvadrat(4), Doira(3), Kvadrat(7)]\n"
                    "for sh in shakllar:\n"
                    "    sh.ta_rifla()  # har biri o'z yuza() ni chaqiradi\n\n"
                    "=== Duck Typing ===\n"
                    "# 'O'rdakdek yurib, o'rdakdek ovoz chiqarsa - o'rdak'\n"
                    "class Mushuk:\n"
                    "    def ovoz_chiqar(self): print('Miyov!')\n\n"
                    "class It:\n"
                    "    def ovoz_chiqar(self): print('Vov!')\n\n"
                    "class Qush:\n"
                    "    def ovoz_chiqar(self): print('Chiw!')\n\n"
                    "hayvonlar = [Mushuk(), It(), Qush()]\n"
                    "for h in hayvonlar:\n"
                    "    h.ovoz_chiqar()  # Miyov! Vov! Chiw!"
                ),
                "video_url": "https://www.youtube.com/watch?v=YSuEIL_e2xA",
            },
            {
                "title": "Sehrli Metodlar (Magic Methods)",
                "order": 7,
                "content": (
                    "=== Sehrli metodlar ===\n"
                    "__ bilan boshlanadigan va tugaydigan metodlar.\n\n"
                    "=== __str__ va __repr__ ===\n"
                    "class Talaba:\n"
                    "    def __init__(self, ism, ball):\n"
                    "        self.ism = ism\n"
                    "        self.ball = ball\n\n"
                    "    def __str__(self):\n"
                    "        return f'Talaba: {self.ism} ({self.ball})'\n\n"
                    "    def __repr__(self):\n"
                    "        return f'Talaba(ism={self.ism!r}, ball={self.ball})'\n\n"
                    "t = Talaba('Ali', 95)\n"
                    "print(t)      # Talaba: Ali (95)\n"
                    "print(repr(t)) # Talaba(ism='Ali', ball=95)\n\n"
                    "=== __len__ va __getitem__ ===\n"
                    "class Sinf:\n"
                    "    def __init__(self):\n"
                    "        self.talabalar = []\n\n"
                    "    def qo_sh(self, talaba):\n"
                    "        self.talabalar.append(talaba)\n\n"
                    "    def __len__(self):\n"
                    "        return len(self.talabalar)\n\n"
                    "    def __getitem__(self, index):\n"
                    "        return self.talabalar[index]\n\n"
                    "s = Sinf()\n"
                    "s.qo_sh('Ali')\n"
                    "s.qo_sh('Sarvar')\n"
                    "print(len(s))   # 2\n"
                    "print(s[0])     # Ali\n\n"
                    "=== __add__ va __eq__ ===\n"
                    "class Vektor:\n"
                    "    def __init__(self, x, y):\n"
                    "        self.x = x\n"
                    "        self.y = y\n\n"
                    "    def __add__(self, other):\n"
                    "        return Vektor(self.x + other.x, self.y + other.y)\n\n"
                    "    def __str__(self):\n"
                    "        return f'Vektor({self.x}, {self.y})'\n\n"
                    "v1 = Vektor(1, 2)\n"
                    "v2 = Vektor(3, 4)\n"
                    "print(v1 + v2)  # Vektor(4, 6)"
                ),
                "video_url": "https://www.youtube.com/watch?v=z1sZyQhBFPs",
            },
            {
                "title": "Amaliy Loyiha: Bank Tizimi",
                "order": 8,
                "content": (
                    "=== Bank Tizimi Loyihasi ===\n"
                    "OOP tamoyillari yordamida bank hisob tizimi.\n\n"
                    "class BankHisob:\n"
                    "    def __init__(self, hisob_raqam, egasi, balans=0):\n"
                    "        self.hisob_raqam = hisob_raqam\n"
                    "        self.egasi = egasi\n"
                    "        self.__balans = balans\n"
                    "        self.__tarix = []\n\n"
                    "    @property\n"
                    "    def balans(self):\n"
                    "        return self.__balans\n\n"
                    "    def kirim(self, miqdor):\n"
                    "        if miqdor <= 0:\n"
                    "            raise ValueError('Miqdor musbat bolishi kerak')\n"
                    "        self.__balans += miqdor\n"
                    "        self.__tarix.append(f'+{miqdor:,}')\n"
                    "        print(f'Kirim: {miqdor:,} som')\n\n"
                    "    def chiqim(self, miqdor):\n"
                    "        if miqdor > self.__balans:\n"
                    "            print('Mablag yetarli emas!')\n"
                    "            return\n"
                    "        self.__balans -= miqdor\n"
                    "        self.__tarix.append(f'-{miqdor:,}')\n"
                    "        print(f'Chiqim: {miqdor:,} som')\n\n"
                    "    def ko_chirma(self):\n"
                    "        print(f'Hisob: {self.hisob_raqam} | {self.egasi}')\n"
                    "        print(f'Balans: {self.__balans:,} som')\n"
                    "        print(f'Operatsiyalar: {self.__tarix}')\n\n"
                    "# Test:\n"
                    "h = BankHisob('UZB001', 'Ali Karimov', 1000000)\n"
                    "h.kirim(500000)\n"
                    "h.chiqim(200000)\n"
                    "h.ko_chirma()"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Klass nima?",
                 "answers": ["Funksiya turi", "Obyekt shabloni", "Ma'lumot turi", "Modul"], "correct": 1},
                {"text": "__init__ metodi nima uchun ishlatiladi?",
                 "answers": ["Klassni o'chirish", "Obyektni boshlash", "Meros olish", "Metodlarni chaqirish"], "correct": 1},
                {"text": "self kalit so'zi nimani bildiradi?",
                 "answers": ["Klassning o'zini", "Joriy obyektni", "Ota klassni", "Yangi obyektni"], "correct": 1},
                {"text": "Meros olish uchun Python sintaksisi qanday?",
                 "answers": ["class Bola extends Ota:", "class Bola(Ota):", "class Bola inherit Ota:", "class Bola: Ota"], "correct": 1},
                {"text": "Polimorfizm nima?",
                 "answers": ["Bir xil nomli metodlarning turli xatti-harakati", "Ko'p klassdan meros olish", "Maxfiy atributlar", "Abstract klass"], "correct": 0},
            ]
        }
    },
    {
        "title": "Fayl va Xatolarni Boshqarish",
        "description": (
            "Fayllar bilan ishlash: o'qish, yozish, qo'shib yozish. "
            "Xatolarni boshqarish: try/except/finally, Exception turlari, "
            "maxsus xatolar yaratish. JSON fayllari va context manager."
        ),
        "price": 69000,
        "level": "Professional",
        "lessons": [
            {
                "title": "Fayllarni Ochish va Yopish",
                "order": 1,
                "content": (
                    "=== Fayllar bilan ishlash ===\n"
                    "Python'da fayllarni o'qish, yozish va boshqarish.\n\n"
                    "=== open() funksiyasi ===\n"
                    "# open(fayl_nomi, rejim, encoding)\n"
                    "# Rejimlar:\n"
                    "# 'r' - o'qish (default)\n"
                    "# 'w' - yozish (mavjudni o'chiradi)\n"
                    "# 'a' - qo'shib yozish\n"
                    "# 'x' - yangi yaratish (mavjud bo'lsa xato)\n"
                    "# 'b' - binary rejim\n\n"
                    "=== with iborasi (tavsiya etiladi) ===\n"
                    "with open('test.txt', 'w', encoding='utf-8') as f:\n"
                    "    f.write('Salom, Dunyo!\\n')\n"
                    "    f.write('Python fayl bilan ishlash.')\n"
                    "# with bloki tugagach fayl avtomatik yopiladi\n\n"
                    "=== close() bilan (eskirgan usul) ===\n"
                    "f = open('test.txt', 'r', encoding='utf-8')\n"
                    "mazmun = f.read()\n"
                    "f.close()  # unutmaslik kerak!\n\n"
                    "=== Fayl mavjudligini tekshirish ===\n"
                    "import os\n"
                    "if os.path.exists('test.txt'):\n"
                    "    print('Fayl mavjud')\n"
                    "print(os.path.getsize('test.txt'))  # bayt"
                ),
                "video_url": "https://www.youtube.com/watch?v=Uh2ebFW8OYM",
            },
            {
                "title": "Fayldan O'qish",
                "order": 2,
                "content": (
                    "=== O'qish metodlari ===\n\n"
                    "=== read() - hammasini o'qish ===\n"
                    "with open('test.txt', 'r', encoding='utf-8') as f:\n"
                    "    mazmun = f.read()\n"
                    "    print(mazmun)\n\n"
                    "# Faqat N ta belgi o'qish:\n"
                    "with open('test.txt', 'r') as f:\n"
                    "    birinchi_10 = f.read(10)\n\n"
                    "=== readline() - bir qator ===\n"
                    "with open('test.txt', 'r', encoding='utf-8') as f:\n"
                    "    birinchi = f.readline()  # birinchi qator\n"
                    "    ikkinchi = f.readline()  # ikkinchi qator\n\n"
                    "=== readlines() - qatorlar ro'yxati ===\n"
                    "with open('test.txt', 'r', encoding='utf-8') as f:\n"
                    "    qatorlar = f.readlines()\n"
                    "for i, qator in enumerate(qatorlar):\n"
                    "    print(f'{i+1}: {qator.strip()}')\n\n"
                    "=== for sikli bilan (samarali) ===\n"
                    "with open('test.txt', 'r', encoding='utf-8') as f:\n"
                    "    for qator in f:   # xotiraga samarali\n"
                    "        print(qator.strip())"
                ),
                "video_url": "https://www.youtube.com/watch?v=Uh2ebFW8OYM",
            },
            {
                "title": "Faylga Yozish",
                "order": 3,
                "content": (
                    "=== Faylga yozish ===\n\n"
                    "=== write() - matn yozish ===\n"
                    "with open('natija.txt', 'w', encoding='utf-8') as f:\n"
                    "    f.write('Birinchi qator\\n')\n"
                    "    f.write('Ikkinchi qator\\n')\n\n"
                    "=== writelines() - ro'yxat yozish ===\n"
                    "qatorlar = ['Bir\\n', 'Ikki\\n', 'Uch\\n']\n"
                    "with open('sonlar.txt', 'w', encoding='utf-8') as f:\n"
                    "    f.writelines(qatorlar)\n\n"
                    "=== 'a' (append) rejimi ===\n"
                    "with open('log.txt', 'a', encoding='utf-8') as f:\n"
                    "    f.write('Yangi yozuv qo\\'shildi\\n')  # Mavjudga qo'shadi\n\n"
                    "=== print() bilan yozish ===\n"
                    "with open('chiqish.txt', 'w', encoding='utf-8') as f:\n"
                    "    print('Bu print bilan yozildi', file=f)\n"
                    "    print(42, file=f)\n\n"
                    "=== CSV fayl yozish ===\n"
                    "import csv\n"
                    "talabalar = [['Ali', 95], ['Sarvar', 88], ['Kamol', 72]]\n"
                    "with open('talabalar.csv', 'w', newline='', encoding='utf-8') as f:\n"
                    "    yozuvchi = csv.writer(f)\n"
                    "    yozuvchi.writerow(['Ism', 'Ball'])\n"
                    "    yozuvchi.writerows(talabalar)"
                ),
                "video_url": "https://www.youtube.com/watch?v=Uh2ebFW8OYM",
            },
            {
                "title": "JSON Fayllari",
                "order": 4,
                "content": (
                    "=== JSON nima? ===\n"
                    "JavaScript Object Notation - ma'lumotlarni saqlash formati.\n\n"
                    "=== json moduli ===\n"
                    "import json\n\n"
                    "=== Python -> JSON (dump/dumps) ===\n"
                    "ma_lumot = {\n"
                    "    'ism': 'Ali',\n"
                    "    'yosh': 20,\n"
                    "    'fanlar': ['Matematika', 'Python'],\n"
                    "    'aktiv': True\n"
                    "}\n\n"
                    "# Faylga yozish\n"
                    "with open('talaba.json', 'w', encoding='utf-8') as f:\n"
                    "    json.dump(ma_lumot, f, ensure_ascii=False, indent=4)\n\n"
                    "# Stringga aylantirish\n"
                    "json_str = json.dumps(ma_lumot, ensure_ascii=False, indent=2)\n"
                    "print(json_str)\n\n"
                    "=== JSON -> Python (load/loads) ===\n"
                    "# Fayldan o'qish\n"
                    "with open('talaba.json', 'r', encoding='utf-8') as f:\n"
                    "    yuklangan = json.load(f)\n"
                    "print(yuklangan['ism'])  # Ali\n\n"
                    "# Stringdan o'qish\n"
                    "json_str = '{\"x\": 1, \"y\": 2}'\n"
                    "obj = json.loads(json_str)\n"
                    "print(obj['x'])  # 1\n\n"
                    "=== JSON turlari ===\n"
                    "# Python dict  <-> JSON object  {}\n"
                    "# Python list  <-> JSON array   []\n"
                    "# Python str   <-> JSON string  ''\n"
                    "# Python int   <-> JSON number\n"
                    "# Python True  <-> JSON true\n"
                    "# Python None  <-> JSON null"
                ),
                "video_url": "https://www.youtube.com/watch?v=9N6a-VLBa2I",
            },
            {
                "title": "Try/Except/Finally Bloki",
                "order": 5,
                "content": (
                    "=== Xatolarni boshqarish ===\n\n"
                    "=== Asosiy try/except ===\n"
                    "try:\n"
                    "    son = int(input('Son kiriting: '))\n"
                    "    natija = 10 / son\n"
                    "    print(f'Natija: {natija}')\n"
                    "except ValueError:\n"
                    "    print('Xato: Iltimos son kiriting!')\n"
                    "except ZeroDivisionError:\n"
                    "    print('Xato: 0 ga bolish mumkin emas!')\n\n"
                    "=== except Exception as e ===\n"
                    "try:\n"
                    "    fayl = open('yoq.txt')\n"
                    "except Exception as e:\n"
                    "    print(f'Xato turi: {type(e).__name__}')\n"
                    "    print(f'Xato xabari: {e}')\n\n"
                    "=== else bloki ===\n"
                    "try:\n"
                    "    son = int('42')\n"
                    "except ValueError:\n"
                    "    print('Konvertatsiya xatosi')\n"
                    "else:\n"
                    "    print(f'Muvaffaqiyat: {son}')  # Faqat xato bo'lmasa\n\n"
                    "=== finally bloki ===\n"
                    "f = None\n"
                    "try:\n"
                    "    f = open('data.txt')\n"
                    "    mazmun = f.read()\n"
                    "except FileNotFoundError:\n"
                    "    print('Fayl topilmadi')\n"
                    "finally:\n"
                    "    if f:\n"
                    "        f.close()  # Har doim ishlaydi!\n"
                    "    print('Operatsiya tugadi')"
                ),
                "video_url": "https://www.youtube.com/watch?v=NIWwJbo-9_8",
            },
            {
                "title": "Exception Turlari va Hierarchy",
                "order": 6,
                "content": (
                    "=== Asosiy exception turlari ===\n\n"
                    "=== ValueError ===\n"
                    "try:\n"
                    "    x = int('salom')  # son emas\n"
                    "except ValueError as e:\n"
                    "    print(f'ValueError: {e}')\n\n"
                    "=== TypeError ===\n"
                    "try:\n"
                    "    x = '5' + 3  # tur mos emas\n"
                    "except TypeError as e:\n"
                    "    print(f'TypeError: {e}')\n\n"
                    "=== IndexError ===\n"
                    "try:\n"
                    "    lst = [1, 2, 3]\n"
                    "    print(lst[10])  # indeks yo'q\n"
                    "except IndexError as e:\n"
                    "    print(f'IndexError: {e}')\n\n"
                    "=== KeyError ===\n"
                    "try:\n"
                    "    d = {'a': 1}\n"
                    "    print(d['b'])  # kalit yo'q\n"
                    "except KeyError as e:\n"
                    "    print(f'KeyError: {e}')\n\n"
                    "=== FileNotFoundError ===\n"
                    "try:\n"
                    "    with open('yoq.txt') as f:\n"
                    "        f.read()\n"
                    "except FileNotFoundError as e:\n"
                    "    print(f'Fayl topilmadi: {e}')\n\n"
                    "=== ZeroDivisionError ===\n"
                    "try:\n"
                    "    x = 1 / 0\n"
                    "except ZeroDivisionError:\n"
                    "    print('0 ga bolish mumkin emas')"
                ),
                "video_url": "https://www.youtube.com/watch?v=ZsvftkbbrR0",
            },
            {
                "title": "Maxsus Xatolar (Custom Exceptions)",
                "order": 7,
                "content": (
                    "=== Custom Exception yaratish ===\n"
                    "Exception klassidan meros olib, o'z xatolarini yaratish.\n\n"
                    "=== Asosiy custom exception ===\n"
                    "class YoshXatosi(Exception):\n"
                    "    pass\n\n"
                    "def yosh_tekshir(yosh):\n"
                    "    if yosh < 0:\n"
                    "        raise YoshXatosi('Yosh manfiy bolaolmaydi!')\n"
                    "    if yosh > 150:\n"
                    "        raise YoshXatosi('Yosh 150 dan katta bolaolmaydi!')\n"
                    "    return f'Yosh: {yosh}'\n\n"
                    "try:\n"
                    "    print(yosh_tekshir(-5))\n"
                    "except YoshXatosi as e:\n"
                    "    print(f'Xato: {e}')\n\n"
                    "=== Ma'lumotli custom exception ===\n"
                    "class MablagYetarliEmas(Exception):\n"
                    "    def __init__(self, kerak, mavjud):\n"
                    "        super().__init__(f'Kerak: {kerak}, Mavjud: {mavjud}')\n"
                    "        self.kerak = kerak\n"
                    "        self.mavjud = mavjud\n\n"
                    "def pul_yechish(hisob, miqdor):\n"
                    "    if miqdor > hisob:\n"
                    "        raise MablagYetarliEmas(miqdor, hisob)\n"
                    "    return hisob - miqdor\n\n"
                    "try:\n"
                    "    qoldi = pul_yechish(1000, 1500)\n"
                    "except MablagYetarliEmas as e:\n"
                    "    print(f'Xato: {e}')\n"
                    "    print(f'Kamomad: {e.kerak - e.mavjud}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=ZsvftkbbrR0",
            },
            {
                "title": "Amaliy Loyiha: Kontaktlar Kitobi",
                "order": 8,
                "content": (
                    "=== Kontaktlar Kitobi Loyihasi ===\n"
                    "JSON faylda kontaktlarni saqlash va boshqarish.\n\n"
                    "import json\nimport os\n\n"
                    "FAYL = 'kontaktlar.json'\n\n"
                    "def yuklash():\n"
                    "    if os.path.exists(FAYL):\n"
                    "        with open(FAYL, 'r', encoding='utf-8') as f:\n"
                    "            return json.load(f)\n"
                    "    return {}\n\n"
                    "def saqlash(kontaktlar):\n"
                    "    with open(FAYL, 'w', encoding='utf-8') as f:\n"
                    "        json.dump(kontaktlar, f, ensure_ascii=False, indent=2)\n\n"
                    "def qo_sh(ism, telefon):\n"
                    "    kontaktlar = yuklash()\n"
                    "    kontaktlar[ism] = telefon\n"
                    "    saqlash(kontaktlar)\n"
                    "    print(f'{ism} qo\\'shildi.')\n\n"
                    "def qidir(ism):\n"
                    "    kontaktlar = yuklash()\n"
                    "    if ism in kontaktlar:\n"
                    "        print(f'{ism}: {kontaktlar[ism]}')\n"
                    "    else:\n"
                    "        print(f'{ism} topilmadi.')\n\n"
                    "def ko_rsat():\n"
                    "    kontaktlar = yuklash()\n"
                    "    if not kontaktlar:\n"
                    "        print('Kontaktlar yo\\'q.')\n"
                    "        return\n"
                    "    for ism, tel in sorted(kontaktlar.items()):\n"
                    "        print(f'{ism}: {tel}')\n\n"
                    "# Test:\n"
                    "qo_sh('Ali Karimov', '+998901234567')\n"
                    "qo_sh('Sarvar Toshev', '+998901234568')\n"
                    "ko_rsat()\n"
                    "qidir('Ali Karimov')"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Faylni o'qish uchun qaysi rejim ishlatiladi?",
                 "answers": ["'w'", "'r'", "'a'", "'x'"], "correct": 1},
                {"text": "try/except bloki nima uchun ishlatiladi?",
                 "answers": ["Fayllarni ochish", "Xatolarni boshqarish", "Funksiya chaqirish", "Sikl yaratish"], "correct": 1},
                {"text": "with open(...) iborasining afzalligi nima?",
                 "answers": ["Tezroq o'qiydi", "Faylni avtomatik yopadi", "Katta fayllarni qo'llab-quvvatlaydi", "JSON uchun"], "correct": 1},
                {"text": "json.load() nima qiladi?",
                 "answers": ["JSON yozadi", "JSON fayldan o'qiydi", "JSON formatlaydi", "JSON o'chiradi"], "correct": 1},
                {"text": "finally bloki qachon ishlaydi?",
                 "answers": ["Faqat xato bo'lganda", "Faqat xato bo'lmaganda", "Har doim", "Hech qachon"], "correct": 2},
            ]
        }
    },
    {
        "title": "Web Dasturlash — Django",
        "description": (
            "Django web framework: loyiha strukturasi, Models, Views, Templates, "
            "URL routing, Django ORM, admin panel, forms va JWT autentifikatsiya. "
            "To'liq funksional REST API va web ilova yaratish."
        ),
        "price": 149000,
        "level": "Intermediate",
        "lessons": [
            {
                "title": "Django o'rnatish va Loyiha Yaratish",
                "order": 1,
                "content": (
                    "=== Django o'rnatish ===\n"
                    "# Virtual muhit yaratish:\n"
                    "python -m venv venv\n"
                    "venv\\Scripts\\activate  # Windows\n"
                    "source venv/bin/activate  # Mac/Linux\n\n"
                    "# Django o'rnatish:\n"
                    "pip install django\n\n"
                    "=== Yangi loyiha yaratish ===\n"
                    "django-admin startproject mening_saytim .\n"
                    "# Struktura:\n"
                    "# mening_saytim/\n"
                    "#   __init__.py\n"
                    "#   settings.py   <- sozlamalar\n"
                    "#   urls.py       <- URL marshrutlar\n"
                    "#   wsgi.py       <- web server interfeysi\n"
                    "# manage.py      <- boshqaruv buyruqlari\n\n"
                    "=== Server ishga tushirish ===\n"
                    "python manage.py runserver\n"
                    "# http://127.0.0.1:8000 da oching\n\n"
                    "=== Ilova (app) yaratish ===\n"
                    "python manage.py startapp blog\n"
                    "# settings.py ga qo'shish:\n"
                    "# INSTALLED_APPS = ['blog', ...]\n\n"
                    "=== Asosiy buyruqlar ===\n"
                    "python manage.py startapp [nom]      # app yaratish\n"
                    "python manage.py makemigrations      # migration yaratish\n"
                    "python manage.py migrate             # migratsiya qo'llash\n"
                    "python manage.py createsuperuser     # admin yaratish\n"
                    "python manage.py shell               # Python shell"
                ),
                "video_url": "https://www.youtube.com/watch?v=rHux0gMZ3Eg",
            },
            {
                "title": "Models va Ma'lumotlar Bazasi",
                "order": 2,
                "content": (
                    "=== Model yaratish ===\n"
                    "# blog/models.py\n"
                    "from django.db import models\n\n"
                    "class Post(models.Model):\n"
                    "    sarlavha = models.CharField(max_length=200)\n"
                    "    mazmun = models.TextField()\n"
                    "    muallif = models.CharField(max_length=100)\n"
                    "    yaratilgan = models.DateTimeField(auto_now_add=True)\n"
                    "    yangilangan = models.DateTimeField(auto_now=True)\n"
                    "    nashr_etilgan = models.BooleanField(default=False)\n\n"
                    "    def __str__(self):\n"
                    "        return self.sarlavha\n\n"
                    "    class Meta:\n"
                    "        ordering = ['-yaratilgan']\n\n"
                    "=== Migratsiya ===\n"
                    "python manage.py makemigrations  # o'zgarishlarni aniqlash\n"
                    "python manage.py migrate         # bazaga qo'llash\n\n"
                    "=== Django ORM so'rovlari ===\n"
                    "# Hammasi:\n"
                    "Post.objects.all()\n\n"
                    "# Birinchi/oxirgi:\n"
                    "Post.objects.first()\n"
                    "Post.objects.last()\n\n"
                    "# Qidirish:\n"
                    "Post.objects.filter(nashr_etilgan=True)\n"
                    "Post.objects.get(id=1)\n\n"
                    "# Yaratish:\n"
                    "Post.objects.create(sarlavha='Yangi post', mazmun='...')\n\n"
                    "# Saralash:\n"
                    "Post.objects.order_by('-yaratilgan')"
                ),
                "video_url": "https://www.youtube.com/watch?v=W0GsWBMkMQk",
            },
            {
                "title": "Views va URL'lar",
                "order": 3,
                "content": (
                    "=== Function-based view ===\n"
                    "# blog/views.py\n"
                    "from django.shortcuts import render, get_object_or_404\n"
                    "from .models import Post\n\n"
                    "def post_list(request):\n"
                    "    postlar = Post.objects.filter(nashr_etilgan=True)\n"
                    "    return render(request, 'blog/list.html', {'postlar': postlar})\n\n"
                    "def post_detail(request, pk):\n"
                    "    post = get_object_or_404(Post, pk=pk)\n"
                    "    return render(request, 'blog/detail.html', {'post': post})\n\n"
                    "=== URL sozlash ===\n"
                    "# blog/urls.py\n"
                    "from django.urls import path\n"
                    "from . import views\n\n"
                    "urlpatterns = [\n"
                    "    path('', views.post_list, name='post-list'),\n"
                    "    path('<int:pk>/', views.post_detail, name='post-detail'),\n"
                    "]\n\n"
                    "# mening_saytim/urls.py\n"
                    "from django.urls import path, include\n"
                    "urlpatterns = [\n"
                    "    path('blog/', include('blog.urls')),\n"
                    "    path('admin/', admin.site.urls),\n"
                    "]\n\n"
                    "=== JsonResponse ===\n"
                    "from django.http import JsonResponse\n\n"
                    "def api_postlar(request):\n"
                    "    postlar = list(Post.objects.values('id', 'sarlavha'))\n"
                    "    return JsonResponse({'postlar': postlar})"
                ),
                "video_url": "https://www.youtube.com/watch?v=m6GHs-7JjNE",
            },
            {
                "title": "Templates va Jinja2",
                "order": 4,
                "content": (
                    "=== Template yaratish ===\n"
                    "# blog/templates/blog/list.html\n\n"
                    "<!DOCTYPE html>\n"
                    "<html>\n"
                    "<body>\n"
                    "  <h1>Blog Postlar</h1>\n"
                    "  {% for post in postlar %}\n"
                    "    <article>\n"
                    "      <h2>{{ post.sarlavha }}</h2>\n"
                    "      <p>{{ post.mazmun|truncatewords:30 }}</p>\n"
                    "      <a href=\"{% url 'post-detail' post.pk %}\">O'qish</a>\n"
                    "    </article>\n"
                    "  {% empty %}\n"
                    "    <p>Postlar yo'q.</p>\n"
                    "  {% endfor %}\n"
                    "</body>\n"
                    "</html>\n\n"
                    "=== Template teglari ===\n"
                    "{{ o'zgaruvchi }}         <- qiymat chiqarish\n"
                    "{% tag %}                 <- mantiq\n"
                    "{{ matn|upper }}          <- filtr\n\n"
                    "=== Foydali teglar ===\n"
                    "{% if shart %} ... {% endif %}\n"
                    "{% for x in lst %} ... {% endfor %}\n"
                    "{% extends 'base.html' %}\n"
                    "{% block content %} ... {% endblock %}\n"
                    "{% include 'nav.html' %}\n"
                    "{% url 'view-name' arg %}\n"
                    "{% static 'css/style.css' %}"
                ),
                "video_url": "https://www.youtube.com/watch?v=9aEsZxaOwRs",
            },
            {
                "title": "Django Admin Paneli",
                "order": 5,
                "content": (
                    "=== Admin sozlash ===\n"
                    "# Superuser yaratish:\n"
                    "python manage.py createsuperuser\n"
                    "# http://127.0.0.1:8000/admin/ ga kiring\n\n"
                    "=== Modelni admin'ga qo'shish ===\n"
                    "# blog/admin.py\n"
                    "from django.contrib import admin\n"
                    "from .models import Post\n\n"
                    "admin.site.register(Post)\n\n"
                    "=== Kengaytirilgan sozlash ===\n"
                    "@admin.register(Post)\n"
                    "class PostAdmin(admin.ModelAdmin):\n"
                    "    list_display = ['sarlavha', 'muallif', 'yaratilgan', 'nashr_etilgan']\n"
                    "    list_filter = ['nashr_etilgan', 'yaratilgan']\n"
                    "    search_fields = ['sarlavha', 'mazmun']\n"
                    "    date_hierarchy = 'yaratilgan'\n"
                    "    ordering = ['-yaratilgan']\n"
                    "    list_per_page = 20\n\n"
                    "    # Harakatlar:\n"
                    "    actions = ['nashr_et']\n\n"
                    "    def nashr_et(self, request, queryset):\n"
                    "        queryset.update(nashr_etilgan=True)\n"
                    "    nashr_et.short_description = 'Tanlanganlari nashr et'"
                ),
                "video_url": "https://www.youtube.com/watch?v=_uQrJ0TkZlc",
            },
            {
                "title": "Forms va Validatsiya",
                "order": 6,
                "content": (
                    "=== Django Form ===\n"
                    "# blog/forms.py\n"
                    "from django import forms\n"
                    "from .models import Post\n\n"
                    "class PostForm(forms.Form):\n"
                    "    sarlavha = forms.CharField(max_length=200)\n"
                    "    mazmun = forms.CharField(widget=forms.Textarea)\n"
                    "    nashr_etilgan = forms.BooleanField(required=False)\n\n"
                    "=== ModelForm ===\n"
                    "class PostModelForm(forms.ModelForm):\n"
                    "    class Meta:\n"
                    "        model = Post\n"
                    "        fields = ['sarlavha', 'mazmun', 'nashr_etilgan']\n"
                    "        widgets = {\n"
                    "            'mazmun': forms.Textarea(attrs={'rows': 5}),\n"
                    "        }\n\n"
                    "=== View'da form ===\n"
                    "def post_yarat(request):\n"
                    "    if request.method == 'POST':\n"
                    "        form = PostModelForm(request.POST)\n"
                    "        if form.is_valid():\n"
                    "            post = form.save()\n"
                    "            return redirect('post-detail', pk=post.pk)\n"
                    "    else:\n"
                    "        form = PostModelForm()\n"
                    "    return render(request, 'blog/form.html', {'form': form})\n\n"
                    "=== Custom validatsiya ===\n"
                    "def clean_sarlavha(self):\n"
                    "    sarlavha = self.cleaned_data['sarlavha']\n"
                    "    if len(sarlavha) < 5:\n"
                    "        raise forms.ValidationError('Sarlavha juda qisqa!')\n"
                    "    return sarlavha"
                ),
                "video_url": "https://www.youtube.com/watch?v=I2-JYxnSiB0",
            },
            {
                "title": "Django REST Framework",
                "order": 7,
                "content": (
                    "=== DRF o'rnatish ===\n"
                    "pip install djangorestframework\n"
                    "# settings.py: INSTALLED_APPS += ['rest_framework']\n\n"
                    "=== Serializer ===\n"
                    "from rest_framework import serializers\n"
                    "from .models import Post\n\n"
                    "class PostSerializer(serializers.ModelSerializer):\n"
                    "    class Meta:\n"
                    "        model = Post\n"
                    "        fields = ['id', 'sarlavha', 'mazmun', 'yaratilgan']\n\n"
                    "=== API View ===\n"
                    "from rest_framework.decorators import api_view\n"
                    "from rest_framework.response import Response\n"
                    "from rest_framework import status\n\n"
                    "@api_view(['GET', 'POST'])\n"
                    "def post_list(request):\n"
                    "    if request.method == 'GET':\n"
                    "        postlar = Post.objects.all()\n"
                    "        ser = PostSerializer(postlar, many=True)\n"
                    "        return Response(ser.data)\n"
                    "    elif request.method == 'POST':\n"
                    "        ser = PostSerializer(data=request.data)\n"
                    "        if ser.is_valid():\n"
                    "            ser.save()\n"
                    "            return Response(ser.data, status=201)\n"
                    "        return Response(ser.errors, status=400)"
                ),
                "video_url": "https://www.youtube.com/watch?v=TmsD8QExZ84",
            },
            {
                "title": "JWT Autentifikatsiya",
                "order": 8,
                "content": (
                    "=== SimpleJWT o'rnatish ===\n"
                    "pip install djangorestframework-simplejwt\n\n"
                    "# settings.py\n"
                    "REST_FRAMEWORK = {\n"
                    "    'DEFAULT_AUTHENTICATION_CLASSES': [\n"
                    "        'rest_framework_simplejwt.authentication.JWTAuthentication',\n"
                    "    ],\n"
                    "}\n\n"
                    "# urls.py\n"
                    "from rest_framework_simplejwt.views import (\n"
                    "    TokenObtainPairView,\n"
                    "    TokenRefreshView,\n"
                    ")\n\n"
                    "urlpatterns = [\n"
                    "    path('api/token/', TokenObtainPairView.as_view()),\n"
                    "    path('api/token/refresh/', TokenRefreshView.as_view()),\n"
                    "]\n\n"
                    "=== Token olish ===\n"
                    "# POST /api/token/\n"
                    "# {\"username\": \"ali\", \"password\": \"parol123\"}\n"
                    "# Javob:\n"
                    "# {\"access\": \"eyJ...\", \"refresh\": \"eyJ...\"}\n\n"
                    "=== Himoyalangan view ===\n"
                    "from rest_framework.permissions import IsAuthenticated\n\n"
                    "@api_view(['GET'])\n"
                    "@permission_classes([IsAuthenticated])\n"
                    "def shaxsiy_malumot(request):\n"
                    "    return Response({'user': request.user.username})"
                ),
                "video_url": "https://www.youtube.com/watch?v=PUzgZrS_piQ",
            },
            {
                "title": "Deployment (Render/VPS)",
                "order": 9,
                "content": (
                    "=== Production sozlash ===\n"
                    "# settings.py\n"
                    "DEBUG = False\n"
                    "ALLOWED_HOSTS = ['yourdomain.com', '*.render.com']\n\n"
                    "# .env fayldan maxfiy ma'lumotlar:\n"
                    "import os\n"
                    "SECRET_KEY = os.environ.get('SECRET_KEY')\n"
                    "DATABASE_URL = os.environ.get('DATABASE_URL')\n\n"
                    "=== requirements.txt ===\n"
                    "pip freeze > requirements.txt\n\n"
                    "=== Gunicorn ===\n"
                    "pip install gunicorn\n"
                    "gunicorn mening_saytim.wsgi:application\n\n"
                    "=== Static fayllar ===\n"
                    "# settings.py\n"
                    "STATIC_ROOT = BASE_DIR / 'staticfiles'\n"
                    "python manage.py collectstatic\n\n"
                    "=== Render.com deploy ===\n"
                    "# Build Command:\n"
                    "pip install -r requirements.txt && python manage.py collectstatic\n"
                    "# Start Command:\n"
                    "gunicorn mening_saytim.wsgi:application"
                ),
                "video_url": "https://www.youtube.com/watch?v=2_aclLr3o5s",
            },
            {
                "title": "Amaliy Loyiha: Blog API",
                "order": 10,
                "content": (
                    "=== To'liq Blog REST API ===\n"
                    "DRF yordamida CRUD operatsiyalarini bajaruvchi API.\n\n"
                    "=== Model ===\n"
                    "class Post(models.Model):\n"
                    "    sarlavha = models.CharField(max_length=200)\n"
                    "    mazmun = models.TextField()\n"
                    "    muallif = models.ForeignKey(User, on_delete=models.CASCADE)\n"
                    "    yaratilgan = models.DateTimeField(auto_now_add=True)\n\n"
                    "=== Serializer ===\n"
                    "class PostSerializer(serializers.ModelSerializer):\n"
                    "    muallif_ism = serializers.CharField(\n"
                    "        source='muallif.username', read_only=True)\n"
                    "    class Meta:\n"
                    "        model = Post\n"
                    "        fields = ['id', 'sarlavha', 'mazmun', 'muallif_ism']\n\n"
                    "=== ViewSet ===\n"
                    "from rest_framework import viewsets\n"
                    "from rest_framework.permissions import IsAuthenticatedOrReadOnly\n\n"
                    "class PostViewSet(viewsets.ModelViewSet):\n"
                    "    queryset = Post.objects.all()\n"
                    "    serializer_class = PostSerializer\n"
                    "    permission_classes = [IsAuthenticatedOrReadOnly]\n\n"
                    "    def perform_create(self, serializer):\n"
                    "        serializer.save(muallif=self.request.user)\n\n"
                    "=== Router ===\n"
                    "from rest_framework.routers import DefaultRouter\n"
                    "router = DefaultRouter()\n"
                    "router.register('posts', PostViewSet)\n"
                    "urlpatterns = router.urls"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Django nima?",
                 "answers": ["Ma'lumotlar bazasi", "Python web framework", "JavaScript kutubxona", "IDE"], "correct": 1},
                {"text": "Django ORM nima qiladi?",
                 "answers": ["HTML yaratadi", "Python kodi bilan SQL bajartiradi", "URL boshqaradi", "Formalarni validatsiya qiladi"], "correct": 1},
                {"text": "urls.py fayli nima uchun?",
                 "answers": ["Ma'lumotlar bazasi", "URL marshrutlash", "Shablon", "Admin"], "correct": 1},
                {"text": "makemigrations nima qiladi?",
                 "answers": ["Server ishga tushiradi", "Model o'zgarishlarini migration faylga yozadi", "Bazani tozalaydi", "Static fayllarni to'playdi"], "correct": 1},
                {"text": "Django admin'ga kirish uchun nima kerak?",
                 "answers": ["Oddiy user", "Superuser", "API token", "Shifrlash kaliti"], "correct": 1},
            ]
        }
    },
    {
        "title": "Data Science — NumPy va Pandas",
        "description": (
            "Data Science kutubxonalari: NumPy (massivlar, matematik amallar), "
            "Pandas (DataFrame, Series, ma'lumotlarni tozalash va tahlil), "
            "Matplotlib va Seaborn bilan vizualizatsiya."
        ),
        "price": 199000,
        "level": "Intermediate",
        "lessons": [
            {
                "title": "NumPy: Massivlar (Arrays)",
                "order": 1,
                "content": (
                    "=== NumPy nima? ===\n"
                    "Yuqori samarali matematik hisoblash uchun kutubxona.\n\n"
                    "import numpy as np\n\n"
                    "=== Array yaratish ===\n"
                    "a = np.array([1, 2, 3, 4, 5])\n"
                    "b = np.array([[1,2,3],[4,5,6]])  # 2D\n"
                    "c = np.zeros((3, 3))              # nollar\n"
                    "d = np.ones((2, 4))               # birlar\n"
                    "e = np.arange(0, 10, 2)           # [0,2,4,6,8]\n"
                    "f = np.linspace(0, 1, 5)          # 5 ta teng oraliq\n\n"
                    "=== Array xususiyatlari ===\n"
                    "print(a.shape)   # (5,)\n"
                    "print(b.shape)   # (2, 3)\n"
                    "print(a.dtype)   # int64\n"
                    "print(a.ndim)    # 1 (o'lchov)\n"
                    "print(a.size)    # 5 (elementlar soni)\n\n"
                    "=== Indekslash va slicing ===\n"
                    "a = np.array([10, 20, 30, 40, 50])\n"
                    "print(a[0])      # 10\n"
                    "print(a[-1])     # 50\n"
                    "print(a[1:4])    # [20 30 40]\n"
                    "print(a[::2])    # [10 30 50]\n\n"
                    "=== Shakl o'zgartirish ===\n"
                    "a = np.arange(12)\n"
                    "b = a.reshape(3, 4)   # 3x4 matritsa\n"
                    "c = b.flatten()        # yana 1D ga"
                ),
                "video_url": "https://www.youtube.com/watch?v=QUT1VHiLmmI",
            },
            {
                "title": "NumPy: Matematik Amallar",
                "order": 2,
                "content": (
                    "=== Vektorlashtirish ===\n"
                    "import numpy as np\n\n"
                    "a = np.array([1, 2, 3, 4, 5])\n"
                    "print(a + 10)    # [11 12 13 14 15]\n"
                    "print(a * 2)     # [2 4 6 8 10]\n"
                    "print(a ** 2)    # [1 4 9 16 25]\n"
                    "print(np.sqrt(a)) # [1.0 1.41 1.73 2.0 2.23]\n\n"
                    "=== Ikki array amali ===\n"
                    "a = np.array([1, 2, 3])\n"
                    "b = np.array([4, 5, 6])\n"
                    "print(a + b)  # [5 7 9]\n"
                    "print(a * b)  # [4 10 18]\n"
                    "print(np.dot(a, b))  # 32 (skalyar ko'paytma)\n\n"
                    "=== Statistika ===\n"
                    "a = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])\n"
                    "print(np.mean(a))    # 5.5 (o'rtacha)\n"
                    "print(np.median(a))  # 5.5 (mediana)\n"
                    "print(np.std(a))     # 2.87 (standart og'ish)\n"
                    "print(np.sum(a))     # 55\n"
                    "print(np.min(a))     # 1\n"
                    "print(np.max(a))     # 10\n\n"
                    "=== Boolean indexing ===\n"
                    "a = np.array([1, 2, 3, 4, 5, 6])\n"
                    "print(a[a > 3])     # [4 5 6]\n"
                    "print(a[a % 2 == 0]) # [2 4 6]"
                ),
                "video_url": "https://www.youtube.com/watch?v=QUT1VHiLmmI",
            },
            {
                "title": "Pandas: Series va DataFrame",
                "order": 3,
                "content": (
                    "=== Pandas nima? ===\n"
                    "Jadval ma'lumotlarini tahlil qilish kutubxonasi.\n\n"
                    "import pandas as pd\n\n"
                    "=== Series ===\n"
                    "s = pd.Series([10, 20, 30, 40])\n"
                    "print(s)\n"
                    "# 0    10\n"
                    "# 1    20  ...\n\n"
                    "s = pd.Series([10, 20, 30], index=['a', 'b', 'c'])\n"
                    "print(s['b'])   # 20\n\n"
                    "=== DataFrame ===\n"
                    "df = pd.DataFrame({\n"
                    "    'ism': ['Ali', 'Sarvar', 'Kamol'],\n"
                    "    'yosh': [20, 25, 22],\n"
                    "    'ball': [95, 88, 72]\n"
                    "})\n"
                    "print(df)\n"
                    "print(df.shape)   # (3, 3)\n"
                    "print(df.dtypes)  # ustun turlari\n\n"
                    "=== Ustun va qator murojaat ===\n"
                    "print(df['ism'])           # ism ustuni\n"
                    "print(df[['ism', 'ball']]) # bir nechta ustun\n"
                    "print(df.iloc[0])          # birinchi qator\n"
                    "print(df.loc[0, 'ism'])    # birinchi qator, ism\n"
                    "print(df[df['ball'] > 80]) # filtr"
                ),
                "video_url": "https://www.youtube.com/watch?v=vmEHCJofslg",
            },
            {
                "title": "Pandas: Ma'lumotlarni Yuklash",
                "order": 4,
                "content": (
                    "=== CSV yuklash ===\n"
                    "import pandas as pd\n\n"
                    "df = pd.read_csv('talabalar.csv')\n"
                    "df = pd.read_csv('data.csv', encoding='utf-8', sep=',')\n"
                    "df = pd.read_csv('data.csv', nrows=1000)  # faqat 1000 ta\n\n"
                    "=== Ma'lumotni ko'rish ===\n"
                    "print(df.head())        # birinchi 5 qator\n"
                    "print(df.tail(3))       # oxirgi 3 qator\n"
                    "print(df.info())        # umumiy ma'lumot\n"
                    "print(df.describe())    # statistika\n"
                    "print(df.shape)         # (qatorlar, ustunlar)\n"
                    "print(df.columns)       # ustun nomlari\n\n"
                    "=== Boshqa formatlar ===\n"
                    "# Excel:\n"
                    "df = pd.read_excel('data.xlsx', sheet_name='Sheet1')\n\n"
                    "# JSON:\n"
                    "df = pd.read_json('data.json')\n\n"
                    "# SQLite:\n"
                    "import sqlite3\n"
                    "conn = sqlite3.connect('db.sqlite3')\n"
                    "df = pd.read_sql('SELECT * FROM talabalar', conn)\n\n"
                    "=== CSV ga saqlash ===\n"
                    "df.to_csv('natija.csv', index=False, encoding='utf-8')"
                ),
                "video_url": "https://www.youtube.com/watch?v=vmEHCJofslg",
            },
            {
                "title": "Pandas: Ma'lumotlarni Tozalash",
                "order": 5,
                "content": (
                    "=== Null qiymatlar ===\n"
                    "import pandas as pd\n"
                    "import numpy as np\n\n"
                    "df = pd.DataFrame({'A': [1, None, 3], 'B': [4, 5, None]})\n"
                    "print(df.isnull())        # True/False\n"
                    "print(df.isnull().sum())  # har ustundagi null soni\n\n"
                    "# Null qatorlarni o'chirish:\n"
                    "df_tozalangan = df.dropna()\n\n"
                    "# Null ni to'ldirish:\n"
                    "df['A'] = df['A'].fillna(df['A'].mean())\n"
                    "df['B'] = df['B'].fillna(0)\n\n"
                    "=== Duplikatlar ===\n"
                    "df = pd.DataFrame({'A': [1, 2, 2, 3], 'B': ['a', 'b', 'b', 'c']})\n"
                    "print(df.duplicated())         # bool\n"
                    "df_noyob = df.drop_duplicates()\n\n"
                    "=== Tur o'zgartirish ===\n"
                    "df['yosh'] = df['yosh'].astype(int)\n"
                    "df['sana'] = pd.to_datetime(df['sana'])\n\n"
                    "=== Noto'g'ri qiymatlar ===\n"
                    "df = df[df['yosh'] > 0]         # manfiy yoshni o'chirish\n"
                    "df = df[df['ball'].between(0, 100)]"
                ),
                "video_url": "https://www.youtube.com/watch?v=bDhvCp3_lYw",
            },
            {
                "title": "Pandas: Groupby va Agregatsiya",
                "order": 6,
                "content": (
                    "=== Groupby ===\n"
                    "import pandas as pd\n\n"
                    "df = pd.DataFrame({\n"
                    "    'shahar': ['Toshkent', 'Samarqand', 'Toshkent', 'Samarqand'],\n"
                    "    'yosh': [20, 25, 22, 30],\n"
                    "    'maosh': [5000, 6000, 4500, 7000]\n"
                    "})\n\n"
                    "# Shahar bo'yicha o'rtacha:\n"
                    "print(df.groupby('shahar')['maosh'].mean())\n\n"
                    "# Ko'p funksiya:\n"
                    "print(df.groupby('shahar').agg({\n"
                    "    'yosh': 'mean',\n"
                    "    'maosh': ['min', 'max', 'sum']\n"
                    "}))\n\n"
                    "=== apply() ===\n"
                    "df['daraja'] = df['maosh'].apply(\n"
                    "    lambda x: 'yuqori' if x > 5500 else 'past')\n\n"
                    "=== Pivot table ===\n"
                    "pivot = df.pivot_table(\n"
                    "    values='maosh',\n"
                    "    index='shahar',\n"
                    "    aggfunc='mean'\n"
                    ")\n"
                    "print(pivot)"
                ),
                "video_url": "https://www.youtube.com/watch?v=txMdrV1Ut64",
            },
            {
                "title": "Matplotlib bilan Grafik",
                "order": 7,
                "content": (
                    "=== Matplotlib ===\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "=== Chiziqli grafik ===\n"
                    "x = np.linspace(0, 10, 100)\n"
                    "y = np.sin(x)\n"
                    "plt.plot(x, y, 'b-', label='sin(x)')\n"
                    "plt.plot(x, np.cos(x), 'r--', label='cos(x)')\n"
                    "plt.xlabel('x')\n"
                    "plt.ylabel('y')\n"
                    "plt.title('Sin va Cos')\n"
                    "plt.legend()\n"
                    "plt.grid(True)\n"
                    "plt.show()\n\n"
                    "=== Ustunli grafik ===\n"
                    "kategoriyalar = ['Python', 'Django', 'FastAPI', 'Flask']\n"
                    "qiymatlar = [80, 65, 45, 55]\n"
                    "plt.bar(kategoriyalar, qiymatlar, color='skyblue')\n"
                    "plt.title('Ramkalar mashhurligi')\n"
                    "plt.show()\n\n"
                    "=== Scatter plot ===\n"
                    "x = np.random.randn(100)\n"
                    "y = x * 2 + np.random.randn(100)\n"
                    "plt.scatter(x, y, alpha=0.5)\n"
                    "plt.title('Korrelyatsiya')\n"
                    "plt.show()"
                ),
                "video_url": "https://www.youtube.com/watch?v=3Xc3CA655Y4",
            },
            {
                "title": "Seaborn bilan Vizualizatsiya",
                "order": 8,
                "content": (
                    "=== Seaborn ===\n"
                    "import seaborn as sns\n"
                    "import matplotlib.pyplot as plt\n"
                    "import pandas as pd\n\n"
                    "# Namuna dataset:\n"
                    "df = sns.load_dataset('iris')\n\n"
                    "=== Histogramma ===\n"
                    "sns.histplot(data=df, x='sepal_length', kde=True)\n"
                    "plt.show()\n\n"
                    "=== Boxplot ===\n"
                    "sns.boxplot(data=df, x='species', y='petal_length')\n"
                    "plt.title('Gultok uzunligi')\n"
                    "plt.show()\n\n"
                    "=== Heatmap (korrelyatsiya) ===\n"
                    "korr = df.select_dtypes(include='number').corr()\n"
                    "sns.heatmap(korr, annot=True, cmap='coolwarm')\n"
                    "plt.show()\n\n"
                    "=== Pairplot ===\n"
                    "sns.pairplot(df, hue='species')\n"
                    "plt.show()\n\n"
                    "=== Violin plot ===\n"
                    "sns.violinplot(data=df, x='species', y='sepal_width')\n"
                    "plt.show()"
                ),
                "video_url": "https://www.youtube.com/watch?v=6GUZXDef2U0",
            },
            {
                "title": "Amaliy Loyiha: Narx Tahlili",
                "order": 9,
                "content": (
                    "=== Narx Tahlili Loyihasi ===\n"
                    "Pandas va Matplotlib yordamida mahsulot narxlarini tahlil qilish.\n\n"
                    "import pandas as pd\n"
                    "import matplotlib.pyplot as plt\n"
                    "import numpy as np\n\n"
                    "# Dataset yaratish:\n"
                    "np.random.seed(42)\n"
                    "n = 100\n"
                    "df = pd.DataFrame({\n"
                    "    'mahsulot': np.random.choice(['Olma', 'Banan', 'Gilos', 'Uzum'], n),\n"
                    "    'narx': np.random.uniform(1000, 20000, n).round(),\n"
                    "    'soni': np.random.randint(1, 50, n),\n"
                    "    'oy': np.random.randint(1, 13, n),\n"
                    "})\n\n"
                    "# Tahlil:\n"
                    "df['jami'] = df['narx'] * df['soni']\n\n"
                    "print('=== Asosiy statistika ===')\n"
                    "print(df.describe())\n\n"
                    "print('=== Mahsulot bo\\'yicha o\\'rtacha narx ===')\n"
                    "print(df.groupby('mahsulot')['narx'].mean().sort_values(ascending=False))\n\n"
                    "# Grafik:\n"
                    "fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))\n\n"
                    "# Ustunli grafik:\n"
                    "df.groupby('mahsulot')['jami'].sum().plot(kind='bar', ax=ax1)\n"
                    "ax1.set_title('Jami sotuv')\n\n"
                    "# Pie chart:\n"
                    "df.groupby('mahsulot')['soni'].sum().plot(kind='pie', ax=ax2)\n"
                    "ax2.set_title('Sotilgan miqdor')\n\n"
                    "plt.tight_layout()\n"
                    "plt.savefig('tahlil.png')\n"
                    "print('Grafik saqlandi: tahlil.png')"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Pandas'da DataFrame nima?",
                 "answers": ["Rasm turi", "Jadval tuzilmasi", "Funksiya", "Sikl"], "correct": 1},
                {"text": "NumPy asosan nima uchun ishlatiladi?",
                 "answers": ["Web dasturlash", "Jadval tuzilmalari", "Yuqori samarali matematik amallar", "Ma'lumotlar bazasi"], "correct": 2},
                {"text": "pd.read_csv() nima qiladi?",
                 "answers": ["CSV yozadi", "CSV o'chiradi", "CSV faylni DataFrame ga yuklaydi", "CSV formatlaydi"], "correct": 2},
                {"text": "df.dropna() nima qiladi?",
                 "answers": ["Barcha ma'lumotni o'chiradi", "Null qiymatli qatorlarni o'chiradi", "Duplikatlarni o'chiradi", "Saralaydi"], "correct": 1},
                {"text": "matplotlib.pyplot nima uchun?",
                 "answers": ["Ma'lumotlarni tozalash", "Matematik amallar", "Grafiklar chizish", "Web dasturlash"], "correct": 2},
            ]
        }
    },
    {
        "title": "Machine Learning Asoslari",
        "description": (
            "Machine Learning: supervised/unsupervised learning, scikit-learn, "
            "linear/logistic regression, Decision Tree, Random Forest, "
            "model baholash, cross-validation va feature engineering."
        ),
        "price": 249000,
        "level": "Professional",
        "lessons": [
            {
                "title": "Machine Learning Nima?",
                "order": 1,
                "content": (
                    "=== Machine Learning nima? ===\n"
                    "Kompyuterni aniq dasturlamasdan o'rganishga o'rgatish.\n\n"
                    "=== 3 asosiy paradigma ===\n\n"
                    "1. Supervised Learning (Nazoratli)\n"
                    "   - Belgilangan ma'lumotlar bilan o'rganish\n"
                    "   - Kiritish X va to'g'ri javob Y beriladi\n"
                    "   - Misol: spam filtri, narx bashorati\n"
                    "   - Algoritmlar: Linear Regression, Decision Tree\n\n"
                    "2. Unsupervised Learning (Nazoratssiz)\n"
                    "   - Belgilanmagan ma'lumotlar bilan o'rganish\n"
                    "   - Yashirin tuzilmalarni topish\n"
                    "   - Misol: mijozlar guruhlash, anomaliya topish\n"
                    "   - Algoritmlar: K-Means, PCA\n\n"
                    "3. Reinforcement Learning (Mustahkamlash)\n"
                    "   - Agent muhit bilan o'zaro ta'sir qiladi\n"
                    "   - Mukofot va jazo orqali o'rganish\n"
                    "   - Misol: o'yinlar, robot boshqarish\n\n"
                    "=== ML loyiha bosqichlari ===\n"
                    "# 1. Ma'lumot yig'ish\n"
                    "# 2. Ma'lumotni tozalash\n"
                    "# 3. Feature engineering\n"
                    "# 4. Model tanlash va o'rgatish\n"
                    "# 5. Baholash\n"
                    "# 6. Deploy"
                ),
                "video_url": "https://www.youtube.com/watch?v=ukzFI9rgwfU",
            },
            {
                "title": "scikit-learn Bilan Tanishish",
                "order": 2,
                "content": (
                    "=== scikit-learn ===\n"
                    "Python'da ML uchun asosiy kutubxona.\n\n"
                    "pip install scikit-learn\n\n"
                    "=== Asosiy API ===\n"
                    "from sklearn.linear_model import LinearRegression\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import mean_squared_error\n"
                    "import numpy as np\n\n"
                    "# Ma'lumot tayyorlash:\n"
                    "X = np.array([[1], [2], [3], [4], [5]])\n"
                    "y = np.array([2, 4, 6, 8, 10])\n\n"
                    "# Train/test bo'lish:\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, y, test_size=0.2, random_state=42)\n\n"
                    "# Model yaratish va o'rgatish:\n"
                    "model = LinearRegression()\n"
                    "model.fit(X_train, y_train)   # o'rgatish\n\n"
                    "# Bashorat:\n"
                    "y_pred = model.predict(X_test)\n\n"
                    "# Baholash:\n"
                    "mse = mean_squared_error(y_test, y_pred)\n"
                    "print(f'MSE: {mse:.4f}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=0B5eIE_1vpU",
            },
            {
                "title": "Linear Regression",
                "order": 3,
                "content": (
                    "=== Linear Regression ===\n"
                    "Raqamli qiymat bashorat qilish.\n"
                    "y = a*x + b (to'g'ri chiziq)\n\n"
                    "from sklearn.linear_model import LinearRegression\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import mean_squared_error, r2_score\n"
                    "import numpy as np\n\n"
                    "# Uy narxi namuna dataset:\n"
                    "np.random.seed(42)\n"
                    "xona = np.random.randint(1, 6, 100)\n"
                    "narx = xona * 150000 + np.random.randn(100) * 20000\n\n"
                    "X = xona.reshape(-1, 1)\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, narx, test_size=0.2, random_state=42)\n\n"
                    "model = LinearRegression()\n"
                    "model.fit(X_train, y_train)\n\n"
                    "y_pred = model.predict(X_test)\n\n"
                    "print(f'Koeffitsient: {model.coef_[0]:.0f}')\n"
                    "print(f'Intercept: {model.intercept_:.0f}')\n"
                    "print(f'R2 score: {r2_score(y_test, y_pred):.4f}')\n"
                    "print(f'MSE: {mean_squared_error(y_test, y_pred):.0f}')\n\n"
                    "# 3 xonali uy narxi:\n"
                    "bashorat = model.predict([[3]])\n"
                    "print(f'3 xonali: {bashorat[0]:.0f} so\\'m')"
                ),
                "video_url": "https://www.youtube.com/watch?v=E5RjzSK0fvY",
            },
            {
                "title": "Logistic Regression va Klassifikatsiya",
                "order": 4,
                "content": (
                    "=== Logistic Regression ===\n"
                    "Kategoriyalarni tasniflash (klassifikatsiya).\n\n"
                    "from sklearn.linear_model import LogisticRegression\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import accuracy_score, classification_report\n\n"
                    "# Iris dataset:\n"
                    "iris = load_iris()\n"
                    "X, y = iris.data, iris.target\n\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, y, test_size=0.3, random_state=42)\n\n"
                    "model = LogisticRegression(max_iter=200)\n"
                    "model.fit(X_train, y_train)\n\n"
                    "y_pred = model.predict(X_test)\n"
                    "print(f'Aniqlik: {accuracy_score(y_test, y_pred):.4f}')\n"
                    "print(classification_report(y_test, y_pred,\n"
                    "      target_names=iris.target_names))"
                ),
                "video_url": "https://www.youtube.com/watch?v=yIYKR4sgzI8",
            },
            {
                "title": "Decision Tree va Random Forest",
                "order": 5,
                "content": (
                    "=== Decision Tree ===\n"
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import accuracy_score\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, y, test_size=0.3, random_state=42)\n\n"
                    "dt = DecisionTreeClassifier(max_depth=3)\n"
                    "dt.fit(X_train, y_train)\n"
                    "print(f'DT aniqlik: {accuracy_score(y_test, dt.predict(X_test)):.4f}')\n\n"
                    "=== Random Forest ===\n"
                    "# Ko'p qaror daraxtlari ensemble\n"
                    "from sklearn.ensemble import RandomForestClassifier\n\n"
                    "rf = RandomForestClassifier(n_estimators=100, random_state=42)\n"
                    "rf.fit(X_train, y_train)\n"
                    "print(f'RF aniqlik: {accuracy_score(y_test, rf.predict(X_test)):.4f}')\n\n"
                    "# Feature muhimligi:\n"
                    "for nom, muh in zip(load_iris().feature_names, rf.feature_importances_):\n"
                    "    print(f'{nom}: {muh:.4f}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=_L39rN6gz7Y",
            },
            {
                "title": "K-Nearest Neighbors (KNN)",
                "order": 6,
                "content": (
                    "=== KNN nima? ===\n"
                    "Yangi nuqtani k ta eng yaqin qo'shniga qarab tasniflash.\n\n"
                    "from sklearn.neighbors import KNeighborsClassifier\n"
                    "from sklearn.datasets import load_iris\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.preprocessing import StandardScaler\n"
                    "from sklearn.metrics import accuracy_score\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, y, test_size=0.3, random_state=42)\n\n"
                    "# Masshtablash (KNN uchun muhim!):\n"
                    "scaler = StandardScaler()\n"
                    "X_train = scaler.fit_transform(X_train)\n"
                    "X_test = scaler.transform(X_test)\n\n"
                    "# Eng yaxshi k ni topish:\n"
                    "for k in [3, 5, 7, 9, 11]:\n"
                    "    knn = KNeighborsClassifier(n_neighbors=k)\n"
                    "    knn.fit(X_train, y_train)\n"
                    "    acc = accuracy_score(y_test, knn.predict(X_test))\n"
                    "    print(f'k={k}: {acc:.4f}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=HVXime0nQeI",
            },
            {
                "title": "Model Baholash Metrikalari",
                "order": 7,
                "content": (
                    "=== Klassifikatsiya metrikalari ===\n"
                    "from sklearn.metrics import (\n"
                    "    accuracy_score, precision_score, recall_score,\n"
                    "    f1_score, confusion_matrix, classification_report\n"
                    ")\n\n"
                    "y_test  = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]\n"
                    "y_pred  = [1, 0, 1, 0, 0, 1, 1, 0, 1, 1]\n\n"
                    "print(f'Accuracy:  {accuracy_score(y_test, y_pred):.4f}')\n"
                    "print(f'Precision: {precision_score(y_test, y_pred):.4f}')\n"
                    "print(f'Recall:    {recall_score(y_test, y_pred):.4f}')\n"
                    "print(f'F1 score:  {f1_score(y_test, y_pred):.4f}')\n\n"
                    "print('Confusion matrix:')\n"
                    "print(confusion_matrix(y_test, y_pred))\n"
                    "# [[TN, FP],\n"
                    "#  [FN, TP]]\n\n"
                    "=== Regressiya metrikalari ===\n"
                    "from sklearn.metrics import mean_squared_error, r2_score\n"
                    "import numpy as np\n\n"
                    "y_test = [3, 2, 5, 1, 4]\n"
                    "y_pred = [2.8, 2.1, 4.9, 1.2, 3.8]\n"
                    "print(f'MSE:  {mean_squared_error(y_test, y_pred):.4f}')\n"
                    "print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.4f}')\n"
                    "print(f'R2:   {r2_score(y_test, y_pred):.4f}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=2osIZ-dSPge",
            },
            {
                "title": "Cross-Validation va Overfitting",
                "order": 8,
                "content": (
                    "=== Overfitting nima? ===\n"
                    "Model o'quv ma'lumotlarini yod olib qoladi - yangi ma'lumotda yomon ishlaydi.\n\n"
                    "=== Cross-Validation ===\n"
                    "from sklearn.model_selection import cross_val_score\n"
                    "from sklearn.ensemble import RandomForestClassifier\n"
                    "from sklearn.datasets import load_iris\n\n"
                    "X, y = load_iris(return_X_y=True)\n"
                    "model = RandomForestClassifier(n_estimators=50)\n\n"
                    "# 5-fold CV:\n"
                    "scores = cross_val_score(model, X, y, cv=5)\n"
                    "print(f'CV natijalar: {scores}')\n"
                    "print(f'O\\'rtacha: {scores.mean():.4f} (+/- {scores.std():.4f})')\n\n"
                    "=== Overfitting oldini olish ===\n"
                    "# 1. Ko'proq ma'lumot\n"
                    "# 2. Regularizatsiya:\n"
                    "from sklearn.linear_model import Ridge, Lasso\n"
                    "ridge = Ridge(alpha=1.0)  # L2 regularizatsiya\n"
                    "lasso = Lasso(alpha=0.1)  # L1 regularizatsiya\n\n"
                    "# 3. max_depth cheklash (Decision Tree)\n"
                    "from sklearn.tree import DecisionTreeClassifier\n"
                    "dt = DecisionTreeClassifier(max_depth=5, min_samples_split=10)"
                ),
                "video_url": "https://www.youtube.com/watch?v=fSytzGwwBVw",
            },
            {
                "title": "Feature Engineering",
                "order": 9,
                "content": (
                    "=== Feature Engineering ===\n"
                    "Ma'lumotlarni model uchun tayyorlash.\n\n"
                    "=== Normalizatsiya / Masshtablash ===\n"
                    "from sklearn.preprocessing import StandardScaler, MinMaxScaler\n"
                    "import numpy as np\n\n"
                    "X = np.array([[100, 0.1], [200, 0.5], [300, 0.9]])\n\n"
                    "# StandardScaler (mean=0, std=1):\n"
                    "scaler = StandardScaler()\n"
                    "X_scaled = scaler.fit_transform(X)\n\n"
                    "# MinMaxScaler (0-1 oralig'i):\n"
                    "mm = MinMaxScaler()\n"
                    "X_mm = mm.fit_transform(X)\n\n"
                    "=== Kategorik encoding ===\n"
                    "from sklearn.preprocessing import LabelEncoder, OneHotEncoder\n"
                    "import pandas as pd\n\n"
                    "shahar = ['Toshkent', 'Samarqand', 'Toshkent', 'Buxoro']\n\n"
                    "# Label encoding:\n"
                    "le = LabelEncoder()\n"
                    "encoded = le.fit_transform(shahar)\n"
                    "print(encoded)  # [2 1 2 0]\n\n"
                    "# One-hot encoding:\n"
                    "df = pd.DataFrame({'shahar': shahar})\n"
                    "dummies = pd.get_dummies(df['shahar'])\n"
                    "print(dummies)"
                ),
                "video_url": "https://www.youtube.com/watch?v=GduT2ZCc26E",
            },
            {
                "title": "Amaliy Loyiha: Narx Bashorati",
                "order": 10,
                "content": (
                    "=== Uy Narxi Bashorati ===\n"
                    "Random Forest bilan narx bashorat qilish.\n\n"
                    "import numpy as np\n"
                    "import pandas as pd\n"
                    "from sklearn.ensemble import RandomForestRegressor\n"
                    "from sklearn.model_selection import train_test_split\n"
                    "from sklearn.metrics import mean_squared_error, r2_score\n"
                    "from sklearn.preprocessing import StandardScaler\n\n"
                    "# Namuna dataset yaratish:\n"
                    "np.random.seed(42)\n"
                    "n = 200\n"
                    "data = pd.DataFrame({\n"
                    "    'xonalar': np.random.randint(1, 6, n),\n"
                    "    'yuza_m2': np.random.randint(30, 200, n),\n"
                    "    'qavat': np.random.randint(1, 16, n),\n"
                    "    'yil': np.random.randint(1980, 2024, n),\n"
                    "})\n"
                    "data['narx'] = (\n"
                    "    data['xonalar'] * 50000 +\n"
                    "    data['yuza_m2'] * 3000 +\n"
                    "    np.random.randn(n) * 30000\n"
                    ")\n\n"
                    "X = data.drop('narx', axis=1)\n"
                    "y = data['narx']\n\n"
                    "X_train, X_test, y_train, y_test = train_test_split(\n"
                    "    X, y, test_size=0.2, random_state=42)\n\n"
                    "model = RandomForestRegressor(n_estimators=100)\n"
                    "model.fit(X_train, y_train)\n"
                    "y_pred = model.predict(X_test)\n\n"
                    "print(f'R2: {r2_score(y_test, y_pred):.4f}')\n"
                    "print(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred)):.0f}')"
                ),
                "video_url": "https://www.youtube.com/watch?v=8ext9G7xspg",
            },
        ],
        "quiz": {
            "questions": [
                {"text": "Supervised learning nima?",
                 "answers": ["Belgilanmagan ma'lumotlar bilan o'rganish", "Belgilangan ma'lumotlar bilan o'rganish", "O'z-o'zidan o'rganish", "Mustahkamlash orqali"], "correct": 1},
                {"text": "train_test_split nima uchun?",
                 "answers": ["Ma'lumotlarni tozalash", "Ma'lumotlarni o'qitish va test qismiga bo'lish", "Modelni saqlash", "Feature tanlash"], "correct": 1},
                {"text": "Overfitting nima?",
                 "answers": ["Model juda oddiy", "Model o'quv ma'lumotlarini yod olib, yangi ma'lumotlarda yomon ishlaydi", "Model hech nima o'rganmadi", "Ma'lumotlar ko'p"], "correct": 1},
                {"text": "Random Forest nima?",
                 "answers": ["Bitta qaror daraxti", "Ko'p qaror daraxtlari ansambli", "Neyron tarmoq", "Klasterizatsiya"], "correct": 1},
                {"text": "Accuracy nima o'lchaydi?",
                 "answers": ["Model hajmi", "To'g'ri bashorat qilingan miqdor nisbati", "O'qitish vaqti", "Xotira sarfi"], "correct": 1},
            ]
        }
    },
]


# ─────────────────────────────────────────────
#  TASKLAR  (LeetCode uslubida)
# ─────────────────────────────────────────────

# Python Asoslari 3-darsi uchun string masalasi
STRING_LESSON_TASK = {
    "title": "Matnni Teskari Yozish",
    "description": (
        "Berilgan matnni teskari tartibda qaytaruvchi funksiya yozing.\n\n"
        "**Misol:**\n"
        "```\n"
        "Kirish:  'Python'\n"
        "Chiqish: 'nohtyP'\n\n"
        "Kirish:  'Salom'\n"
        "Chiqish: 'molaS'\n"
        "```\n\n"
        "**Maslahat:** Python'da string slicing ishlatishingiz mumkin: `s[::-1]`\n\n"
        "**Vazifa:** `solve(s)` funksiyasini yozing — teskari matn qaytarsin."
    ),
    "starter_code": (
        "def solve(s):\n"
        "    # Matnni teskari yozing\n"
        "    # Maslahat: s[::-1] sintaksisidan foydalaning\n"
        "    pass\n"
    ),
    "expected_output": "nohtyP",
    "difficulty": "Beginner",
    "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_python(self):
        from __main__ import solve
        self.assertEqual(solve('Python'), 'nohtyP')

    def test_salom(self):
        from __main__ import solve
        self.assertEqual(solve('Salom'), 'molaS')

    def test_empty(self):
        from __main__ import solve
        self.assertEqual(solve(''), '')

    def test_single(self):
        from __main__ import solve
        self.assertEqual(solve('a'), 'a')

    def test_palindrome(self):
        from __main__ import solve
        self.assertEqual(solve('abba'), 'abba')

if __name__ == "__main__":
    unittest.main()
""",
}

PYTHON_TASKS = [
    {
        "title": "Ikki Sonni Yig'indisi",
        "course_key": "Python Asoslari",
        "description": (
            "Berilgan ikkita butun sonning yig'indisini hisoblang.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  a = 5, b = 3\n"
            "Chiqish: 8\n"
            "```\n\n"
            "**Cheklov:** -10^9 <= a, b <= 10^9\n\n"
            "**Vazifa:** `solve(a, b)` funksiyasini yozing."
        ),
        "starter_code": "def solve(a, b):\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "8",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_positive(self):
        from __main__ import solve
        self.assertEqual(solve(5, 3), 8)

    def test_negative(self):
        from __main__ import solve
        self.assertEqual(solve(-5, 5), 0)

    def test_zero(self):
        from __main__ import solve
        self.assertEqual(solve(0, 0), 0)

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Listdagi Eng Katta Son",
        "course_key": "Ma'lumotlar Tuzilmalari",
        "description": (
            "Berilgan sonlar ro'yxatidagi eng katta sonni toping.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  [3, 1, 4, 1, 5, 9, 2, 6]\n"
            "Chiqish: 9\n"
            "```\n\n"
            "**Cheklov:** Ro'yxatda kamida 1 ta element bo'ladi.\n\n"
            "**Vazifa:** `solve(numbers)` funksiyasini yozing."
        ),
        "starter_code": "def solve(numbers):\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "9",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_basic(self):
        from __main__ import solve
        self.assertEqual(solve([3, 1, 4, 1, 5, 9, 2, 6]), 9)

    def test_negative(self):
        from __main__ import solve
        self.assertEqual(solve([-10, -3, -1]), -1)

    def test_single(self):
        from __main__ import solve
        self.assertEqual(solve([42]), 42)

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Palindrom Tekshirish",
        "course_key": "Python Asoslari",
        "description": (
            "Berilgan matn palindrom ekanligini tekshiring (oldidan va orqadan o'qilganda bir xil).\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  'racecar'\n"
            "Chiqish: True\n\n"
            "Kirish:  'hello'\n"
            "Chiqish: False\n"
            "```\n\n"
            "**Vazifa:** `solve(s)` funksiyasini yozing — True/False qaytarsin."
        ),
        "starter_code": "def solve(s):\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "True",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_palindrome(self):
        from __main__ import solve
        self.assertTrue(solve('racecar'))

    def test_not_palindrome(self):
        from __main__ import solve
        self.assertFalse(solve('hello'))

    def test_single(self):
        from __main__ import solve
        self.assertTrue(solve('a'))

    def test_empty(self):
        from __main__ import solve
        self.assertTrue(solve(''))

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Fibonacci Ketma-ketligi",
        "course_key": "Funksiyalar va Modullar",
        "description": (
            "Fibonacci ketma-ketligining n-chi elementini toping.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  n = 7\n"
            "Chiqish: 13\n"
            "(0, 1, 1, 2, 3, 5, 8, 13, ...)\n"
            "```\n\n"
            "**Cheklov:** 0 <= n <= 30\n\n"
            "**Vazifa:** `solve(n)` funksiyasini yozing."
        ),
        "starter_code": "def solve(n):\n    # 0-indexed Fibonacci\n    # solve(0) = 0, solve(1) = 1, solve(7) = 13\n    pass\n",
        "expected_output": "13",
        "difficulty": "Intermediate",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_base0(self):
        from __main__ import solve
        self.assertEqual(solve(0), 0)

    def test_base1(self):
        from __main__ import solve
        self.assertEqual(solve(1), 1)

    def test_7(self):
        from __main__ import solve
        self.assertEqual(solve(7), 13)

    def test_10(self):
        from __main__ import solve
        self.assertEqual(solve(10), 55)

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "So'zlar Soni",
        "course_key": "Python Asoslari",
        "description": (
            "Berilgan jumlada nechta so'z borligini hisoblang.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  'Salom dunyo bu Python'\n"
            "Chiqish: 4\n"
            "```\n\n"
            "**Eslatma:** So'zlar bo'shliq bilan ajratilgan.\n\n"
            "**Vazifa:** `solve(text)` funksiyasini yozing."
        ),
        "starter_code": "def solve(text):\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "4",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_basic(self):
        from __main__ import solve
        self.assertEqual(solve('Salom dunyo bu Python'), 4)

    def test_single(self):
        from __main__ import solve
        self.assertEqual(solve('Python'), 1)

    def test_empty(self):
        from __main__ import solve
        self.assertEqual(solve(''), 0)

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Listni Teskari Aylantirish",
        "course_key": "Ma'lumotlar Tuzilmalari",
        "description": (
            "Berilgan ro'yxatni teskari tartibda qaytaring.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  [1, 2, 3, 4, 5]\n"
            "Chiqish: [5, 4, 3, 2, 1]\n"
            "```\n\n"
            "**Vazifa:** `solve(lst)` funksiyasini yozing."
        ),
        "starter_code": "def solve(lst):\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "[5, 4, 3, 2, 1]",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_basic(self):
        from __main__ import solve
        self.assertEqual(solve([1, 2, 3, 4, 5]), [5, 4, 3, 2, 1])

    def test_single(self):
        from __main__ import solve
        self.assertEqual(solve([1]), [1])

    def test_empty(self):
        from __main__ import solve
        self.assertEqual(solve([]), [])

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Faktoriyel Hisoblash",
        "course_key": "Funksiyalar va Modullar",
        "description": (
            "Berilgan n sonning faktoriyalini hisoblang: n! = 1 * 2 * 3 * ... * n\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  n = 5\n"
            "Chiqish: 120\n"
            "```\n\n"
            "**Cheklov:** 0 <= n <= 12\n"
            "**Eslatma:** 0! = 1\n\n"
            "**Vazifa:** `solve(n)` funksiyasini yozing."
        ),
        "starter_code": "def solve(n):\n    # 0! = 1, 1! = 1, 5! = 120\n    pass\n",
        "expected_output": "120",
        "difficulty": "Beginner",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_5(self):
        from __main__ import solve
        self.assertEqual(solve(5), 120)

    def test_0(self):
        from __main__ import solve
        self.assertEqual(solve(0), 1)

    def test_1(self):
        from __main__ import solve
        self.assertEqual(solve(1), 1)

    def test_10(self):
        from __main__ import solve
        self.assertEqual(solve(10), 3628800)

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Tub Son Tekshirish",
        "course_key": "OOP - Obyektga Yo'naltirilgan Dasturlash",
        "description": (
            "Berilgan son tub son ekanligini tekshiring.\n\n"
            "Tub son — faqat 1 ga va o'ziga bo'linadigan musbat butun son.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  17\n"
            "Chiqish: True\n\n"
            "Kirish:  4\n"
            "Chiqish: False\n"
            "```\n\n"
            "**Vazifa:** `solve(n)` funksiyasini yozing."
        ),
        "starter_code": "def solve(n):\n    # n tub son bo'lsa True, aks holda False\n    pass\n",
        "expected_output": "True",
        "difficulty": "Intermediate",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_prime(self):
        from __main__ import solve
        self.assertTrue(solve(17))

    def test_not_prime(self):
        from __main__ import solve
        self.assertFalse(solve(4))

    def test_2(self):
        from __main__ import solve
        self.assertTrue(solve(2))

    def test_1(self):
        from __main__ import solve
        self.assertFalse(solve(1))

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Matndagi Takrorlanuvchi Harflar",
        "course_key": "Ma'lumotlar Tuzilmalari",
        "description": (
            "Berilgan matndagi har bir harfning necha marta uchrashini hisoblang.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  'hello'\n"
            "Chiqish: {'h': 1, 'e': 1, 'l': 2, 'o': 1}\n"
            "```\n\n"
            "**Vazifa:** `solve(s)` funksiyasini yozing — dict qaytarsin."
        ),
        "starter_code": "def solve(s):\n    # Har bir harf: necha marta\n    pass\n",
        "expected_output": "{'h': 1, 'e': 1, 'l': 2, 'o': 1}",
        "difficulty": "Intermediate",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_hello(self):
        from __main__ import solve
        self.assertEqual(solve('hello'), {'h': 1, 'e': 1, 'l': 2, 'o': 1})

    def test_aaa(self):
        from __main__ import solve
        self.assertEqual(solve('aaa'), {'a': 3})

    def test_empty(self):
        from __main__ import solve
        self.assertEqual(solve(''), {})

if __name__ == "__main__":
    unittest.main()
""",
    },
    {
        "title": "Saralangan Listdan Topish (Binary Search)",
        "course_key": "Fayl va Xatolarni Boshqarish",
        "description": (
            "Saralangan ro'yxatda target sonni ikkilik qidiruv (binary search) orqali toping. "
            "Topilsa indeksini, topilmasa -1 qaytaring.\n\n"
            "**Misol:**\n"
            "```\n"
            "Kirish:  lst=[1,3,5,7,9,11], target=7\n"
            "Chiqish: 3\n"
            "```\n\n"
            "**Vazifa:** `solve(lst, target)` funksiyasini yozing."
        ),
        "starter_code": "def solve(lst, target):\n    # Binary search algoritmi\n    left, right = 0, len(lst) - 1\n    # Kodingizni shu yerga yozing\n    pass\n",
        "expected_output": "3",
        "difficulty": "Professional",
        "test_code": """import unittest

class TestSolution(unittest.TestCase):
    def test_found(self):
        from __main__ import solve
        self.assertEqual(solve([1,3,5,7,9,11], 7), 3)

    def test_not_found(self):
        from __main__ import solve
        self.assertEqual(solve([1,3,5,7,9,11], 4), -1)

    def test_first(self):
        from __main__ import solve
        self.assertEqual(solve([1,3,5,7,9,11], 1), 0)

    def test_last(self):
        from __main__ import solve
        self.assertEqual(solve([1,3,5,7,9,11], 11), 5)

if __name__ == "__main__":
    unittest.main()
""",
    },
]


class Command(BaseCommand):
    help = "Seed LMS with Python courses, lessons (with videos) and coding tasks"

    def handle(self, *args, **kwargs):
        self.stdout.write("Eski malumotlarni ochirish...")
        TaskModel.objects.all().delete()
        AnswerModel.objects.all().delete()
        QuestionModel.objects.all().delete()
        QuizModel.objects.all().delete()
        LessonModel.objects.all().delete()
        CourseModel.objects.all().delete()
        CategoryModel.objects.all().delete()

        # ── Kategoriyalar ──────────────────────────────────────────
        self.stdout.write("Kategoriyalar yaratilmoqda...")
        cats = {}
        for slug, name in [
            ("python-asoslari", "Python Asoslari"),
            ("web-dasturlash", "Web Dasturlash"),
            ("data-science", "Data Science"),
            ("machine-learning", "Machine Learning"),
            ("amaliyot", "Amaliyot"),
        ]:
            cats[slug] = CategoryModel.objects.create(name=name, slug=slug)

        course_cat = {
            "Python Asoslari": "python-asoslari",
            "Funksiyalar va Modullar": "python-asoslari",
            "Ma'lumotlar Tuzilmalari": "python-asoslari",
            "OOP - Obyektga Yo'naltirilgan Dasturlash": "python-asoslari",
            "Fayl va Xatolarni Boshqarish": "amaliyot",
            "Web Dasturlash — Django": "web-dasturlash",
            "Data Science — NumPy va Pandas": "data-science",
            "Machine Learning Asoslari": "machine-learning",
        }

        # ── 1. Barcha tasklar yaratiladi (course keyisiz) ──────────
        self.stdout.write("Tasklar yaratilmoqda...")

        # String darsi uchun maxsus task (Python Asoslari kursi)
        string_task = TaskModel.objects.create(
            title=STRING_LESSON_TASK["title"],
            description=STRING_LESSON_TASK["description"],
            test_code=STRING_LESSON_TASK["test_code"],
            starter_code=STRING_LESSON_TASK["starter_code"],
            difficulty=STRING_LESSON_TASK["difficulty"],
            expected_output=STRING_LESSON_TASK["expected_output"],
        )

        # Asosiy tasklar (course_key bilan keyinroq bog'lanadi)
        task_objects = []
        for t in PYTHON_TASKS:
            obj = TaskModel.objects.create(
                title=t["title"],
                description=t["description"],
                test_code=t["test_code"],
                starter_code=t.get("starter_code", ""),
                difficulty=t.get("difficulty", "Beginner"),
                expected_output=t.get("expected_output", ""),
            )
            task_objects.append((obj, t.get("course_key", "")))
            self.stdout.write(f"  >> Task: {t['title']} [{t['difficulty']}]")

        # course_key -> task ob'ektlari mapping (keyinroq kursga bog'lash uchun)
        course_tasks_map = {}  # course_title -> [TaskModel, ...]
        for obj, key in task_objects:
            course_tasks_map.setdefault(key, []).append(obj)

        # ── 2. Kurslar va darslar ──────────────────────────────────
        self.stdout.write("Kurslar yaratilmoqda...")

        # Dars tartib raqamiga ko'ra vazifa turi:
        # Juft tartib (2,4,6,8) → faqat mazmun (video+text)
        # 1 → quiz + related_task (agar bo'lsa)
        # 3,5,7 → required_task (quiz o'rniga)
        QUIZ_ORDERS = {1}
        TASK_ORDERS = {3, 5, 7}

        for course_data in PYTHON_COURSES:
            cat_slug = course_cat.get(course_data["title"], "amaliyot")
            base_slug = slugify(course_data["title"])
            course_slug = f"{base_slug[:40]}-{uuid.uuid4().hex[:6]}"

            course = CourseModel.objects.create(
                category=cats[cat_slug],
                title=course_data["title"],
                slug=course_slug,
                description=course_data["description"],
                price=course_data["price"],
                level=course_data["level"],
            )
            self.stdout.write(f"  >> Kurs: {course.title} [{course.level}]")

            # Bu kursga tegishli tasklar (related_task uchun)
            course_task_pool = course_tasks_map.get(course_data["title"], [])
            task_pool_idx = 0  # navbatdagi task indeksi

            # Kursga tegishli tasklarni kursga bog'lash
            for obj in course_task_pool:
                obj.course = course
                obj.save(update_fields=["course"])

            for lesson_data in course_data["lessons"]:
                order = lesson_data["order"]
                lesson_slug = f"{uuid.uuid4().hex[:8]}-{order}"

                # required_task: 3,5,7-darslar uchun kursning navbatdagi taski
                req_task = None
                if order in TASK_ORDERS:
                    if course_data["title"] == "Python Asoslari" and order == 3:
                        req_task = string_task
                    elif task_pool_idx < len(course_task_pool):
                        req_task = course_task_pool[task_pool_idx]
                        task_pool_idx += 1

                lesson = LessonModel.objects.create(
                    course=course,
                    title=lesson_data["title"],
                    slug=lesson_slug,
                    order=order,
                    content=lesson_data.get("content", ""),
                    video_url=lesson_data.get("video_url", ""),
                    required_task=req_task,
                )

                # Quiz: 1-dars (va 4-dars agar mavjud bo'lsa)
                if order in QUIZ_ORDERS and "quiz" in course_data:
                    # related_task: kursning birinchi taskini quiz bilan bog'lash
                    quiz_related = course_task_pool[0] if course_task_pool else None
                    # Python Asoslari 1-darsi uchun string_task
                    if course_data["title"] == "Python Asoslari":
                        quiz_related = string_task

                    quiz = QuizModel.objects.create(
                        lesson=lesson,
                        title=f"{course_data['title']} - Kirish Testi",
                        related_task=quiz_related,
                    )
                    for q in course_data["quiz"]["questions"]:
                        question = QuestionModel.objects.create(quiz=quiz, text=q["text"])
                        for i, ans in enumerate(q["answers"]):
                            AnswerModel.objects.create(
                                question=question,
                                text=ans,
                                is_correct=(i == q["correct"]),
                            )
                    if quiz_related:
                        self.stdout.write(
                            f"     [QUIZ -> MASALA] {lesson.title} >> {quiz_related.title}"
                        )

                if req_task:
                    self.stdout.write(
                        f"     [MAJBURIY MASALA] {lesson.title} >> {req_task.title}"
                    )

        self.stdout.write(self.style.SUCCESS(
            f"\nMuvaffaqiyatli! "
            f"{len(PYTHON_COURSES)} ta kurs, "
            f"{sum(len(c['lessons']) for c in PYTHON_COURSES)} ta dars, "
            f"{len(PYTHON_TASKS)} ta task yaratildi."
        ))
