"use client"

import { useState } from "react"
import { useAppStore } from "@/lib/store"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { 
  CheckCircle2, XCircle, ChevronRight, Trophy, 
  RefreshCw, ArrowRight, Sparkles
} from "lucide-react"
import { cn } from "@/lib/utils"

export function PlacementTest() {
  const { selectedCourse, setView, completePlacementTest, skipCourse } = useAppStore()
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [answers, setAnswers] = useState<number[]>([])
  const [testComplete, setTestComplete] = useState(false)

  if (!selectedCourse) return null

  const questions = selectedCourse.placementTest
  const question = questions[currentQuestion]
  const progress = ((currentQuestion + 1) / questions.length) * 100

  const handleSelectAnswer = (index: number) => {
    if (showResult) return
    setSelectedAnswer(index)
  }

  const handleConfirm = () => {
    if (selectedAnswer === null) return

    if (!showResult) {
      setShowResult(true)
    } else {
      const newAnswers = [...answers, selectedAnswer]
      setAnswers(newAnswers)

      if (currentQuestion < questions.length - 1) {
        setCurrentQuestion(currentQuestion + 1)
        setSelectedAnswer(null)
        setShowResult(false)
      } else {
        // Calculate score
        const correctCount = newAnswers.filter(
          (answer, index) => answer === questions[index].correctAnswer
        ).length
        const score = Math.round((correctCount / questions.length) * 100)
        const passed = score >= 80

        completePlacementTest(selectedCourse.id, score, passed)
        setTestComplete(true)
      }
    }
  }

  const handleSkipCourse = () => {
    skipCourse(selectedCourse.id)
    setView('courses')
  }

  const handleTakeCourse = () => {
    setView('course')
  }

  const handleRetry = () => {
    setCurrentQuestion(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setAnswers([])
    setTestComplete(false)
  }

  // Calculate final score
  const correctCount = answers.filter(
    (answer, index) => answer === questions[index].correctAnswer
  ).length
  const finalScore = Math.round((correctCount / questions.length) * 100)
  const passed = finalScore >= 80

  if (testComplete) {
    return (
      <div className="min-h-screen py-8 px-4 flex items-center justify-center">
        <Card className="w-full max-w-lg text-center">
          <CardHeader className="pb-2">
            <div className={cn(
              "mx-auto flex h-20 w-20 items-center justify-center rounded-full mb-4",
              passed ? "bg-success/20" : "bg-warning/20"
            )}>
              <Trophy className={cn(
                "h-10 w-10",
                passed ? "text-success" : "text-warning"
              )} />
            </div>
            <h2 className="text-2xl font-bold">
              {passed ? "Ajoyib natija!" : "Yaxshi urinish!"}
            </h2>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <p className="text-5xl font-bold mb-2">
                {finalScore}%
              </p>
              <p className="text-muted-foreground">
                {correctCount} / {questions.length} to&apos;g&apos;ri javob
              </p>
            </div>

            {passed ? (
              <div className="rounded-lg bg-success/10 p-4">
                <div className="flex items-center justify-center gap-2 text-success mb-2">
                  <Sparkles className="h-5 w-5" />
                  <span className="font-medium">Tabriklaymiz!</span>
                </div>
                <p className="text-sm text-muted-foreground">
                  Siz bu mavzuni yaxshi bilasiz. Kursni o&apos;tkazib yuborishingiz 
                  yoki takrorlash uchun o&apos;tishingiz mumkin.
                </p>
              </div>
            ) : (
              <div className="rounded-lg bg-warning/10 p-4">
                <p className="text-sm text-muted-foreground">
                  80% va undan yuqori ball olish kerak edi. 
                  Bu kursni o&apos;rganishni tavsiya qilamiz.
                </p>
              </div>
            )}
          </CardContent>
          <CardFooter className="flex-col gap-3">
            {passed ? (
              <>
                <Button onClick={handleSkipCourse} className="w-full gap-2">
                  <ArrowRight className="h-4 w-4" />
                  Kursni o&apos;tkazib yuborish
                </Button>
                <Button variant="outline" onClick={handleTakeCourse} className="w-full">
                  Baribir o&apos;rganish
                </Button>
              </>
            ) : (
              <>
                <Button onClick={handleTakeCourse} className="w-full gap-2">
                  <ArrowRight className="h-4 w-4" />
                  Kursni boshlash
                </Button>
                <Button variant="outline" onClick={handleRetry} className="w-full gap-2">
                  <RefreshCw className="h-4 w-4" />
                  Qayta urinish
                </Button>
              </>
            )}
          </CardFooter>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-2xl">
        {/* Header */}
        <div className="mb-8">
          <Badge variant="outline" className="mb-3">
            {selectedCourse.title} - Darajani aniqlash testi
          </Badge>
          <h1 className="text-2xl font-bold mb-4">Bilimingizni tekshiring</h1>
          
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">
                Savol {currentQuestion + 1} / {questions.length}
              </span>
              <span className="font-medium">{Math.round(progress)}%</span>
            </div>
            <Progress value={progress} className="h-2" />
          </div>
        </div>

        {/* Question Card */}
        <Card>
          <CardHeader>
            <h2 className="text-lg font-medium">{question.question}</h2>
          </CardHeader>
          <CardContent className="space-y-3">
            {question.options.map((option, index) => {
              const isSelected = selectedAnswer === index
              const isCorrect = index === question.correctAnswer
              const showCorrect = showResult && isCorrect
              const showWrong = showResult && isSelected && !isCorrect

              return (
                <button
                  key={index}
                  onClick={() => handleSelectAnswer(index)}
                  disabled={showResult}
                  className={cn(
                    "w-full text-left p-4 rounded-lg border-2 transition-all",
                    "hover:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/20",
                    isSelected && !showResult && "border-primary bg-primary/5",
                    showCorrect && "border-success bg-success/10",
                    showWrong && "border-destructive bg-destructive/10",
                    !isSelected && !showCorrect && !showWrong && "border-border"
                  )}
                >
                  <div className="flex items-center gap-3">
                    <div className={cn(
                      "flex h-8 w-8 shrink-0 items-center justify-center rounded-full border-2 text-sm font-medium",
                      isSelected && !showResult && "border-primary text-primary",
                      showCorrect && "border-success bg-success text-success-foreground",
                      showWrong && "border-destructive bg-destructive text-destructive-foreground",
                      !isSelected && !showCorrect && !showWrong && "border-muted-foreground/30"
                    )}>
                      {showCorrect ? (
                        <CheckCircle2 className="h-5 w-5" />
                      ) : showWrong ? (
                        <XCircle className="h-5 w-5" />
                      ) : (
                        String.fromCharCode(65 + index)
                      )}
                    </div>
                    <span className={cn(
                      showCorrect && "text-success font-medium",
                      showWrong && "text-destructive"
                    )}>
                      {option}
                    </span>
                  </div>
                </button>
              )
            })}

            {/* Explanation */}
            {showResult && question.explanation && (
              <div className="mt-4 rounded-lg bg-muted/50 p-4">
                <p className="text-sm text-muted-foreground">
                  <span className="font-medium text-foreground">Tushuntirish: </span>
                  {question.explanation}
                </p>
              </div>
            )}
          </CardContent>
          <CardFooter>
            <Button 
              onClick={handleConfirm}
              disabled={selectedAnswer === null}
              className="w-full gap-2"
            >
              {showResult ? (
                <>
                  {currentQuestion < questions.length - 1 ? "Keyingi savol" : "Natijani ko'rish"}
                  <ChevronRight className="h-4 w-4" />
                </>
              ) : (
                "Javobni tekshirish"
              )}
            </Button>
          </CardFooter>
        </Card>
      </div>
    </div>
  )
}
