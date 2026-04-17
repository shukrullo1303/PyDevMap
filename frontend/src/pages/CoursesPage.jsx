import React, { useEffect, useState } from 'react';
import { getCourses } from '../services/courses';
import CourseCard from '../components/CourseCard';

const LEVELS = ["Hammasi", "Boshlang'ich", "O'rta", "Murakkab"];

const CoursesPage = () => {
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [levelFilter, setLevelFilter] = useState('Hammasi');

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

    const filteredCourses = courses.filter(c => {
        const matchSearch = !searchQuery.trim() ||
            c.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
            c.description?.toLowerCase().includes(searchQuery.toLowerCase());

        const matchLevel = levelFilter === 'Hammasi' ||
            c.level?.toLowerCase().includes(levelFilter.toLowerCase()) ||
            (levelFilter === "Boshlang'ich" && c.level?.toLowerCase().includes('beginner')) ||
            (levelFilter === "O'rta" && c.level?.toLowerCase().includes('intermediate')) ||
            (levelFilter === 'Murakkab' && c.level?.toLowerCase().includes('advanced'));

        return matchSearch && matchLevel;
    });

    return (
        <div className="site-container">
            {/* Header */}
            <div style={{ marginBottom: 32 }}>
                <h1 style={{ marginBottom: 8 }}>Barcha Kurslar</h1>
                <p style={{ color: 'var(--text-secondary)', margin: 0 }}>
                    Python dasturlashni o'rganish uchun tanlangan kurslar to'plami
                </p>
            </div>

            {/* Filters */}
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16, marginBottom: 32, alignItems: 'center' }}>
                {/* Search */}
                <div style={{ position: 'relative', flex: '1', minWidth: 220, maxWidth: 400 }}>
                    <span style={{
                        position: 'absolute', left: 12, top: '50%', transform: 'translateY(-50%)',
                        color: 'var(--text-tertiary)', pointerEvents: 'none'
                    }}>
                        🔍
                    </span>
                    <input
                        type="text"
                        placeholder="Kurs qidirish..."
                        value={searchQuery}
                        onChange={e => setSearchQuery(e.target.value)}
                        className="form-control"
                        style={{ paddingLeft: 38 }}
                    />
                </div>

                {/* Level filter */}
                <div className="filter-bar" style={{ margin: 0 }}>
                    <span className="filter-label">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                            <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>
                        </svg>
                    </span>
                    <div className="filter-btns">
                        {LEVELS.map(level => (
                            <button
                                key={level}
                                className={`filter-btn ${levelFilter === level ? 'active' : ''}`}
                                onClick={() => setLevelFilter(level)}
                            >
                                {level}
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Courses Grid */}
            {loading ? (
                <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Kurslar yuklanmoqda...</p>
                </div>
            ) : filteredCourses.length === 0 ? (
                <div className="empty-state">
                    <p style={{ fontSize: 40, marginBottom: 12 }}>🔍</p>
                    <p>Kurslar topilmadi</p>
                    {searchQuery && <p style={{ fontSize: 'var(--font-size-sm)', color: 'var(--text-tertiary)', marginTop: 4 }}>
                        Qidiruvni qaytadan ko'rib chiqing
                    </p>}
                </div>
            ) : (
                <>
                    <p style={{ color: 'var(--text-tertiary)', fontSize: 'var(--font-size-sm)', marginBottom: 16 }}>
                        {filteredCourses.length} ta kurs topildi
                    </p>
                    <div className="course-grid">
                        {filteredCourses.map((course, idx) => (
                            <CourseCard key={course.id} course={course} index={idx} />
                        ))}
                    </div>
                </>
            )}
        </div>
    );
};

export default CoursesPage;
