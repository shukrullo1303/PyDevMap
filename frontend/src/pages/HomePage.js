import React, { useEffect, useState } from 'react';
import { getCourses } from '../services/courses';
import CourseCard from '../components/CourseCard';
import '../styles/pages/HomePage.css';

const Home = () => {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    getCourses()
      .then(res => {
        setCourses(res.data.results || res.data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading courses:', err);
        setCourses([]);
        setLoading(false);
      });
  }, []);

  const filteredCourses = searchQuery.trim()
    ? courses.filter(c =>
      c.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      c.description?.toLowerCase().includes(searchQuery.toLowerCase())
    )
    : courses;

  return (
    <div className="site-container">
      <div className="hero">
        <h1>Learn anything, achieve everything</h1>
        <p>Bizning kurslarni o'rganing va o'z yo'lingizda yangi ko'nikmalarni egallang.</p>
        <div className="search-bar">
          <input
            placeholder="Kurslarni qidirish..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="hero-search"
          />
        </div>
      </div>

      <div className="home-section">
        <div className="section-header">
          <h2>Siz uchun tavsiya qilinadi</h2>
          <p className="section-desc">Yangi imkoniyatlarni ochish uchun o'rganing</p>
        </div>

        {loading ? (
          <div className="loading-state">
            <p>Kurslar yuklanmoqda...</p>
          </div>
        ) : filteredCourses.length === 0 ? (
          <div className="empty-state">
            <p>Kurslar topilmadi</p>
            {searchQuery && <p className="empty-desc">Qidiruvni qaytadan ko'rib chiqing</p>}
          </div>
        ) : (
          <div className="course-grid">
            {filteredCourses.map(course => (
              <CourseCard key={course.id} course={course} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Home;
