import 'bootstrap/dist/css/bootstrap.min.css';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import RoadmapPage from './pages/RoadmapPage';
import CoursesPage from './pages/CoursesPage';
import CoursePage from './pages/CoursePage';
import LessonDetailPage from './pages/LessonDetailPage';
import QuizPage from './pages/QuizPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import TasksListPage from './pages/TasksListPage';
import TaskPage from './pages/TaskPage';
import LeaderboardPage from './pages/LeaderboardPage';
import PlacementTestPage from './pages/PlacementTestPage';
import Navigation from './components/Navbar';
import { AuthProvider } from './context/AuthContext';
import { ThemeProvider } from './context/ThemeContext';


function App() {
  return (
    <ThemeProvider>
    <Router>
      <AuthProvider>
        <Navigation />
        <Routes>
          <Route path="/" element={<RoadmapPage />} />
          <Route path="/courses" element={<CoursesPage />} />
          <Route path="/courses/:id" element={<CoursePage />} />
          <Route path="/lessons/:id" element={<LessonDetailPage />} />
          <Route path="/quiz/:id" element={<QuizPage />} />
          <Route path="/lessons/:id/quiz" element={<QuizPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/tasks" element={<TasksListPage />} />
          <Route path="/tasks/:id" element={<TaskPage />} />
          <Route path="/leaderboard" element={<LeaderboardPage />} />
          <Route path="/placement-test" element={<PlacementTestPage />} />
        </Routes>
      </AuthProvider>
    </Router>
    </ThemeProvider>
  );
}

export default App;
