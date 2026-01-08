import api from '../services/api';
import React, { useEffect, useState } from 'react';
import { getProfile } from '../services/auth';
import { getMyEnrollments } from '../services/enrollments';
import '../styles/pages/ProfilePage.css';
import DownloadCertificateButton from '../components/DownloadCertificateButton'

const ProfilePage = () => {
    const [user, setUser] = useState(null);
    const [enrollments, setEnrollments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [progress, setProgress] = useState([]); // array of {course_id, course_title, progress}


    useEffect(() => {
        const loadUser = async () => {
            try {
                const res = await api.get('/me/', {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                setUser(res.data);
            } catch (err) {
                console.error("User fetch error:", err);
            }
        };

        const loadProfile = async () => {
            try {
                // 1. User
                const profileRes = await getProfile();
                const user = profileRes.data;
                setUser(user);

                // 2. Enrollments
                const enrollRes = await getMyEnrollments(user.id);
                const enrollments = Array.isArray(enrollRes.data)
                    ? enrollRes.data
                    : enrollRes.data.results || [];
                setEnrollments(enrollments);

                // 3. Course progress (backend hisoblagan)
                const progressRes = await api.get('/course-progress/');
                // progressRes.data => [{course_id, course_title, progress}, ...]
                setProgress(progressRes.data);

            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        loadProfile();
        loadUser();
    }, []);

    if (loading) {
        return <div className="site-container">
            <div className="loading-state">Profil yuklanmoqda...</div>
        </div>;
    }

    return (
        <div className="site-container">
            <div className="profile-layout sidebar">
                <div className="profile-main">
                    <section className="profile-section">
                        <h2>My Profile</h2>
                        {user ? (
                            <div className="profile-card">
                                <div className="profile-avatar">
                                    {user.username?.[0]?.toUpperCase() || user.email?.[0]?.toUpperCase() || 'U'}
                                </div>
                                <div className="profile-info">
                                    <h3>{user.username || 'User'} </h3>
                                    <p className="">{user.first_name} {user.last_name}</p>
                                    <p className="profile-email">{user.email}</p>
                                    <p className="profile-joined">
                                        {new Date(user.date_joined || Date.now()).toLocaleDateString()} sanasida ro'yxatdan o'tgan
                                    </p>
                                </div>
                            </div>
                        ) : (
                            <div className="empty-state">Profil topilmadi!</div>
                        )}
                    </section>

                    <section className="profile-section">
                        <h2>Mening kurslarim</h2>
                        {enrollments.length === 0 ? (
                            <div className="empty-state">
                                <p>Ro'yxatdan o'tilgan kurslar topilmadi.</p>
                                <p className="empty-desc">O'zingiz yoqtirgan kurslarni toping va ro'yxatdan o'ting</p>
                            </div>
                        ) : (
                            <div className="enrollments-list">
                                {enrollments.map((e) => {
                                    const courseProgress = progress.find(p => p.course_id === e.course) || { progress: 0, course_title: e.course_title };
                                    return (
                                        <div key={e.id} className="enrollment-item">
                                            {/* Faqat 100% bo'lganda sertifikat tugmasi */}
                                            <div className="enrollment-header">
                                                <h4>{e.course_title || e.course}</h4>
                                                {courseProgress.progress === 100 ?
                                                    <DownloadCertificateButton courseId={e.course} /> :
                                                    <span className="enrollment-status">Jarayonda</span>
                                                }
                                            </div>
                                            <p className="enrollment-date">
                                                Ro'yxatdan o'tilgan: {new Date(e.created_at).toLocaleDateString()}
                                            </p>
                                            <div className="enrollment-progress">
                                                <div className="progress-bar">
                                                    <div className="progress-fill" style={{ width: `${courseProgress.progress}%` }}></div>
                                                </div>
                                                <small>{courseProgress.progress}% complete</small>
                                            </div>
                                        </div>
                                    )
                                })}
                            </div>
                        )}
                    </section>
                </div>

                <aside className="profile-sidebar">
                    <div className="sidebar-card">
                        <h4>Akkaunt ma'lumotlari</h4>
                        <div className="stat-item">
                            <span className="stat-value">{enrollments.length}</span>
                            <span className="stat-label">Ro'yxatdan o'tilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">
                                {progress.filter(p => p.progress === 100).length}
                            </span>
                            <span className="stat-label">Tugatilgan kurslar</span>
                        </div>
                        <div className="stat-item">
                            <span className="stat-value">0</span>
                            <span className="stat-label">Sertifikatlar</span>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    )
}

export default ProfilePage;
