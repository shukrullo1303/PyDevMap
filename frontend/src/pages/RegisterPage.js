import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/pages/AuthPages.css';

const RegisterPage = () => {
    const [data, setData] = useState({
        username: '',
        email: '',
        password: '',
        first_name: '',
        last_name: ''
    });
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();
    const { register } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);

        if (data.password.length < 6) {
            setError('Password must be at least 6 characters');
            setLoading(false);
            return;
        }

        if (!data.username || !data.email) {
            setError('Username and email are required');
            setLoading(false);
            return;
        }

        try {
            await register(data);
            nav('/login');
        } catch (err) {
            const errorMsg = err.response?.data?.detail ||
                err.response?.data?.email?.[0] ||
                err.response?.data?.username?.[0] ||
                err.response?.data ||
                err.message;
            setError(typeof errorMsg === 'object' ? JSON.stringify(errorMsg) : errorMsg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>Create your account</h1>
                    <p>Join our learning community today</p>
                </div>

                {error && (
                    <div className="auth-error">
                        <strong>Error:</strong> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label className="form-label">First Name</label>
                        <input
                            type="text"
                            value={data.first_name}
                            onChange={(e) => setData({ ...data, first_name: e.target.value })}
                            placeholder="John"
                            className="form-control"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Last Name</label>
                        <input
                            type="text"
                            value={data.last_name}
                            onChange={(e) => setData({ ...data, last_name: e.target.value })}
                            placeholder="Doe"
                            className="form-control"
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            value={data.username}
                            onChange={(e) => setData({ ...data, username: e.target.value })}
                            placeholder="johndoe"
                            className="form-control"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Email address</label>
                        <input
                            type="email"
                            value={data.email}
                            onChange={(e) => setData({ ...data, email: e.target.value })}
                            placeholder="you@example.com"
                            className="form-control"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            value={data.password}
                            onChange={(e) => setData({ ...data, password: e.target.value })}
                            placeholder="••••••••"
                            className="form-control"
                            required
                        />
                        <small className="form-helper">At least 6 characters</small>
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary auth-submit"
                        disabled={loading}
                    >
                        {loading ? 'Creating account...' : 'Create account'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>Already have an account? <Link to="/login">Sign in</Link></p>
                </div>
            </div>
        </div>
    );
};

export default RegisterPage;
