"use client"

import { useState } from "react"
import { useAppStore } from "@/lib/store"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  Play, CheckCircle2, ChevronRight, ChevronLeft,
  Video, FileText, Code, Lightbulb, RotateCcw
} from "lucide-react"
import { cn } from "@/lib/utils"
import { CodeEditor } from "./code-editor"
import { LessonQuiz } from "./lesson-quiz"
import ReactMarkdown from "react-markdown"

export function LessonView() {
  const { 
    selectedCourse, 
    selectedLesson, 
    setView, 
    selectLesson,
    completeLesson,
    getProgress
  } = useAppStore()

  const [activeTab, setActiveTab] = useState<string>("content")
  const [codeCompleted, setCodeCompleted] = useState(false)
  const [quizCompleted, setQuizCompleted] = useState(false)

  if (!selectedCourse || !selectedLesson) return null

  const progress = getProgress(selectedCourse.id)
  const isCompleted = progress?.completedLessons?.includes(selectedLesson.id)

  const lessonIndex = selectedCourse.lessons.findIndex(l => l.id === selectedLesson.id)
  const prevLesson = lessonIndex > 0 ? selectedCourse.lessons[lessonIndex - 1] : null
  const nextLesson = lessonIndex < selectedCourse.lessons.length - 1 
    ? selectedCourse.lessons[lessonIndex + 1] 
    : null

  const handleComplete = () => {
    completeLesson(selectedCourse.id, selectedLesson.id)
    if (nextLesson) {
      selectLesson(nextLesson)
      setActiveTab("content")
      setCodeCompleted(false)
      setQuizCompleted(false)
    } else {
      setView('course')
    }
  }

  const handlePrevious = () => {
    if (prevLesson) {
      selectLesson(prevLesson)
      setActiveTab("content")
      setCodeCompleted(false)
      setQuizCompleted(false)
    }
  }

  const handleNext = () => {
    if (nextLesson) {
      selectLesson(nextLesson)
      setActiveTab("content")
      setCodeCompleted(false)
      setQuizCompleted(false)
    }
  }

  const canComplete = (!selectedLesson.codeExercise || codeCompleted) && 
    (!selectedLesson.quiz || selectedLesson.quiz.length === 0 || quizCompleted)

  return (
    <div className="min-h-screen">
      {/* Lesson Header */}
      <div className="border-b border-border bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <Badge variant="outline">
                  {lessonIndex + 1} / {selectedCourse.lessons.length}
                </Badge>
                <Badge variant="outline">
                  {selectedLesson.type === 'video' ? (
                    <><Video className="h-3 w-3 mr-1" />Video</>
                  ) : (
                    <><FileText className="h-3 w-3 mr-1" />Matn</>
                  )}
                </Badge>
                {isCompleted && (
                  <Badge className="bg-success text-success-foreground">
                    <CheckCircle2 className="h-3 w-3 mr-1" />
                    Tugallangan
                  </Badge>
                )}
              </div>
              <h1 className="text-xl font-bold">{selectedLesson.title}</h1>
              <p className="text-sm text-muted-foreground">{selectedLesson.duration}</p>
            </div>

            <div className="flex items-center gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={handlePrevious}
                disabled={!prevLesson}
                className="gap-1"
              >
                <ChevronLeft className="h-4 w-4" />
                <span className="hidden sm:inline">Oldingi</span>
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handleNext}
                disabled={!nextLesson}
                className="gap-1"
              >
                <span className="hidden sm:inline">Keyingi</span>
                <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={setActiveTab} className="flex-1">
        <div className="border-b border-border bg-card sticky top-16 z-40">
          <div className="container mx-auto px-4">
            <TabsList className="h-12 bg-transparent p-0 border-none">
              <TabsTrigger 
                value="content"
                className="data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-4"
              >
                {selectedLesson.type === 'video' ? (
                  <><Video className="h-4 w-4 mr-2" />Video</>
                ) : (
                  <><FileText className="h-4 w-4 mr-2" />Dars</>
                )}
              </TabsTrigger>
              {selectedLesson.codeExercise && (
                <TabsTrigger 
                  value="code"
                  className="data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-4"
                >
                  <Code className="h-4 w-4 mr-2" />
                  Kod Mashq
                  {codeCompleted && <CheckCircle2 className="h-4 w-4 ml-2 text-success" />}
                </TabsTrigger>
              )}
              {selectedLesson.quiz && selectedLesson.quiz.length > 0 && (
                <TabsTrigger 
                  value="quiz"
                  className="data-[state=active]:border-b-2 data-[state=active]:border-primary rounded-none px-4"
                >
                  <Lightbulb className="h-4 w-4 mr-2" />
                  Test
                  {quizCompleted && <CheckCircle2 className="h-4 w-4 ml-2 text-success" />}
                </TabsTrigger>
              )}
            </TabsList>
          </div>
        </div>

        <div className="container mx-auto px-4 py-6">
          <TabsContent value="content" className="mt-0">
            {selectedLesson.type === 'video' && selectedLesson.videoUrl && (
              <div className="mb-6">
                <div className="aspect-video rounded-lg overflow-hidden bg-black">
                  <iframe
                    src={selectedLesson.videoUrl}
                    className="w-full h-full"
                    allowFullScreen
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                  />
                </div>
              </div>
            )}

            <Card>
              <CardContent className="py-6 prose prose-invert max-w-none">
                <ReactMarkdown
                  components={{
                    code({ className, children, ...props }) {
                      const match = /language-(\w+)/.exec(className || '')
                      const isInline = !match
                      return isInline ? (
                        <code className="bg-muted px-1.5 py-0.5 rounded text-sm" {...props}>
                          {children}
                        </code>
                      ) : (
                        <pre className="bg-[#1e1e2e] p-4 rounded-lg overflow-x-auto">
                          <code className={className} {...props}>
                            {children}
                          </code>
                        </pre>
                      )
                    },
                    h1: ({children}) => <h1 className="text-2xl font-bold text-foreground mb-4">{children}</h1>,
                    h2: ({children}) => <h2 className="text-xl font-semibold text-foreground mt-6 mb-3">{children}</h2>,
                    h3: ({children}) => <h3 className="text-lg font-medium text-foreground mt-4 mb-2">{children}</h3>,
                    p: ({children}) => <p className="text-muted-foreground mb-4 leading-relaxed">{children}</p>,
                    ul: ({children}) => <ul className="list-disc list-inside text-muted-foreground mb-4 space-y-1">{children}</ul>,
                    ol: ({children}) => <ol className="list-decimal list-inside text-muted-foreground mb-4 space-y-1">{children}</ol>,
                    li: ({children}) => <li className="text-muted-foreground">{children}</li>,
                    strong: ({children}) => <strong className="text-foreground font-semibold">{children}</strong>,
                    table: ({children}) => (
                      <div className="overflow-x-auto mb-4">
                        <table className="w-full border-collapse border border-border">{children}</table>
                      </div>
                    ),
                    th: ({children}) => <th className="border border-border bg-muted px-4 py-2 text-left text-foreground font-medium">{children}</th>,
                    td: ({children}) => <td className="border border-border px-4 py-2 text-muted-foreground">{children}</td>,
                  }}
                >
                  {selectedLesson.content}
                </ReactMarkdown>
              </CardContent>
            </Card>
          </TabsContent>

          {selectedLesson.codeExercise && (
            <TabsContent value="code" className="mt-0">
              <CodeEditor 
                exercise={selectedLesson.codeExercise}
                onComplete={() => setCodeCompleted(true)}
              />
            </TabsContent>
          )}

          {selectedLesson.quiz && selectedLesson.quiz.length > 0 && (
            <TabsContent value="quiz" className="mt-0">
              <LessonQuiz
                questions={selectedLesson.quiz}
                onComplete={() => setQuizCompleted(true)}
              />
            </TabsContent>
          )}
        </div>
      </Tabs>

      {/* Bottom Action Bar */}
      <div className="sticky bottom-0 border-t border-border bg-card py-4">
        <div className="container mx-auto px-4">
          <div className="flex items-center justify-between">
            <div className="text-sm text-muted-foreground">
              {canComplete ? (
                <span className="text-success flex items-center gap-1">
                  <CheckCircle2 className="h-4 w-4" />
                  Barcha vazifalar bajarildi
                </span>
              ) : (
                <span>Kod mashq va testni bajaring</span>
              )}
            </div>
            <Button
              onClick={handleComplete}
              disabled={!canComplete && !isCompleted}
              className="gap-2"
            >
              {isCompleted ? (
                <>
                  <RotateCcw className="h-4 w-4" />
                  Qayta o&apos;qish
                </>
              ) : nextLesson ? (
                <>
                  Keyingi dars
                  <ChevronRight className="h-4 w-4" />
                </>
              ) : (
                <>
                  Kursni tugatish
                  <CheckCircle2 className="h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
