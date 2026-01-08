import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/pages/AuthPages.css';

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);
    const nav = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setLoading(true);
        try {
            await login(username, password);
            nav('/profile');
        } catch (err) {
            setError(err.response?.data?.detail || err.message || 'Login failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <div className="auth-header">
                    <h1>Welcome back</h1>
                    <p>Sign in to access your courses</p>
                </div>

                {error && (
                    <div className="auth-error">
                        <strong>Error:</strong> {error}
                    </div>
                )}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="form-group">
                        <label className="form-label">Username</label>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            placeholder="Enter your username"
                            className="form-control"
                            required
                        />
                    </div>

                    <div className="form-group">
                        <label className="form-label">Password</label>
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="••••••••"
                            className="form-control"
                            required
                        />
                    </div>

                    <button
                        type="submit"
                        className="btn btn-primary auth-submit"
                        disabled={loading}
                    >
                        {loading ? 'Signing in...' : 'Sign in'}
                    </button>
                </form>

                <div className="auth-footer">
                    <p>Don't have an account? <Link to="/register">Create one</Link></p>
                </div>
            </div>
        </div>
    );
};

export default LoginPage;
