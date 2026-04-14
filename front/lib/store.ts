import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { Course, Lesson } from './data'

interface UserProgress {
  courseId: string
  completedLessons: string[]
  testScore?: number
  isPurchased: boolean
  skipped: boolean
}

interface AppState {
  currentView: 'roadmap' | 'courses' | 'course' | 'lesson' | 'test' | 'placement-test'
  selectedCourse: Course | null
  selectedLesson: Lesson | null
  userProgress: UserProgress[]
  
  setView: (view: AppState['currentView']) => void
  selectCourse: (course: Course | null) => void
  selectLesson: (lesson: Lesson | null) => void
  purchaseCourse: (courseId: string) => void
  completePlacementTest: (courseId: string, score: number, passed: boolean) => void
  completeLesson: (courseId: string, lessonId: string) => void
  getProgress: (courseId: string) => UserProgress | undefined
  skipCourse: (courseId: string) => void
}

export const useAppStore = create<AppState>()(
  persist(
    (set, get) => ({
      currentView: 'roadmap',
      selectedCourse: null,
      selectedLesson: null,
      userProgress: [],

      setView: (view) => set({ currentView: view }),
      
      selectCourse: (course) => set({ selectedCourse: course }),
      
      selectLesson: (lesson) => set({ selectedLesson: lesson }),
      
      purchaseCourse: (courseId) => {
        const progress = get().userProgress
        const existing = progress.find(p => p.courseId === courseId)
        
        if (existing) {
          set({
            userProgress: progress.map(p => 
              p.courseId === courseId ? { ...p, isPurchased: true } : p
            )
          })
        } else {
          set({
            userProgress: [...progress, {
              courseId,
              completedLessons: [],
              isPurchased: true,
              skipped: false
            }]
          })
        }
      },
      
      completePlacementTest: (courseId, score, passed) => {
        const progress = get().userProgress
        const existing = progress.find(p => p.courseId === courseId)
        
        if (existing) {
          set({
            userProgress: progress.map(p => 
              p.courseId === courseId ? { ...p, testScore: score, skipped: passed } : p
            )
          })
        } else {
          set({
            userProgress: [...progress, {
              courseId,
              completedLessons: [],
              testScore: score,
              isPurchased: false,
              skipped: passed
            }]
          })
        }
      },
      
      completeLesson: (courseId, lessonId) => {
        const progress = get().userProgress
        const existing = progress.find(p => p.courseId === courseId)
        
        if (existing) {
          if (!existing.completedLessons.includes(lessonId)) {
            set({
              userProgress: progress.map(p => 
                p.courseId === courseId 
                  ? { ...p, completedLessons: [...p.completedLessons, lessonId] }
                  : p
              )
            })
          }
        } else {
          set({
            userProgress: [...progress, {
              courseId,
              completedLessons: [lessonId],
              isPurchased: false,
              skipped: false
            }]
          })
        }
      },
      
      getProgress: (courseId) => {
        return get().userProgress.find(p => p.courseId === courseId)
      },
      
      skipCourse: (courseId) => {
        const progress = get().userProgress
        const existing = progress.find(p => p.courseId === courseId)
        
        if (existing) {
          set({
            userProgress: progress.map(p => 
              p.courseId === courseId ? { ...p, skipped: true } : p
            )
          })
        } else {
          set({
            userProgress: [...progress, {
              courseId,
              completedLessons: [],
              isPurchased: false,
              skipped: true
            }]
          })
        }
      }
    }),
    {
      name: 'pydevmap-storage'
    }
  )
)
