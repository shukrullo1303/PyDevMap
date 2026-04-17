import React, { useEffect, useState } from 'react';
import { getCourses } from '../services/courses';
import { useNavigate } from 'react-router-dom';

// Har bir kurs uchun emoji belgi
const COURSE_ICONS = ['🐍', '⚙️', '📊', '🏗️', '🌐', '🤖', '🔧', '📦', '🚀', '🔐'];
// Gradient ranglar
const COURSE_COLORS = [
    'linear-gradient(135deg, #22c55e, #16a34a)',
    'linear-gradient(135deg, #3b82f6, #0891b2)',
    'linear-gradient(135deg, #f97316, #dc2626)',
    'linear-gradient(135deg, #a855f7, #ec4899)',
    'linear-gradient(135deg, #14b8a6, #22c55e)',
    'linear-gradient(135deg, #6366f1, #8b5cf6)',
    'linear-gradient(135deg, #f59e0b, #ef4444)',
    'linear-gradient(135deg, #06b6d4, #3b82f6)',
    'linear-gradient(135deg, #10b981, #059669)',
    'linear-gradient(135deg, #8b5cf6, #6366f1)',
];

const getLevelBadge = (level) => {
    if (!level) return null;
    const lower = level.toLowerCase();
    if (lower.includes('beginner') || lower.includes('boshlang')) {
        return <span className="badge badge-level-beginner">Boshlang'ich</span>;
    } else if (lower.includes('intermediate') || lower.includes('o\'rta') || lower.includes('orta')) {
        return <span className="badge badge-level-intermediate">O'rta</span>;
    } else if (lower.includes('advanced') || lower.includes('murakkab')) {
        return <span className="badge badge-level-advanced">Murakkab</span>;
    }
    return <span className="badge badge-outline">{level}</span>;
};

const RoadmapPage = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        getCourses()
            .then(res => {
                setCourses(res.data.results || res.data);
                setLoading(false);
            })
            .catch(() => {
                setCourses([]);
                setLoading(false);
            });
    }, []);

    return (
        <div className="site-container">
            {/* Hero */}
            <div className="roadmap-hero">
                <div className="roadmap-badge">
                    <span>✨</span>
                    Python Developer Roadmap 2024
                </div>
                <h1 className="roadmap-title">
                    Python Dasturchisi Bo'ling
                </h1>
                <p className="roadmap-subtitle">
                    Bosqichma-bosqich Python dasturlashni o'rganing. Har bir kursdan oldin test yechib,
                    bilimingizni tekshiring va kerakli kurslarni tanlang.
                </p>
            </div>

            {/* Roadmap Steps */}
            {loading ? (
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Kurslar yuklanmoqda...</p>
                </div>
            ) : courses.length === 0 ? (
                <div className="empty-state">
                    <p style={{ fontSize: 48, marginBottom: 16 }}>📭</p>
                    <p>Hozircha kurslar yo'q</p>
                </div>
            ) : (
                <div className="roadmap-steps">
                    {/* Vertical line */}
                    <div className="roadmap-line" />

                    {courses.map((course, idx) => {
                        const icon = COURSE_ICONS[idx % COURSE_ICONS.length];
                        const color = COURSE_COLORS[idx % COURSE_COLORS.length];
                        const isFree = course.is_free || Number(course.price) === 0;

                        return (
                            <div key={course.id} className="roadmap-step">
                                {/* Step number */}
                                <div className="roadmap-step-num">
                                    {idx + 1}
                                </div>

                                {/* Course card */}
                                <div
                                    className="roadmap-step-card"
                                    onClick={() => navigate(`/courses/${course.id}`)}
                                >
                                    <div className="roadmap-card-top">
                                        <div className="roadmap-card-info">
                                            <div className="roadmap-card-title-row">
                                                <span className="roadmap-course-icon">{icon}</span>
                                                <h3 className="roadmap-card-title">{course.title}</h3>
                                                {getLevelBadge(course.level)}
                                            </div>
                                            <p className="roadmap-card-desc">
                                                {course.description?.slice(0, 130)}
                                                {course.description?.length > 130 ? '...' : ''}
                                            </p>
                                            <div className="roadmap-card-meta">
                                                {course.category_name && (
                                                    <span>📂 {course.category_name}</span>
                                                )}
                                                {course.lessons_count !== undefined && (
                                                    <>
                                                        <span>•</span>
                                                        <span>📖 {course.lessons_count} ta dars</span>
                                                    </>
                                                )}
                                            </div>
                                        </div>

                                        <div className="roadmap-card-actions">
                                            {isFree ? (
                                                <span className="badge badge-free">Bepul</span>
                                            ) : (
                                                <span style={{ fontWeight: 700, fontSize: 'var(--font-size-base)', color: 'var(--text-primary)' }}>
                                                    {Number(course.price).toLocaleString('fr-FR').replace(',', ' ')} so'm
                                                </span>
                                            )}
                                            <button
                                                className="btn btn-primary btn-sm"
                                                onClick={(e) => {
                                                    e.stopPropagation();
                                                    navigate(`/courses/${course.id}`);
                                                }}
                                            >
                                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                                                    <line x1="5" y1="12" x2="19" y2="12"/>
                                                    <polyline points="12 5 19 12 12 19"/>
                                                </svg>
                                                Batafsil
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        );
                    })}
                </div>
            )}

            {/* CTA */}
            {!loading && courses.length > 0 && (
                <div className="roadmap-cta">
                    <div className="roadmap-badge" style={{ marginBottom: 12 }}>
                        <span>🚀</span>
                        Hoziroq boshlang!
                    </div>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
                        Barcha kurslarni ko'rish va qidirish uchun kurslar sahifasiga o'ting.
                    </p>
                    <button
                        className="btn btn-primary"
                        onClick={() => navigate('/courses')}
                        style={{ padding: '10px 28px' }}
                    >
                        Barcha kurslar →
                    </button>
                </div>
            )}
        </div>
    );
};

export default RoadmapPage;
