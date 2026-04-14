"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { CheckCircle2, XCircle, ChevronRight, Trophy } from "lucide-react"
import { cn } from "@/lib/utils"
import type { Question } from "@/lib/data"

interface LessonQuizProps {
  questions: Question[]
  onComplete: () => void
}

export function LessonQuiz({ questions, onComplete }: LessonQuizProps) {
  const [currentQuestion, setCurrentQuestion] = useState(0)
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null)
  const [showResult, setShowResult] = useState(false)
  const [answers, setAnswers] = useState<number[]>([])
  const [quizComplete, setQuizComplete] = useState(false)

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
        setQuizComplete(true)
        onComplete()
      }
    }
  }

  const handleRetry = () => {
    setCurrentQuestion(0)
    setSelectedAnswer(null)
    setShowResult(false)
    setAnswers([])
    setQuizComplete(false)
  }

  // Calculate score
  const correctCount = answers.filter(
    (answer, index) => answer === questions[index].correctAnswer
  ).length
  const score = questions.length > 0 ? Math.round((correctCount / questions.length) * 100) : 0

  if (quizComplete) {
    return (
      <Card className="max-w-lg mx-auto text-center">
        <CardHeader>
          <div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-success/20 mb-4">
            <Trophy className="h-8 w-8 text-success" />
          </div>
          <h2 className="text-xl font-bold">Test tugallandi!</h2>
        </CardHeader>
        <CardContent>
          <p className="text-4xl font-bold mb-2">{score}%</p>
          <p className="text-muted-foreground mb-4">
            {correctCount} / {questions.length} to&apos;g&apos;ri javob
          </p>
          {score >= 70 ? (
            <div className="rounded-lg bg-success/10 p-3">
              <p className="text-sm text-success">Ajoyib natija!</p>
            </div>
          ) : (
            <div className="rounded-lg bg-warning/10 p-3">
              <p className="text-sm text-muted-foreground">
                Mavzuni qayta ko&apos;rib chiqishingiz mumkin.
              </p>
            </div>
          )}
        </CardContent>
        <CardFooter>
          <Button variant="outline" onClick={handleRetry} className="w-full">
            Qayta urinish
          </Button>
        </CardFooter>
      </Card>
    )
  }

  return (
    <div className="max-w-2xl mx-auto">
      {/* Progress */}
      <div className="mb-6">
        <div className="flex items-center justify-between text-sm mb-2">
          <span className="text-muted-foreground">
            Savol {currentQuestion + 1} / {questions.length}
          </span>
          <span className="font-medium">{Math.round(progress)}%</span>
        </div>
        <Progress value={progress} className="h-2" />
      </div>

      {/* Question */}
      <Card>
        <CardHeader>
          <h3 className="text-lg font-medium">{question.question}</h3>
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
                  "hover:border-primary/50 focus:outline-none",
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
                {currentQuestion < questions.length - 1 ? "Keyingi" : "Tugatish"}
                <ChevronRight className="h-4 w-4" />
              </>
            ) : (
              "Tekshirish"
            )}
          </Button>
        </CardFooter>
      </Card>
    </div>
  )
}
