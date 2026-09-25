import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { logout } from '../store/authSlice';

function Navbar() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { isAuthenticated, user } = useSelector((state) => state.auth);
  const isAdmin = !!(user?.is_staff || user?.is_superuser);

  const handleLogout = () => {
    dispatch(logout());
    navigate('/login');
  };

  return (
    <nav className="topbar">
      <div className="nav-group nav-left">
        <Link to="/" className="brand-link">BharatBazaar</Link>
        <Link to="/" className="nav-link">Home</Link>
        {isAuthenticated && <Link to="/create" className="nav-link">Create</Link>}
        {isAuthenticated && <Link to="/dashboard" className="nav-link">Dashboard</Link>}
        {isAuthenticated && isAdmin && <Link to="/site-admin" className="nav-link">Admin</Link>}
      </div>

      <div className="nav-group nav-right">
        {isAuthenticated ? (
          <>
            <Link to="/profile" className="profile-link">{user?.username || 'Profile'}</Link>
            <button className="logout-btn" onClick={handleLogout}>
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login" className="nav-link">Login</Link>
            <Link to="/register" className="register-btn">Register</Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
