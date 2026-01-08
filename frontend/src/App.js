import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/HomePage';
import CoursePage from './pages/CoursePage';
import LessonPage from './pages/LessonPage';
import QuizPage from './pages/QuizPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import Navigation from './components/Navbar';
import { AuthProvider } from './context/AuthContext';
import LessonDetailPage from './pages/LessonDetailPage';


function App() {
  return (
    <Router>
      <AuthProvider>
        <Navigation />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/courses/:id" element={<CoursePage />} />
          <Route path="/lessons/:id" element={<LessonDetailPage />} />
          <Route path="/quiz/:id" element={<QuizPage />} />
          <Route path="/lessons/:id/quiz" element={<QuizPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<ProfilePage />} />
        </Routes>
      </AuthProvider>
    </Router>
  );
}


export default App;
