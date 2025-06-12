import { Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import RegisterPage from './pages/RegisterPage';
import SeatChartPage from './pages/SeatChartPage';
import StudentManagerPage from './pages/StudentManagerPage';

const isAuthenticated = () => localStorage.getItem('access_token') !== null;

const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <DashboardPage />
          </ProtectedRoute>
        }
      >
        {/* ↓ DashboardPage の <Outlet/> に表示される子ルート */}
        <Route index element={<SeatChartPage />} />
        <Route path="students" element={<StudentManagerPage />} />
      </Route>
    </Routes>
  );
}

export default App;