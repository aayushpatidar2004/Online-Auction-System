import React, { useEffect, useState } from 'react';
import { toast } from 'react-toastify';
import { getProfile, updateProfile } from '../services/api';
import { formatINR } from '../utils/formatters';

function Profile() {
  const [profile, setProfile] = useState(null);
  const [form, setForm] = useState({ email: '', phone: '' });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    setLoading(true);
    getProfile()
      .then(({ data }) => {
        setProfile(data);
        setForm({
          email: data.email || '',
          phone: data.phone || '',
        });
      })
      .catch(() => toast.error('Failed to load profile.'))
      .finally(() => setLoading(false));
  }, []);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const { data } = await updateProfile(form);
      setProfile(data);
      toast.success('🎉 Profile updated successfully!');
    } catch (error) {
      const msg = error?.response?.data?.phone?.[0] || error?.response?.data?.email?.[0] || 'Profile update failed.';
      toast.error(msg);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-muted)' }}>Loading profile...</p>;
  }

  return (
    <div className="content-shell" style={{ maxWidth: 760, margin: '1.5rem auto' }}>
      <div
        className="card"
        style={{
          background: 'var(--bg-card)',
          border: '1px solid var(--border)',
          borderRadius: '24px',
          padding: '2.5rem',
          boxShadow: 'var(--shadow-soft)'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '1.5rem', marginBottom: '1.5rem' }}>
          <div
            style={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, var(--primary), var(--secondary))',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '2rem',
              fontWeight: 800,
              color: '#fff',
              boxShadow: '0 8px 20px rgba(0,0,0,0.3)'
            }}
          >
            {profile?.username?.charAt(0).toUpperCase() || 'U'}
          </div>

          <div>
            <h1 style={{ fontSize: '1.75rem', marginBottom: '4px' }}>{profile?.username}</h1>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem' }}>
              Member since {profile?.created_at ? new Date(profile.created_at).toLocaleDateString() : '2026'}
            </p>
          </div>
        </div>

        {/* Financial & Rating Summary */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
          <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem 1.25rem', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Wallet Balance</span>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#34d399', marginTop: '4px' }}>
              {formatINR(profile?.wallet_balance || 0)}
            </div>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem 1.25rem', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Seller Rating</span>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#fbbf24', marginTop: '4px' }}>
              ⭐ {Number(profile?.seller_rating || 0).toFixed(1)} / 5.0
            </div>
          </div>

          <div style={{ background: 'rgba(255,255,255,0.04)', padding: '1rem 1.25rem', borderRadius: '16px', border: '1px solid rgba(255,255,255,0.06)' }}>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Buyer Rating</span>
            <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#60a5fa', marginTop: '4px' }}>
              ⭐ {Number(profile?.buyer_rating || 0).toFixed(1)} / 5.0
            </div>
          </div>
        </div>

        {/* Profile Edit Form */}
        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="form-group">
            <label htmlFor="username" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
              Username
            </label>
            <input
              id="username"
              className="form-control"
              value={profile?.username || ''}
              disabled
              style={{ opacity: 0.6, cursor: 'not-allowed' }}
            />
            <small style={{ color: 'var(--text-muted)', fontSize: '0.78rem' }}>Username cannot be modified.</small>
          </div>

          <div className="form-group">
            <label htmlFor="email" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
              Email Address
            </label>
            <input
              id="email"
              type="email"
              className="form-control"
              name="email"
              value={form.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="phone" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
              Phone Number
            </label>
            <input
              id="phone"
              type="tel"
              className="form-control"
              name="phone"
              placeholder="+91 98765 43210"
              value={form.phone}
              onChange={handleChange}
            />
          </div>

          <button
            type="submit"
            className="btn btn-primary"
            disabled={saving}
            style={{ marginTop: '1rem', padding: '12px', fontSize: '1rem', fontWeight: 700 }}
          >
            {saving ? 'Updating Profile...' : 'Save Profile Changes'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
