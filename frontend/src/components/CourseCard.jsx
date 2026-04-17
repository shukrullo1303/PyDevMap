import React from 'react';
import { useNavigate } from 'react-router-dom';

const COURSE_ICONS = ['🐍', '⚙️', '📊', '🏗️', '🌐', '🤖', '🔧', '📦', '🚀', '🔐'];
const ICON_BG_COLORS = [
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

const CourseCard = ({ course, index = 0 }) => {
    const navigate = useNavigate();
    const icon = COURSE_ICONS[index % COURSE_ICONS.length];
    const bgColor = ICON_BG_COLORS[index % ICON_BG_COLORS.length];
    const isFree = course.is_free || Number(course.price) === 0;

    return (
        <div
            className="course-card"
            onClick={() => navigate(`/courses/${course.id}`)}
        >
            {/* Header */}
            <div className="course-card-header">
                <div
                    className="course-icon"
                    style={{ background: bgColor }}
                >
                    {icon}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                    {getLevelBadge(course.level)}
                </div>
            </div>

            {/* Body */}
            <div className="course-body">
                <div className="course-title">{course.title}</div>
                <div className="course-desc">
                    {course.description?.slice(0, 120)}
                    {course.description?.length > 120 ? '...' : ''}
                </div>

                {/* Meta */}
                <div className="course-meta-row">
                    {course.lessons_count !== undefined && (
                        <div className="course-meta-item">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>
                                <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
                            </svg>
                            {course.lessons_count} dars
                        </div>
                    )}
                    {course.category_name && (
                        <div className="course-meta-item">
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                            </svg>
                            {course.category_name}
                        </div>
                    )}
                </div>
            </div>

            {/* Footer */}
            <div className="course-footer">
                {isFree ? (
                    <span className="badge badge-free">Bepul</span>
                ) : (
                    <span className="course-price">
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
                    Ko'rish
                </button>
            </div>
        </div>
    );
};

export default CourseCard;
