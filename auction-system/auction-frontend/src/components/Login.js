import React, { useState } from 'react';
import { useDispatch } from 'react-redux';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { login, getProfile } from '../services/api';
import { setCredentials } from '../store/authSlice';

function Login() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', password: '' });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const { data } = await login(form);
      dispatch(setCredentials({ access: data.access, refresh: data.refresh, user: null }));
      const profileResponse = await getProfile();
      const user = profileResponse.data;
      dispatch(setCredentials({ access: data.access, refresh: data.refresh, user }));
      toast.success('Logged in successfully');
      navigate(user?.is_staff || user?.is_superuser ? '/site-admin' : '/');
    } catch (error) {
      const detail = error?.response?.data;
      const message = detail && typeof detail === 'object' ? Object.values(detail).flat().join(' ') : (detail || 'Login failed');
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 460, margin: '3rem auto', padding: '2rem', border: '1px solid #e5e7eb', borderRadius: 12 }}>
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 14 }}>
          <label>Username</label>
          <input name="username" value={form.username} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <div style={{ marginBottom: 14 }}>
          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <button type="submit" disabled={loading} style={{ width: '100%', padding: 10, background: '#111827', color: '#fff', border: 'none', borderRadius: 8 }}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
      </form>
      <p style={{ marginTop: 12 }}>
        Need an account? <Link to="/register">Register</Link>
      </p>
    </div>
  );
}

export default Login;
