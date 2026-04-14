"use client"

import { Button } from "@/components/ui/button"
import { useAppStore } from "@/lib/store"
import { BookOpen, Map, Home, ChevronLeft } from "lucide-react"

export function Header() {
  const { currentView, setView, selectedCourse, selectCourse, selectLesson } = useAppStore()

  const handleBack = () => {
    if (currentView === 'lesson' || currentView === 'test') {
      setView('course')
      selectLesson(null)
    } else if (currentView === 'course' || currentView === 'placement-test') {
      setView('courses')
      selectCourse(null)
    } else {
      setView('roadmap')
    }
  }

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-card/95 backdrop-blur supports-[backdrop-filter]:bg-card/60">
      <div className="container mx-auto px-4">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center gap-4">
            {currentView !== 'roadmap' && (
              <Button 
                variant="ghost" 
                size="icon"
                onClick={handleBack}
                className="text-muted-foreground hover:text-foreground"
              >
                <ChevronLeft className="h-5 w-5" />
              </Button>
            )}
            <div 
              className="flex items-center gap-2 cursor-pointer"
              onClick={() => {
                setView('roadmap')
                selectCourse(null)
                selectLesson(null)
              }}
            >
              <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
                py
              </div>
              <span className="text-xl font-bold text-foreground">
                pyDevMap
              </span>
            </div>
          </div>

          <nav className="flex items-center gap-2">
            <Button
              variant={currentView === 'roadmap' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => {
                setView('roadmap')
                selectCourse(null)
                selectLesson(null)
              }}
              className="gap-2"
            >
              <Map className="h-4 w-4" />
              <span className="hidden sm:inline">Yo&apos;l Xaritasi</span>
            </Button>
            <Button
              variant={currentView === 'courses' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => {
                setView('courses')
                selectCourse(null)
                selectLesson(null)
              }}
              className="gap-2"
            >
              <BookOpen className="h-4 w-4" />
              <span className="hidden sm:inline">Kurslar</span>
            </Button>
          </nav>
        </div>

        {selectedCourse && (currentView === 'course' || currentView === 'lesson') && (
          <div className="pb-3 -mt-1">
            <p className="text-sm text-muted-foreground">
              {selectedCourse.title}
            </p>
          </div>
        )}
      </div>
    </header>
  )
}
