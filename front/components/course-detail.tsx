"use client"

import { useAppStore } from "@/lib/store"
import { courses } from "@/lib/data"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { 
  Clock, BookOpen, Play, Check, Lock, 
  FileText, Video, Code, Trophy, Zap
} from "lucide-react"
import { cn } from "@/lib/utils"

export function CourseDetail() {
  const { 
    selectedCourse, 
    setView, 
    selectLesson, 
    getProgress, 
    purchaseCourse 
  } = useAppStore()

  if (!selectedCourse) return null

  const progress = getProgress(selectedCourse.id)
  const isPurchased = progress?.isPurchased || selectedCourse.price === 0
  const testScore = progress?.testScore
  const completedLessons = progress?.completedLessons || []

  const handleStartPlacementTest = () => {
    setView('placement-test')
  }

  const handlePurchase = () => {
    purchaseCourse(selectedCourse.id)
  }

  const handleStartLesson = (lessonId: string) => {
    const lesson = selectedCourse.lessons.find(l => l.id === lessonId)
    if (lesson) {
      selectLesson(lesson)
      setView('lesson')
    }
  }

  // Check prerequisites
  const prerequisitesMet = selectedCourse.prerequisites.every(prereqId => {
    const prereqProgress = getProgress(prereqId)
    return prereqProgress?.skipped || prereqProgress?.isPurchased
  })

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* Course Header */}
        <div className="mb-8">
          <div className="flex flex-col md:flex-row md:items-start gap-6">
            <div className={cn(
              "flex h-20 w-20 shrink-0 items-center justify-center rounded-2xl text-4xl",
              `bg-gradient-to-br ${selectedCourse.color}`
            )}>
              {selectedCourse.icon}
            </div>
            
            <div className="flex-1">
              <div className="flex flex-wrap items-center gap-3 mb-2">
                <Badge variant={
                  selectedCourse.level === "Boshlang'ich" ? "secondary" :
                  selectedCourse.level === "O'rta" ? "outline" : "default"
                }>
                  {selectedCourse.level}
                </Badge>
                {isPurchased && (
                  <Badge className="bg-success text-success-foreground">
                    <Check className="h-3 w-3 mr-1" />
                    Sotib olingan
                  </Badge>
                )}
                {testScore !== undefined && (
                  <Badge variant="outline" className={cn(
                    testScore >= 80 ? "border-success text-success" : "border-warning text-warning"
                  )}>
                    <Trophy className="h-3 w-3 mr-1" />
                    Test: {testScore}%
                  </Badge>
                )}
              </div>
              
              <h1 className="text-3xl font-bold mb-3">{selectedCourse.title}</h1>
              <p className="text-muted-foreground mb-4">{selectedCourse.description}</p>
              
              <div className="flex flex-wrap items-center gap-4 text-sm">
                <div className="flex items-center gap-1 text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  {selectedCourse.duration}
                </div>
                <div className="flex items-center gap-1 text-muted-foreground">
                  <BookOpen className="h-4 w-4" />
                  {selectedCourse.lessonsCount} ta dars
                </div>
                {completedLessons.length > 0 && (
                  <div className="flex items-center gap-1 text-success">
                    <Check className="h-4 w-4" />
                    {completedLessons.length}/{selectedCourse.lessons.length} tugallangan
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Prerequisites Warning */}
        {!prerequisitesMet && (
          <Card className="mb-6 border-destructive/50 bg-destructive/5">
            <CardContent className="py-4">
              <div className="flex items-start gap-3">
                <Lock className="h-5 w-5 text-destructive mt-0.5" />
                <div>
                  <p className="font-medium text-foreground mb-1">Talab qilingan kurslar</p>
                  <p className="text-sm text-muted-foreground mb-2">
                    Bu kursni boshlash uchun quyidagi kurslarni tugatishingiz kerak:
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {selectedCourse.prerequisites.map(prereqId => {
                      const prereq = courses.find(c => c.id === prereqId)
                      return prereq ? (
                        <Badge key={prereqId} variant="outline">{prereq.title}</Badge>
                      ) : null
                    })}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Placement Test Section */}
        {prerequisitesMet && !isPurchased && selectedCourse.price > 0 && (
          <Card className="mb-6 border-primary/30 bg-primary/5">
            <CardContent className="py-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="flex items-start gap-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/20">
                    <Zap className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <h3 className="font-semibold text-lg mb-1">Darajangizni tekshiring</h3>
                    <p className="text-sm text-muted-foreground">
                      Test yechib, bilimingizni tekshiring. 80% va undan yuqori ball olsangiz, 
                      bu kursni o&apos;tkazib yuborishingiz mumkin.
                    </p>
                  </div>
                </div>
                <Button onClick={handleStartPlacementTest} className="shrink-0 gap-2">
                  <Play className="h-4 w-4" />
                  Testni boshlash
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Purchase Section */}
        {prerequisitesMet && !isPurchased && selectedCourse.price > 0 && (
          <Card className="mb-6">
            <CardContent className="py-6">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                  <p className="text-2xl font-bold">
                    {selectedCourse.price.toLocaleString()} so&apos;m
                  </p>
                  <p className="text-sm text-muted-foreground">
                    To&apos;liq kurnga kirish
                  </p>
                </div>
                <Button onClick={handlePurchase} size="lg" className="gap-2">
                  Sotib olish
                </Button>
              </div>
            </CardContent>
          </Card>
        )}

        {/* Lessons List */}
        <div className="mb-8">
          <h2 className="text-xl font-semibold mb-4">Darslar</h2>
          
          {selectedCourse.lessons.length === 0 ? (
            <Card>
              <CardContent className="py-12 text-center">
                <p className="text-muted-foreground">Darslar tez orada qo&apos;shiladi</p>
              </CardContent>
            </Card>
          ) : (
            <div className="space-y-3">
              {selectedCourse.lessons.map((lesson, index) => {
                const isCompleted = completedLessons.includes(lesson.id)
                const isLocked = !isPurchased && selectedCourse.price > 0 && index > 0

                return (
                  <Card 
                    key={lesson.id}
                    className={cn(
                      "transition-all",
                      isCompleted && "border-success/30 bg-success/5",
                      !isLocked && "cursor-pointer hover:border-primary/50"
                    )}
                    onClick={() => !isLocked && handleStartLesson(lesson.id)}
                  >
                    <CardContent className="py-4">
                      <div className="flex items-center gap-4">
                        {/* Lesson Number / Status */}
                        <div className={cn(
                          "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg text-sm font-medium",
                          isCompleted 
                            ? "bg-success text-success-foreground"
                            : isLocked
                              ? "bg-muted text-muted-foreground"
                              : "bg-secondary text-secondary-foreground"
                        )}>
                          {isCompleted ? (
                            <Check className="h-5 w-5" />
                          ) : isLocked ? (
                            <Lock className="h-4 w-4" />
                          ) : (
                            index + 1
                          )}
                        </div>

                        {/* Lesson Info */}
                        <div className="flex-1 min-w-0">
                          <div className="flex items-center gap-2 mb-1">
                            <h3 className={cn(
                              "font-medium truncate",
                              isLocked && "text-muted-foreground"
                            )}>
                              {lesson.title}
                            </h3>
                            <Badge variant="outline" className="shrink-0">
                              {lesson.type === 'video' ? (
                                <><Video className="h-3 w-3 mr-1" />Video</>
                              ) : (
                                <><FileText className="h-3 w-3 mr-1" />Matn</>
                              )}
                            </Badge>
                          </div>
                          <div className="flex items-center gap-3 text-sm text-muted-foreground">
                            <span>{lesson.duration}</span>
                            {lesson.codeExercise && (
                              <span className="flex items-center gap-1">
                                <Code className="h-3 w-3" />
                                Kod mashq
                              </span>
                            )}
                            {lesson.quiz && lesson.quiz.length > 0 && (
                              <span>{lesson.quiz.length} ta savol</span>
                            )}
                          </div>
                        </div>

                        {/* Action */}
                        {!isLocked && (
                          <Button variant="ghost" size="icon" className="shrink-0">
                            <Play className="h-4 w-4" />
                          </Button>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                )
              })}
            </div>
          )}
        </div>

        {/* What You'll Learn */}
        <Card>
          <CardHeader>
            <h2 className="text-xl font-semibold">Nimalarni o&apos;rganasiz</h2>
          </CardHeader>
          <CardContent>
            <ul className="grid md:grid-cols-2 gap-3">
              {[
                "Python sintaksisi va asosiy tushunchalar",
                "Amaliy masalalar yechish",
                "Kod yozish ko'nikmalari",
                "Real loyihalar yaratish"
              ].map((item, i) => (
                <li key={i} className="flex items-start gap-2">
                  <Check className="h-5 w-5 text-success shrink-0 mt-0.5" />
                  <span className="text-muted-foreground">{item}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
