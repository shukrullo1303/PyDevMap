// components/CourseEnrollButton.js
import React, { useState } from 'react';
import { Button } from 'react-bootstrap';
import api from '../services/api'; // axios instance
import { useAuth } from '../context/AuthContext';

const CourseEnrollButton = ({ courseId, onEnroll }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const handleEnroll = async () => {
    if (!user) return; // foydalanuvchi login qilmagan bo‘lsa
    setLoading(true);
    setError(null);
    try {
      const res = await api.post(`courses/courses/${courseId}/enroll/`);
      if (res.status === 201 || res.status === 200) {
        onEnroll?.(); // parent componentga xabar berishx
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Enrollment failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button onClick={handleEnroll} disabled={loading}>
        {loading ? `Ro'yxatdan otilmoqda...` : `Ro'yxatdan otish`}
      </Button>
      {error && <div className="text-danger mt-1">{error}</div>}
    </>
  );
};

export default CourseEnrollButton;
