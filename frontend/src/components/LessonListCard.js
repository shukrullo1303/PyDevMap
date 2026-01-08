import { Card, Button } from 'react-bootstrap';
import { isRouteErrorResponse, useNavigate } from 'react-router-dom';
import "../styles/components/LessonCard.css"

const LessonListCard = ({ lesson, isOpen }) => {
    const navigate = useNavigate();

    const handleOpen = () => {
        navigate(`/lessons/${lesson.id}`);
    };

    return (
        <Card className="mb-2">
            <Card.Body className="d-flex justify-content-between align-items-center">
                <div>
                    <Card.Title className="mb-0">{lesson.title}</Card.Title>
                    <small className="text-muted">{lesson.duration || ''}</small>
                </div>
                <Button
                    variant="outline-primary"
                    onClick={handleOpen}
                    disabled={!isOpen} // locked darslarni ochmaslik
                >
                    Ochish
                </Button>
            </Card.Body>
        </Card>
    );
};

export default LessonListCard;