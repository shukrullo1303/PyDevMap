// pages/CoursePage.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getCourse } from '../services/courses';
import { getLessonsByCourse, getLessonProgress } from '../services/lessons';
import LessonListCard from '../components/LessonListCard';
import { enrollCourse, checkEnrolled } from '../services/enrollments';
import { useAuth } from '../context/AuthContext';
import '../styles/pages/CoursePage.css';


const CoursePage = () => {
    const { id } = useParams();
    const { user } = useAuth();
    const [course, setCourse] = useState(null);
    const [lessons, setLessons] = useState([]);
    const [enrolled, setEnrolled] = useState();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await getCourse(id);
                setCourse(res.data);
            } catch (err) {
                console.error(err);
            }

            try {
                const res2 = await getLessonsByCourse(id);
                setLessons(Array.isArray(res2.data) ? res2.data : res2.data.results || []);
                console.log(res2.data)
            } catch (e) {
                setLessons([]);
            }

            // ENROLLED STATUSNI TEKSHIRISH
            if (user) {
                try {
                    const r = await checkEnrolled(id);
                    setEnrolled(r.data.enrolled);
                } catch (e) {
                    setEnrolled(false);
                }
            }

            setLoading(false);
        };
        load();
    }, [id, user]);


    const handleEnroll = async () => {
        try {
            const res = await enrollCourse(course.id);
            alert(res.data.detail);
            if (res.data.detail === "Successfully enrolled") {
                setEnrolled(true);
            }
        } catch (err) {
            console.error("Enroll error:", err.response?.data);
            alert(err.response?.data?.detail || "Enroll failed");
        }
    };

    if (loading) return <div className="site-container"><div className="loading-state">Loading course...</div></div>;
    if (!course) return <div className="site-container"><div className="empty-state">Kurs topilmadi.</div></div>;

    return (
        <div className="site-container">
            <div className="breadcrumb">
                <Link to="/">Bosh sahifa</Link>
                <span>/</span>
                <span>{course.title}</span>
            </div>

            <div className="course-hero">
                <div className="course-hero-content">
                    <h1>{course.title}</h1>
                    <p className="course-subtitle">{course.subtitle || course.description?.slice(0, 120)}</p>
                    <div className="course-actions">
                        <div className="price-badge">
                            {course.is_free
                                ? 'Bepul'
                                : `${Number(course.price).toLocaleString('fr-FR').replace(',', ' ')} so'm`}
                        </div>
                        <button
                            onClick={handleEnroll}
                            className={`btn ${enrolled ? 'btn-secondary' : 'btn-primary'}`}
                            disabled={enrolled}
                        >
                            {enrolled ? '✓ Enrolled' : 'Enroll now'}
                        </button>
                    </div>
                </div>
            </div>

            <div className="course-layout sidebar">
                <div className="course-main">
                    <section className="course-section">
                        <h2>Kurs haqida</h2>
                        <p className="course-description">
                            {course.description}
                        </p>
                    </section>

                    <section className="course-section">
                        <h2>Darslar ({lessons.length})</h2>
                        {lessons.length === 0 ? (
                            <div className="empty-state">Darslar yo'q</div>
                        ) : (
                            <div className="lesson-grid">
                                {lessons.map((lesson, idx) => {
                                    // Foydalanuvchining progressini olish
                                    const userProgress = lesson.progress_records?.find(pr => pr.user === user?.id);

                                    // Oldingi lesson progressini topish
                                    const prevLesson = lessons.find(l => l.id === lesson.prev_lesson_id);
                                    const prevProgress = prevLesson?.progress_records?.find(pr => pr.user === user?.id);

                                    // Lesson ochiq bo‘lish sharti
                                    const isOpen = enrolled && (
                                        lesson.prev_lesson_id === null || // birinchi lesson
                                        prevProgress?.completed           // oldingi lesson completed bo‘lsa
                                    );
                                    return (
                                        <LessonListCard
                                            key={lesson.id}
                                            lesson={lesson}
                                            index={idx + 1}
                                            isOpen={isOpen}  // button LessonListCard ichida shu shartga qarab
                                        />
                                    );
                                })}

                            </div>
                        )}
                    </section>

                </div>

                <aside className="course-sidebar">
                    <div className="sidebar-card">
                        <h4>Kurs ma'lumotlari</h4>
                        <div className="detail-item">
                            <span className="detail-label">O'qituvchi</span>
                            <span className="detail-value">{course.instructor_name || 'TBA'}</span>
                        </div>
                        <div className="detail-item">
                            <span className="detail-label">Daraja</span>
                            <span className="detail-value">{course.level || 'noaniq'}</span>
                        </div>
                        <div className="detail-item">
                            <span className="detail-label">Darslar</span>
                            <span className="detail-value">{lessons.length}</span>
                        </div>
                        <div className="detail-item">
                            <span className="detail-label">Status</span>
                            <span className={`detail-badge ${enrolled ? 'enrolled' : 'available'}`}>
                                {enrolled ? 'Enrolled' : 'Available'}
                            </span>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default CoursePage;
