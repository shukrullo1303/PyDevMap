"use client"

import { courses, roadmapSteps } from "@/lib/data"
import { useAppStore } from "@/lib/store"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Check, Lock, Play, ArrowRight, Sparkles } from "lucide-react"
import { cn } from "@/lib/utils"

export function Roadmap() {
  const { setView, selectCourse, getProgress } = useAppStore()

  const handleCourseClick = (courseId: string) => {
    const course = courses.find(c => c.id === courseId)
    if (course) {
      selectCourse(course)
      setView('course')
    }
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-4xl">
        {/* Hero Section */}
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 border-primary/50 text-primary">
            <Sparkles className="h-3 w-3 mr-1" />
            Python Developer Roadmap 2024
          </Badge>
          <h1 className="text-4xl md:text-5xl font-bold mb-4 text-balance">
            Python Dasturchisi Bo&apos;ling
          </h1>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto text-pretty">
            Bosqichma-bosqich Python dasturlashni o&apos;rganing. Har bir kursdan oldin test yechib, 
            bilimingizni tekshiring va kerakli kurslarni tanlang.
          </p>
        </div>

        {/* Roadmap Steps */}
        <div className="relative">
          {/* Connection Line */}
          <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-border hidden md:block" />

          <div className="space-y-6">
            {roadmapSteps.map((step, index) => {
              const course = courses.find(c => c.id === step.courseId)
              if (!course) return null

              const progress = getProgress(course.id)
              const isCompleted = progress?.skipped || 
                (progress?.completedLessons?.length === course.lessons.length && course.lessons.length > 0)
              const isPurchased = progress?.isPurchased || course.price === 0
              const testScore = progress?.testScore

              // Check if prerequisites are met
              const prerequisitesMet = course.prerequisites.every(prereqId => {
                const prereqProgress = getProgress(prereqId)
                return prereqProgress?.skipped || prereqProgress?.isPurchased
              })

              return (
                <div 
                  key={step.id}
                  className={cn(
                    "relative flex gap-6 items-start",
                    !prerequisitesMet && "opacity-50"
                  )}
                >
                  {/* Step Number */}
                  <div className={cn(
                    "relative z-10 flex h-16 w-16 shrink-0 items-center justify-center rounded-2xl border-2 text-2xl font-bold transition-colors",
                    isCompleted 
                      ? "bg-success border-success text-success-foreground"
                      : isPurchased
                        ? "bg-primary border-primary text-primary-foreground"
                        : "bg-card border-border text-foreground"
                  )}>
                    {isCompleted ? (
                      <Check className="h-8 w-8" />
                    ) : !prerequisitesMet ? (
                      <Lock className="h-6 w-6" />
                    ) : (
                      step.id
                    )}
                  </div>

                  {/* Course Card */}
                  <div 
                    className={cn(
                      "flex-1 rounded-xl border border-border bg-card p-6 transition-all cursor-pointer hover:border-primary/50",
                      isCompleted && "border-success/30 bg-success/5"
                    )}
                    onClick={() => prerequisitesMet && handleCourseClick(course.id)}
                  >
                    <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                      <div className="flex-1">
                        <div className="flex items-center gap-3 mb-2">
                          <span className="text-2xl">{course.icon}</span>
                          <h3 className="text-xl font-semibold text-foreground">
                            {course.title}
                          </h3>
                          {step.required && (
                            <Badge variant="secondary" className="text-xs">
                              Majburiy
                            </Badge>
                          )}
                          {isCompleted && (
                            <Badge className="bg-success text-success-foreground text-xs">
                              Tugallangan
                            </Badge>
                          )}
                        </div>
                        <p className="text-muted-foreground text-sm mb-3">
                          {course.description}
                        </p>
                        <div className="flex flex-wrap items-center gap-3 text-sm">
                          <span className="text-muted-foreground">
                            {course.duration}
                          </span>
                          <span className="text-muted-foreground">•</span>
                          <span className="text-muted-foreground">
                            {course.lessonsCount} ta dars
                          </span>
                          {testScore !== undefined && (
                            <>
                              <span className="text-muted-foreground">•</span>
                              <span className={cn(
                                "font-medium",
                                testScore >= 80 ? "text-success" : "text-warning"
                              )}>
                                Test: {testScore}%
                              </span>
                            </>
                          )}
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        {course.price === 0 ? (
                          <Badge className="bg-success text-success-foreground">
                            Bepul
                          </Badge>
                        ) : (
                          <span className="text-lg font-bold text-foreground">
                            {course.price.toLocaleString()} so&apos;m
                          </span>
                        )}
                        
                        <Button 
                          size="sm"
                          disabled={!prerequisitesMet}
                          className="gap-2"
                          onClick={(e) => {
                            e.stopPropagation()
                            if (prerequisitesMet) handleCourseClick(course.id)
                          }}
                        >
                          {isCompleted ? (
                            <>Takrorlash</>
                          ) : isPurchased ? (
                            <>
                              <Play className="h-4 w-4" />
                              Davom etish
                            </>
                          ) : (
                            <>
                              <ArrowRight className="h-4 w-4" />
                              Batafsil
                            </>
                          )}
                        </Button>
                      </div>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>

        {/* CTA Section */}
        <div className="mt-16 text-center">
          <div className="inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-primary mb-4">
            <Sparkles className="h-4 w-4" />
            <span className="text-sm font-medium">Hoziroq boshlang!</span>
          </div>
          <p className="text-muted-foreground max-w-xl mx-auto">
            Birinchi kursni bepul o&apos;rganing va Python dasturlash dunyosiga qadam qo&apos;ying.
          </p>
        </div>
      </div>
    </div>
  )
}
