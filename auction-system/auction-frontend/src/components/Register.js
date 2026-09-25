import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { register } from '../services/api';

function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: '', email: '', phone: '', password: '', password2: '' });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await register(form);
      toast.success('Registration successful. Please login.');
      navigate('/login');
    } catch (error) {
      const detail = error?.response?.data;
      const message = detail && typeof detail === 'object' ? Object.values(detail).flat().join(' ') : 'Registration failed';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 460, margin: '3rem auto', padding: '2rem', border: '1px solid #e5e7eb', borderRadius: 12 }}>
      <h2>Create account</h2>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 14 }}>
          <label>Username</label>
          <input name="username" value={form.username} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <div style={{ marginBottom: 14 }}>
          <label>Email</label>
          <input type="email" name="email" value={form.email} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <div style={{ marginBottom: 14 }}>
          <label>Phone</label>
          <input name="phone" value={form.phone} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} />
        </div>
        <div style={{ marginBottom: 14 }}>
          <label>Password</label>
          <input type="password" name="password" value={form.password} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <div style={{ marginBottom: 14 }}>
          <label>Confirm password</label>
          <input type="password" name="password2" value={form.password2} onChange={handleChange} style={{ width: '100%', padding: 8, marginTop: 6 }} required />
        </div>
        <button type="submit" disabled={loading} style={{ width: '100%', padding: 10, background: '#111827', color: '#fff', border: 'none', borderRadius: 8 }}>
          {loading ? 'Creating account...' : 'Register'}
        </button>
      </form>
      <p style={{ marginTop: 12 }}>
        Already registered? <Link to="/login">Login</Link>
      </p>
    </div>
  );
}

export default Register;
