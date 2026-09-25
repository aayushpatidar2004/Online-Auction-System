import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from './components/Navbar';
import AuctionList from './components/AuctionList';
import AuctionDetail from './components/AuctionDetail';
import CreateAuction from './components/CreateAuction';
import Dashboard from './components/Dashboard';
import Profile from './components/Profile';
import Login from './components/Login';
import Register from './components/Register';
import AdminPanel from './components/AdminPanel';
import { useSelector } from 'react-redux';

function PrivateRoute({ children }) {
  const { token } = useSelector((state) => state.auth);
  return token ? children : <Navigate to="/login" replace />;
}

function AdminRoute({ children }) {
  const { token, user } = useSelector((state) => state.auth);
  const isAdmin = !!(user?.is_staff || user?.is_superuser);
  return token && isAdmin ? children : <Navigate to="/login" replace />;
}

function App() {
  return (
    <Router>
      <div className="app-shell">
        <div className="bg-orb orb-one" />
        <div className="bg-orb orb-two" />
        <Navbar />
        <main className="page-content">
          <Routes>
            <Route path="/" element={<AuctionList />} />
            <Route path="/auction/:id" element={<AuctionDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/create" element={<PrivateRoute><CreateAuction /></PrivateRoute>} />
            <Route path="/dashboard" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            <Route path="/profile" element={<PrivateRoute><Profile /></PrivateRoute>} />
            <Route path="/site-admin" element={<AdminRoute><AdminPanel /></AdminRoute>} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
      <ToastContainer
        position="bottom-right"
        autoClose={4000}
        hideProgressBar={false}
        newestOnTop
        closeOnClick
        pauseOnHover
        theme="dark"
      />
    </Router>
  );
}

export default App;
