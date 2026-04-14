"use client"

import { courses } from "@/lib/data"
import { useAppStore } from "@/lib/store"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent, CardFooter, CardHeader } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Clock, BookOpen, Play, Search, Filter, Check } from "lucide-react"
import { useState } from "react"
import { cn } from "@/lib/utils"

export function CoursesList() {
  const { setView, selectCourse, getProgress } = useAppStore()
  const [searchQuery, setSearchQuery] = useState("")
  const [levelFilter, setLevelFilter] = useState<string | null>(null)

  const filteredCourses = courses.filter(course => {
    const matchesSearch = course.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      course.description.toLowerCase().includes(searchQuery.toLowerCase())
    const matchesLevel = !levelFilter || course.level === levelFilter
    return matchesSearch && matchesLevel
  })

  const levels = ["Boshlang'ich", "O'rta", "Murakkab"]

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">Barcha Kurslar</h1>
          <p className="text-muted-foreground">
            Python dasturlashni o&apos;rganish uchun tanlangan kurslar to&apos;plami
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Kurs qidirish..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-muted-foreground" />
            <div className="flex gap-2">
              <Button
                variant={levelFilter === null ? "secondary" : "ghost"}
                size="sm"
                onClick={() => setLevelFilter(null)}
              >
                Hammasi
              </Button>
              {levels.map(level => (
                <Button
                  key={level}
                  variant={levelFilter === level ? "secondary" : "ghost"}
                  size="sm"
                  onClick={() => setLevelFilter(level)}
                >
                  {level}
                </Button>
              ))}
            </div>
          </div>
        </div>

        {/* Courses Grid */}
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {filteredCourses.map((course) => {
            const progress = getProgress(course.id)
            const isCompleted = progress?.skipped || 
              (progress?.completedLessons?.length === course.lessons.length && course.lessons.length > 0)
            const isPurchased = progress?.isPurchased || course.price === 0

            const completedCount = progress?.completedLessons?.length || 0
            const progressPercent = course.lessons.length > 0 
              ? Math.round((completedCount / course.lessons.length) * 100)
              : 0

            return (
              <Card 
                key={course.id} 
                className={cn(
                  "group cursor-pointer transition-all hover:border-primary/50",
                  isCompleted && "border-success/30"
                )}
                onClick={() => {
                  selectCourse(course)
                  setView('course')
                }}
              >
                <CardHeader className="pb-3">
                  <div className="flex items-start justify-between">
                    <div className={cn(
                      "flex h-12 w-12 items-center justify-center rounded-xl text-2xl",
                      `bg-gradient-to-br ${course.color}`
                    )}>
                      {course.icon}
                    </div>
                    <div className="flex items-center gap-2">
                      {isCompleted && (
                        <div className="flex h-6 w-6 items-center justify-center rounded-full bg-success">
                          <Check className="h-4 w-4 text-success-foreground" />
                        </div>
                      )}
                      <Badge variant={
                        course.level === "Boshlang'ich" ? "secondary" :
                        course.level === "O'rta" ? "outline" : "default"
                      }>
                        {course.level}
                      </Badge>
                    </div>
                  </div>
                  <h3 className="text-lg font-semibold mt-4 group-hover:text-primary transition-colors">
                    {course.title}
                  </h3>
                  <p className="text-sm text-muted-foreground line-clamp-2">
                    {course.description}
                  </p>
                </CardHeader>

                <CardContent className="pb-3">
                  <div className="flex items-center gap-4 text-sm text-muted-foreground">
                    <div className="flex items-center gap-1">
                      <Clock className="h-4 w-4" />
                      {course.duration}
                    </div>
                    <div className="flex items-center gap-1">
                      <BookOpen className="h-4 w-4" />
                      {course.lessonsCount} dars
                    </div>
                  </div>

                  {isPurchased && course.lessons.length > 0 && (
                    <div className="mt-4">
                      <div className="flex items-center justify-between text-sm mb-1">
                        <span className="text-muted-foreground">Progress</span>
                        <span className="font-medium">{progressPercent}%</span>
                      </div>
                      <div className="h-2 rounded-full bg-muted overflow-hidden">
                        <div 
                          className="h-full bg-primary transition-all"
                          style={{ width: `${progressPercent}%` }}
                        />
                      </div>
                    </div>
                  )}

                  {course.prerequisites.length > 0 && (
                    <div className="mt-4">
                      <p className="text-xs text-muted-foreground mb-1">Talab qilinadi:</p>
                      <div className="flex flex-wrap gap-1">
                        {course.prerequisites.map(prereqId => {
                          const prereq = courses.find(c => c.id === prereqId)
                          const prereqProgress = getProgress(prereqId)
                          const prereqCompleted = prereqProgress?.skipped || prereqProgress?.isPurchased
                          return prereq ? (
                            <Badge 
                              key={prereqId} 
                              variant="outline"
                              className={cn(
                                "text-xs",
                                prereqCompleted && "border-success/50 text-success"
                              )}
                            >
                              {prereqCompleted && <Check className="h-3 w-3 mr-1" />}
                              {prereq.title}
                            </Badge>
                          ) : null
                        })}
                      </div>
                    </div>
                  )}
                </CardContent>

                <CardFooter className="pt-3 border-t border-border">
                  <div className="flex items-center justify-between w-full">
                    {course.price === 0 ? (
                      <Badge className="bg-success text-success-foreground">
                        Bepul
                      </Badge>
                    ) : (
                      <span className="font-bold">
                        {course.price.toLocaleString()} so&apos;m
                      </span>
                    )}
                    <Button size="sm" className="gap-2">
                      {isCompleted ? (
                        "Takrorlash"
                      ) : isPurchased ? (
                        <>
                          <Play className="h-4 w-4" />
                          Davom etish
                        </>
                      ) : (
                        "Batafsil"
                      )}
                    </Button>
                  </div>
                </CardFooter>
              </Card>
            )
          })}
        </div>

        {filteredCourses.length === 0 && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Hech qanday kurs topilmadi</p>
          </div>
        )}
      </div>
    </div>
  )
}
