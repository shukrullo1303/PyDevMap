import React, { useState } from 'react';
import '../styles/components/Quiz.css';

const Quiz = ({ quiz, onSubmit, submitting }) => {
    const [answers, setAnswers] = useState({});

    const handleChange = (questionId, answerId) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: answerId
        }));
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit(answers);
    };

    return (
        <form className="quiz-form" onSubmit={handleSubmit}>
            {quiz.questions.map(question => (
                <div key={question.id} className="question">
                    <h3>{question.text}</h3>
                    <div className="answers">
                        {question.answers.map(answer => (
                            <label key={answer.id} className="answer">
                                <input
                                    type="radio"
                                    name={`question-${question.id}`}
                                    value={answer.id}
                                    checked={answers[question.id] === answer.id}
                                    onChange={() => handleChange(question.id, answer.id)}
                                />
                                {answer.text}
                            </label>
                        ))}
                    </div>
                </div>
            ))}
            <button type="submit" className="btn btn-primary" disabled={submitting}>
                {submitting ? 'Submitting...' : 'Submit Quiz'}
            </button>
        </form>
    );
};

export default Quiz;
