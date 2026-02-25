import React, { createContext, useContext, useEffect, useState } from 'react';
import { login as svcLogin, register as svcRegister, getProfile as svcProfile, setTokens as svcSetTokens, logout as svcLogout } from '../services/auth';

const AuthContext = createContext(null);
export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Profilni yuklash
  const loadProfile = async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      setUser(null);
      setLoading(false);
      return;
    }
    try {
      const res = await svcProfile();
      setUser(res.data);
    } catch {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProfile();
  }, []);

  // Login funksiyasi
  const login = async (username, password) => {
    const res = await svcLogin(username, password); // API login
    const { access, refresh } = res.data;

    // TOKENLARNI LOCALSTORAGE GA SAQLASH
    svcSetTokens({ access, refresh });

    // Foydalanuvchi profilini yuklash
    await loadProfile();
    return res;
  };

  // Register
  const register = async (payload) => {
    const res = await svcRegister(payload);
    return res;
  };

  // Logout
  const logout = () => {
    svcLogout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
