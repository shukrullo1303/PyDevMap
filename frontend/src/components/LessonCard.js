import { Card, Button, Badge } from 'react-bootstrap';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { markProgress } from '../services/lessons';
import "../styles/components/LessonCard.css";

const LessonCard = ({ lesson, refreshLesson }) => {
    const navigate = useNavigate();
    const { user } = useAuth();
    const [loading, setLoading] = useState(false);

    const handleComplete = async () => {
        if (!user) return; // user bo'lmasa return
        setLoading(true);
        try {
            await markProgress(lesson.id, { completed: true });
            if (refreshLesson) refreshLesson(); // parent componentni refresh qilish
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleQuiz = () => {
        navigate(`/lessons/${lesson.id}/quiz`);
    };

    return (
        <div className="lesson-detail">
            <h2>{lesson.title}</h2>
            <p>{lesson.order} - dars </p>

            {/* Video container */}
            {lesson.video_url && (
                <div style={{ width: '100%', maxHeight: '80vh', margin: '20px 0' }}>
                    <video
                        src={lesson.video_url}
                        controls
                        style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'contain', // cover emas, shunda butun video ko‘rinadi
                            borderRadius: '8px',
                        }}
                    />
                </div>
            )}

            {/* Tugmalar */}
            <div style={{ marginTop: '20px', display: 'flex', gap: '10px' }}>
                {!lesson.is_completed && (
                    <button className="btn btn-primary" onClick={() => handleComplete(lesson.id)}>
                        Mark as Complete
                    </button>
                )}
                {lesson.has_quiz && (
                    <button className="btn btn-success" onClick={() => navigate(`/lessons/${lesson.id}/quiz`)}>
                        Go to Quiz
                    </button>
                )}
            </div>
        </div>

    );
};

export default LessonCard;
