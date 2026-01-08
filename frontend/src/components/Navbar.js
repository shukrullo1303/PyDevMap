import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import '../styles/components/Navbar.css';

const Navigation = () => {
    const { user, logout } = useAuth();
    const [q, setQ] = useState('');
    const [mobileOpen, setMobileOpen] = useState(false);
    const nav = useNavigate();

    const handleLogout = () => {
        logout();
        nav('/');
    };

    // const doSearch = (e) => {
    //     e.preventDefault();
    //     nav(`/?q=${encodeURIComponent(q)}`);
    //     setQ('');
    // };

    return (
        <nav className="navbar">
            <div className="site-container navbar-content">
                <Link to="/" className="nav-brand">OsonMarketing</Link>

                {/* <form onSubmit={doSearch} className="search-form">
                    <input
                        type="text"
                        placeholder="Kurslar bo'yicha qidiruv"
                        value={q}
                        onChange={(e) => setQ(e.target.value)}
                        className="search-input"
                    />
                </form> */}

                <div className="nav-right">
                    {user ? (
                        <>
                            <Link to="/profile" className="nav-user">
                                <span className="user-avatar">{user.username?.[0]?.toUpperCase() || 'U'}</span>
                                <span className="user-name">{user.username || user.email}</span>
                            </Link>
                            <button onClick={handleLogout} className="btn btn-outline-primary">
                                Chiqish
                            </button>
                        </>
                    ) : (
                        <>
                            <Link to="/login" className="btn btn-primary">
                                Kirish
                            </Link>
                            <Link to="/register" className="btn btn-outline-primary">
                                Registratsiya
                            </Link>
                        </>
                    )}
                </div>

                <button
                    className="mobile-toggle"
                    onClick={() => setMobileOpen(!mobileOpen)}
                >
                    ☰
                </button>
            </div>

            {mobileOpen && (
                <div className="mobile-menu">
                    {user && (
                        <>
                            <Link to="/profile" className="mobile-link">Profil</Link>
                            <button onClick={handleLogout} className="mobile-link">Chiqish</button>
                        </>
                    )}
                    {!user && (
                        <>
                            <Link to="/login" className="mobile-link">Kirish</Link>
                            <Link to="/register" className="mobile-link">Registratsiya</Link>
                        </>
                    )}
                </div>
            )}
        </nav>
    );
};

export default Navigation;
