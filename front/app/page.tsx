"use client"

import { Header } from "@/components/header"
import { Roadmap } from "@/components/roadmap"
import { CoursesList } from "@/components/courses-list"
import { CourseDetail } from "@/components/course-detail"
import { PlacementTest } from "@/components/placement-test"
import { LessonView } from "@/components/lesson-view"
import { useAppStore } from "@/lib/store"

export default function Home() {
  const { currentView } = useAppStore()

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main>
        {currentView === 'roadmap' && <Roadmap />}
        {currentView === 'courses' && <CoursesList />}
        {currentView === 'course' && <CourseDetail />}
        {currentView === 'placement-test' && <PlacementTest />}
        {currentView === 'lesson' && <LessonView />}
      </main>
    </div>
  )
}
