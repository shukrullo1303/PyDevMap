import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getLesson, getLessonsByCourse, markProgress, getLessonProgress } from '../services/lessons';
import LessonListCard from '../components/LessonListCard';
import { useAuth } from '../context/AuthContext';
import { getUserQuizResult } from '../services/quiz';
import '../styles/pages/LessonPage.css';

const LessonPage = () => {
    const { id } = useParams(); // course id
    const { user } = useAuth();
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(true);
    const [lesson_progress, setLessonProgress] = useState(null)

    useEffect(() => {
        const loadLessons = async () => {
            try {
                const res = await getLesson(id); // backend API: /courses/:id/lessons/
                setLessons(res.data);
                const res_lesson_progress = await getLessonProgress(id)
                setLessonProgress(res_lesson_progress.data)
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        loadLessons();
    }, [id]);

    // Lesson progress mark qilish
    const handleComplete = async (lessonId) => {
        try {
            await markProgress(lessonId, { completed: true });
            setLessons(prev =>
                prev.map(l => l.id === lessonId ? { ...l, is_completed: true } : l)
            );
        } catch (err) {
            console.error(err);
        }
    };

    if (loading) {
        return <div className="site-container">Loading lessons...</div>;
    }

    if (!lessons.length) {
        return <div className="site-container">No lessons found for this course.</div>;
    }

    return (
        <div className="site-container">
            <h2>Lessons</h2>
            
            <div className="lessons-list">
                {lessons.map((lesson, idx) => (
                    <div key={lesson.id} className="lesson-item">
                        <LessonListCard
                            lesson={{
                                ...lesson,
                                lesson_progress: lesson_progress, // backenddan kelgan
                                has_quiz: lesson.quiz !== null,
                            }}
                        />
                        {/* Completed tugmasi lesson pastida */}
                        {!lesson.is_completed && (
                            <button
                                className="btn btn-sm btn-primary mt-1"
                                onClick={() => handleComplete(lesson.id)}
                            >
                                Mark as Complete
                            </button>
                        )}
                        {lesson.is_completed && (
                            <span className="badge bg-success mt-1">Completed</span>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default LessonPage;
