import React from 'react';
import '../styles/components/AnswerOption.css';

const AnswerOption = ({ option, checked, onChange }) => (
    <label className="answer-option">
        <input
            type={option.is_multiple ? 'checkbox' : 'radio'}
            id={`opt-${option.id}`}
            checked={checked}
            onChange={() => onChange(option.id)}
            className="answer-input"
        />
        <div className={`answer-box ${checked ? 'checked' : ''}`}>
            <span className="answer-indicator">
                {option.is_multiple ? (
                    checked ? '✓' : ''
                ) : (
                    checked ? '◉' : '○'
                )}
            </span>
            <span className="answer-text">{option.text}</span>
        </div>
    </label>
);

export default AnswerOption;
