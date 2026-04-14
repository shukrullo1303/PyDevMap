export interface Question {
  id: string
  question: string
  options: string[]
  correctAnswer: number
  explanation?: string
}

export interface Lesson {
  id: string
  title: string
  type: 'video' | 'text'
  content: string
  videoUrl?: string
  duration: string
  codeExercise?: {
    instructions: string
    starterCode: string
    expectedOutput: string
    hints: string[]
  }
  quiz?: Question[]
}

export interface Course {
  id: string
  title: string
  description: string
  level: 'Boshlang\'ich' | 'O\'rta' | 'Murakkab'
  duration: string
  lessonsCount: number
  icon: string
  color: string
  prerequisites: string[]
  placementTest: Question[]
  lessons: Lesson[]
  price: number
  isPurchased?: boolean
  progress?: number
}

export const courses: Course[] = [
  {
    id: 'python-basics',
    title: 'Python Asoslari',
    description: 'Python dasturlash tilining asosiy tushunchalari: o\'zgaruvchilar, ma\'lumot turlari, shartlar va sikllar',
    level: 'Boshlang\'ich',
    duration: '8 soat',
    lessonsCount: 12,
    icon: '🐍',
    color: 'from-green-500 to-emerald-600',
    prerequisites: [],
    price: 0,
    placementTest: [
      {
        id: 'pb-1',
        question: 'Python\'da o\'zgaruvchi e\'lon qilish uchun qaysi kalit so\'z ishlatiladi?',
        options: ['var', 'let', 'Kalit so\'z kerak emas', 'define'],
        correctAnswer: 2,
        explanation: 'Python\'da o\'zgaruvchi e\'lon qilish uchun maxsus kalit so\'z kerak emas, shunchaki nom = qiymat yoziladi'
      },
      {
        id: 'pb-2',
        question: 'print("Salom") buyrug\'i nima qiladi?',
        options: ['Faylga yozadi', 'Ekranga chiqaradi', 'O\'zgaruvchi yaratadi', 'Xatolik beradi'],
        correctAnswer: 1,
        explanation: 'print() funksiyasi ma\'lumotni ekranga (konsolga) chiqaradi'
      },
      {
        id: 'pb-3',
        question: 'Python\'da qaysi ma\'lumot turi butun sonlarni ifodalaydi?',
        options: ['str', 'float', 'int', 'bool'],
        correctAnswer: 2,
        explanation: 'int (integer) ma\'lumot turi butun sonlarni ifodalaydi'
      },
      {
        id: 'pb-4',
        question: 'if-else konstruksiyasi nima uchun ishlatiladi?',
        options: ['Sikllar uchun', 'Shartli operatorlar uchun', 'Funksiyalar uchun', 'Import uchun'],
        correctAnswer: 1,
        explanation: 'if-else konstruksiyasi shartga qarab turli kod bloklarini bajarish uchun ishlatiladi'
      },
      {
        id: 'pb-5',
        question: 'for sikli nima uchun ishlatiladi?',
        options: ['Funksiya yaratish', 'Takrorlanuvchi amallar', 'O\'zgaruvchi e\'lon qilish', 'Dasturni to\'xtatish'],
        correctAnswer: 1,
        explanation: 'for sikli ma\'lum bir ketma-ketlik bo\'yicha takrorlanuvchi amallarni bajarish uchun ishlatiladi'
      }
    ],
    lessons: [
      {
        id: 'pb-l1',
        title: 'Python\'ga Kirish',
        type: 'video',
        content: `# Python\'ga Kirish

Python - bu o'rganish oson, ammo kuchli dasturlash tili. U 1991-yilda Guido van Rossum tomonidan yaratilgan.

## Nima uchun Python?

- **Sodda sintaksis** - o'qish va yozish oson
- **Ko'p qo'llanilishi** - web, data science, AI, automation
- **Katta jamoa** - ko'p kutubxonalar va yordamlar

## Birinchi dasturingiz

\`\`\`python
print("Salom, Dunyo!")
\`\`\`

Bu sizning birinchi Python dasturingiz! \`print()\` funksiyasi ekranga matn chiqaradi.`,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        duration: '15 min',
        codeExercise: {
          instructions: 'Ekranga "Salom, Python!" so\'zini chiqaring',
          starterCode: '# Quyidagi qatorga kod yozing\n',
          expectedOutput: 'Salom, Python!',
          hints: ['print() funksiyasidan foydalaning', 'Matnni qo\'shtirnoq ichida yozing']
        }
      },
      {
        id: 'pb-l2',
        title: 'O\'zgaruvchilar va Ma\'lumot Turlari',
        type: 'text',
        content: `# O'zgaruvchilar va Ma'lumot Turlari

## O'zgaruvchi nima?

O'zgaruvchi - bu ma'lumotni saqlash uchun nomlangan joy. Python'da o'zgaruvchi yaratish juda oddiy:

\`\`\`python
ism = "Ali"
yosh = 25
ball = 95.5
talaba = True
\`\`\`

## Asosiy ma'lumot turlari

| Tur | Tavsif | Misol |
|-----|--------|-------|
| str | Matn (string) | "Salom" |
| int | Butun son | 42 |
| float | O'nli son | 3.14 |
| bool | Mantiqiy | True/False |

## Tip tekshirish

\`\`\`python
x = 10
print(type(x))  # <class 'int'>
\`\`\``,
        duration: '20 min',
        quiz: [
          {
            id: 'pb-l2-q1',
            question: 'yosh = 25 qatorida "yosh" nima?',
            options: ['Funksiya', 'O\'zgaruvchi', 'Kalit so\'z', 'Operator'],
            correctAnswer: 1
          }
        ],
        codeExercise: {
          instructions: 'Ismingizni saqlash uchun o\'zgaruvchi yarating va uni ekranga chiqaring',
          starterCode: '# O\'zgaruvchi yarating\n\n# Ekranga chiqaring\n',
          expectedOutput: 'Sizning ismingiz',
          hints: ['ism = "..." ko\'rinishida yozing', 'print(ism) bilan chiqaring']
        }
      },
      {
        id: 'pb-l3',
        title: 'Shartli Operatorlar',
        type: 'text',
        content: `# Shartli Operatorlar

## if-else

Shartli operatorlar dasturingizga qaror qabul qilish imkoniyatini beradi.

\`\`\`python
yosh = 18

if yosh >= 18:
    print("Siz kattasiz")
else:
    print("Siz yoshsiz")
\`\`\`

## elif

Ko'p shartlarni tekshirish uchun \`elif\` ishlatiladi:

\`\`\`python
ball = 85

if ball >= 90:
    print("A baho")
elif ball >= 80:
    print("B baho")
elif ball >= 70:
    print("C baho")
else:
    print("Qayta topshiring")
\`\`\`

## Taqqoslash operatorlari

- \`==\` Teng
- \`!=\` Teng emas
- \`>\` Katta
- \`<\` Kichik
- \`>=\` Katta yoki teng
- \`<=\` Kichik yoki teng`,
        duration: '25 min',
        codeExercise: {
          instructions: 'Berilgan ball asosida bahoni aniqlang (90+ = A, 80+ = B, 70+ = C, qolgan = D)',
          starterCode: 'ball = 85\n\n# Shartli operator yozing\n',
          expectedOutput: 'B baho',
          hints: ['if-elif-else strukturasidan foydalaning', 'ball >= 90 dan boshlang']
        }
      }
    ]
  },
  {
    id: 'python-functions',
    title: 'Funksiyalar va Modullar',
    description: 'Funksiyalar yaratish, parametrlar, qaytarish qiymatlari va modullar bilan ishlash',
    level: 'Boshlang\'ich',
    duration: '6 soat',
    lessonsCount: 8,
    icon: '⚙️',
    color: 'from-blue-500 to-cyan-600',
    prerequisites: ['python-basics'],
    price: 49000,
    placementTest: [
      {
        id: 'pf-1',
        question: 'Funksiya yaratish uchun qaysi kalit so\'z ishlatiladi?',
        options: ['function', 'def', 'func', 'create'],
        correctAnswer: 1,
        explanation: 'Python\'da funksiya yaratish uchun "def" kalit so\'zi ishlatiladi'
      },
      {
        id: 'pf-2',
        question: 'return kalit so\'zi nima qiladi?',
        options: ['Funksiyani to\'xtatadi', 'Qiymat qaytaradi', 'Xatolik beradi', 'Sikl boshlaydi'],
        correctAnswer: 1,
        explanation: 'return funksiyadan qiymat qaytarish uchun ishlatiladi'
      },
      {
        id: 'pf-3',
        question: 'import math buyrug\'i nima qiladi?',
        options: ['Yangi funksiya yaratadi', 'math modulini ulaydi', 'Matematik amal bajaradi', 'O\'zgaruvchi yaratadi'],
        correctAnswer: 1,
        explanation: 'import buyrug\'i tashqi modullarni dasturingizga ulash uchun ishlatiladi'
      }
    ],
    lessons: [
      {
        id: 'pf-l1',
        title: 'Funksiyalar Asoslari',
        type: 'video',
        content: `# Funksiyalar Asoslari

Funksiya - bu qayta ishlatish mumkin bo'lgan kod bloki.

## Funksiya yaratish

\`\`\`python
def salomlash():
    print("Salom!")

# Funksiyani chaqirish
salomlash()
\`\`\`

## Parametrli funksiya

\`\`\`python
def salomlash(ism):
    print(f"Salom, {ism}!")

salomlash("Ali")  # Salom, Ali!
\`\`\``,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        duration: '20 min',
        codeExercise: {
          instructions: 'Ikki sonni qo\'shib, natijani qaytaruvchi funksiya yarating',
          starterCode: 'def qoshish(a, b):\n    # Kodingizni yozing\n    pass\n\nnatija = qoshish(5, 3)\nprint(natija)',
          expectedOutput: '8',
          hints: ['return kalit so\'zidan foydalaning', 'a + b ni qaytaring']
        }
      }
    ]
  },
  {
    id: 'python-oop',
    title: 'OOP - Obyektga Yo\'naltirilgan Dasturlash',
    description: 'Klasslar, obyektlar, meros olish, inkapsulyatsiya va polimorfizm',
    level: 'O\'rta',
    duration: '10 soat',
    lessonsCount: 15,
    icon: '🏗️',
    color: 'from-purple-500 to-pink-600',
    prerequisites: ['python-basics', 'python-functions'],
    price: 99000,
    placementTest: [
      {
        id: 'oop-1',
        question: 'Klass nima?',
        options: ['Funksiya turi', 'Obyekt shabloni', 'Ma\'lumot turi', 'Modul'],
        correctAnswer: 1,
        explanation: 'Klass - bu obyektlar uchun shablon yoki chizma'
      },
      {
        id: 'oop-2',
        question: '__init__ metodi nima uchun ishlatiladi?',
        options: ['Klassni o\'chirish', 'Obyektni boshlash', 'Meros olish', 'Metodlarni chaqirish'],
        correctAnswer: 1,
        explanation: '__init__ konstruktor metodi bo\'lib, obyekt yaratilganda avtomatik chaqiriladi'
      },
      {
        id: 'oop-3',
        question: 'self kalit so\'zi nimani bildiradi?',
        options: ['Klassning o\'zini', 'Joriy obyektni', 'Ota klassni', 'Yangi obyektni'],
        correctAnswer: 1,
        explanation: 'self joriy obyektga murojaat qilish uchun ishlatiladi'
      }
    ],
    lessons: [
      {
        id: 'oop-l1',
        title: 'Klasslar va Obyektlar',
        type: 'text',
        content: `# Klasslar va Obyektlar

## Klass yaratish

\`\`\`python
class Mashina:
    def __init__(self, model, rang):
        self.model = model
        self.rang = rang
    
    def malumot(self):
        return f"{self.rang} {self.model}"

# Obyekt yaratish
mening_mashinam = Mashina("Tesla", "qora")
print(mening_mashinam.malumot())
\`\`\``,
        duration: '30 min',
        codeExercise: {
          instructions: 'Talaba klassi yarating: ism va yosh atributlari, salomlash() metodi',
          starterCode: 'class Talaba:\n    # Kodingizni yozing\n    pass\n\ntalaba = Talaba("Ali", 20)\nprint(talaba.salomlash())',
          expectedOutput: 'Salom, men Ali, yoshim 20',
          hints: ['__init__ metodini yarating', 'self.ism va self.yosh atributlarini yarating']
        }
      }
    ]
  },
  {
    id: 'python-data',
    title: 'Ma\'lumotlar Tuzilmalari',
    description: 'Listlar, tuplar, to\'plamlar, lug\'atlar va ular bilan ishlash',
    level: 'Boshlang\'ich',
    duration: '7 soat',
    lessonsCount: 10,
    icon: '📊',
    color: 'from-orange-500 to-red-600',
    prerequisites: ['python-basics'],
    price: 59000,
    placementTest: [
      {
        id: 'pd-1',
        question: 'List yaratish uchun qaysi qavslar ishlatiladi?',
        options: ['()', '{}', '[]', '<>'],
        correctAnswer: 2,
        explanation: 'Python\'da list yaratish uchun kvadrat qavslar [] ishlatiladi'
      },
      {
        id: 'pd-2',
        question: 'Dictionary (lug\'at) nima saqlaydi?',
        options: ['Faqat sonlar', 'Kalit-qiymat juftliklari', 'Faqat matnlar', 'Faqat listlar'],
        correctAnswer: 1,
        explanation: 'Dictionary kalit-qiymat juftliklarini saqlaydi'
      }
    ],
    lessons: [
      {
        id: 'pd-l1',
        title: 'Listlar bilan Ishlash',
        type: 'video',
        content: `# Listlar

List - bu tartiblangan, o'zgartirilishi mumkin bo'lgan to'plam.

\`\`\`python
mevalar = ["olma", "banan", "uzum"]
mevalar.append("anor")
print(mevalar[0])  # olma
\`\`\``,
        videoUrl: 'https://www.youtube.com/embed/dQw4w9WgXcQ',
        duration: '25 min',
        codeExercise: {
          instructions: 'Sonlar listini yarating va yig\'indisini hisoblang',
          starterCode: 'sonlar = [1, 2, 3, 4, 5]\n\n# Yig\'indini hisoblang\nyigindi = 0\n',
          expectedOutput: '15',
          hints: ['for sikli yoki sum() funksiyasidan foydalaning']
        }
      }
    ]
  },
  {
    id: 'python-web',
    title: 'Web Dasturlash (Flask/Django)',
    description: 'Flask va Django frameworklari bilan web ilovalar yaratish',
    level: 'O\'rta',
    duration: '15 soat',
    lessonsCount: 20,
    icon: '🌐',
    color: 'from-teal-500 to-green-600',
    prerequisites: ['python-basics', 'python-functions', 'python-oop'],
    price: 149000,
    placementTest: [
      {
        id: 'pw-1',
        question: 'Flask nima?',
        options: ['Ma\'lumotlar bazasi', 'Web framework', 'Kutubxona', 'IDE'],
        correctAnswer: 1,
        explanation: 'Flask - Python uchun yengil web framework'
      }
    ],
    lessons: []
  },
  {
    id: 'python-data-science',
    title: 'Data Science va ML',
    description: 'NumPy, Pandas, Matplotlib va Machine Learning asoslari',
    level: 'Murakkab',
    duration: '20 soat',
    lessonsCount: 25,
    icon: '🤖',
    color: 'from-indigo-500 to-purple-600',
    prerequisites: ['python-basics', 'python-functions', 'python-data'],
    price: 199000,
    placementTest: [
      {
        id: 'pds-1',
        question: 'Pandas\'da DataFrame nima?',
        options: ['Rasm turi', 'Jadval tuzilmasi', 'Funksiya', 'Sikl turi'],
        correctAnswer: 1,
        explanation: 'DataFrame - jadval ko\'rinishidagi ma\'lumotlar tuzilmasi'
      }
    ],
    lessons: []
  }
]

export const roadmapSteps = [
  { id: 1, title: 'Python Asoslari', courseId: 'python-basics', required: true },
  { id: 2, title: 'Funksiyalar', courseId: 'python-functions', required: true },
  { id: 3, title: 'Ma\'lumotlar Tuzilmalari', courseId: 'python-data', required: true },
  { id: 4, title: 'OOP', courseId: 'python-oop', required: true },
  { id: 5, title: 'Web Dasturlash', courseId: 'python-web', required: false },
  { id: 6, title: 'Data Science', courseId: 'python-data-science', required: false },
]
