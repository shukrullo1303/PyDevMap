import React from 'react';
import { useNavigate } from 'react-router-dom';

const LessonListCard = ({ lesson, index, isOpen }) => {
    const navigate = useNavigate();

    return (
        <div
            className="lesson-card"
            style={!isOpen ? { opacity: 0.5 } : {}}
        >
            <div style={{ display: 'flex', alignItems: 'center', gap: 12, flex: 1 }}>
                {/* Step number */}
                <div style={{
                    width: 32,
                    height: 32,
                    borderRadius: '50%',
                    background: isOpen ? 'var(--surface-2)' : 'var(--border)',
                    border: '1.5px solid var(--border)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 'var(--font-size-xs)',
                    fontWeight: 'var(--font-weight-semibold)',
                    color: 'var(--text-secondary)',
                    flexShrink: 0,
                }}>
                    {index}
                </div>

                <div>
                    <h4 style={{ margin: 0, fontSize: 'var(--font-size-base)' }}>
                        {lesson.title}
                    </h4>
                    {lesson.duration && (
                        <small style={{ color: 'var(--text-tertiary)', fontSize: 'var(--font-size-xs)' }}>
                            ⏱ {lesson.duration}
                        </small>
                    )}
                </div>
            </div>

            <button
                className={`btn btn-sm ${isOpen ? 'btn-primary' : 'btn-secondary'}`}
                onClick={() => navigate(`/lessons/${lesson.id}`)}
                disabled={!isOpen}
                style={{ flexShrink: 0 }}
            >
                {isOpen ? (
                    <>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                            <polygon points="5 3 19 12 5 21 5 3"/>
                        </svg>
                        Ochish
                    </>
                ) : (
                    <>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                            <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
                        </svg>
                        Yopiq
                    </>
                )}
            </button>
        </div>
    );
};

export default LessonListCard;
