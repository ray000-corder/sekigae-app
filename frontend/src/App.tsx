// App.tsx
import { Routes, Route, Navigate } from "react-router-dom";
import type { ReactNode } from "react"; // ← 追加！
import LoginPage from "./pages/LoginPage";
import DashboardPage from "./pages/DashboardPage";
import RegisterPage from "./pages/RegisterPage";
import SeatChartPage from "./pages/SeatChartPage";
import StudentManagerPage from "./pages/StudentManagerPage";

const isAuthenticated = () => localStorage.getItem("access_token") !== null;

type ProtectedRouteProps = {
  children: ReactNode;
};

const ProtectedRoute = ({ children }: ProtectedRouteProps) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return <>{children}</>; // ReactNode を返すときは fragment で囲む
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
        <Route index element={<SeatChartPage />} />
        <Route path="students" element={<StudentManagerPage />} />
      </Route>
    </Routes>
  );
}

export default App;
