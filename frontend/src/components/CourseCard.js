import React from 'react';
import { Link } from 'react-router-dom';
import "../styles/components/CourseCard.css"

const CourseCard = ({ course }) => {
  return (
    <div className="course-card">
      {course.thumbnail ? (
        <img src={course.thumbnail} alt={course.title} className="course-thumb" />
      ) : (
        <div className="course-thumb" />
      )}
      <div className="course-body">
        <div className="course-title">{course.title}</div>
        <div className="course-desc">{course.description?.slice(0, 120)}{course.description && course.description.length > 120 ? '...' : ''}</div>
        <div className="course-meta">
          <div className="tag">{course.level || 'noaniq'}</div>
          <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
            <div className="price-badge">
              {course.is_free
                ? 'Bepul'
                : `${Number(course.price).toLocaleString('fr-FR').replace(',', ' ')} so'm`}
            </div>
            <Link to={`/courses/${course.id}`} className="btn btn-outline-primary">Ko'rish</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseCard;
