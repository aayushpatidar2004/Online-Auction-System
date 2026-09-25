import React, { useEffect, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { getAuctions } from '../services/api';
import { formatINR } from '../utils/formatters';

function AdminPanel() {
  const { user } = useSelector((state) => state.auth);
  const [auctions, setAuctions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getAuctions()
      .then(({ data }) => {
        const items = data?.results || data || [];
        setAuctions(items);
      })
      .catch(() => setAuctions([]))
      .finally(() => setLoading(false));
  }, []);

  const summary = useMemo(() => {
    const totalValue = auctions.reduce((sum, item) => sum + Number(item.base_price || 0), 0);
    const active = auctions.filter((item) => item.status === 'active').length;
    const ended = auctions.filter((item) => item.status === 'ended').length;

    return {
      totalAuctions: auctions.length,
      active,
      ended,
      totalValue,
    };
  }, [auctions]);

  if (!user || !(user.is_staff || user.is_superuser)) {
    return (
      <div className="content-shell">
        <div className="card" style={{ maxWidth: 560, margin: '4rem auto', padding: '2rem', textAlign: 'center' }}>
          <h2>Access denied</h2>
          <p style={{ marginTop: '0.8rem', color: '#a4b4cf' }}>Only site administrators can access this panel.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="content-shell">
      <div className="page-header">
        <h1>Admin panel</h1>
        <p>Manage auctions and monitor marketplace activity.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem', marginBottom: '2rem' }}>
        <div className="card" style={{ padding: '1.2rem' }}>
          <p style={{ color: '#a4b4cf', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem' }}>Total listings</p>
          <h3 style={{ fontSize: '2rem', marginTop: '0.3rem' }}>{summary.totalAuctions}</h3>
        </div>
        <div className="card" style={{ padding: '1.2rem' }}>
          <p style={{ color: '#a4b4cf', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem' }}>Active</p>
          <h3 style={{ fontSize: '2rem', marginTop: '0.3rem' }}>{summary.active}</h3>
        </div>
        <div className="card" style={{ padding: '1.2rem' }}>
          <p style={{ color: '#a4b4cf', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem' }}>Ended</p>
          <h3 style={{ fontSize: '2rem', marginTop: '0.3rem' }}>{summary.ended}</h3>
        </div>
        <div className="card" style={{ padding: '1.2rem' }}>
          <p style={{ color: '#a4b4cf', textTransform: 'uppercase', letterSpacing: '0.08em', fontSize: '0.7rem' }}>Base value</p>
          <h3 style={{ fontSize: '2rem', marginTop: '0.3rem' }}>{formatINR(summary.totalValue)}</h3>
        </div>
      </div>

      <div className="card" style={{ padding: '1.2rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <h3>Marketplace listings</h3>
          <Link to="/create" className="btn btn-primary btn-sm">Create auction</Link>
        </div>

        {loading ? (
          <div className="loading-container">
            <div className="spinner" />
          </div>
        ) : auctions.length === 0 ? (
          <p style={{ color: '#a4b4cf' }}>No auctions found.</p>
        ) : (
          <div style={{ display: 'grid', gap: '0.9rem' }}>
            {auctions.map((auction) => (
              <div key={auction.id} style={{ display: 'flex', justifyContent: 'space-between', gap: '1rem', padding: '1rem', border: '1px solid rgba(148,163,184,0.18)', borderRadius: '14px', background: 'rgba(15,23,42,0.45)' }}>
                <div>
                  <h4 style={{ marginBottom: '0.25rem' }}>{auction.title}</h4>
                  <p style={{ color: '#a4b4cf', marginBottom: '0.35rem' }}>Seller: {auction.seller_username || 'Unknown'}</p>
                  <p style={{ color: '#a4b4cf', marginBottom: 0 }}>Status: {auction.status}</p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <p style={{ fontWeight: 700, marginBottom: '0.5rem' }}>{formatINR(auction.base_price || 0)}</p>
                  <Link to={`/auction/${auction.id}`} className="detail-link">View</Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default AdminPanel;
