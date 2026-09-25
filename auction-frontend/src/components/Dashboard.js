import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { getMyAuctions, getMyBids } from '../services/api';
import { formatINR } from '../utils/formatters';

function Dashboard() {
  const { user } = useSelector((state) => state.auth);
  const [myAuctions, setMyAuctions] = useState([]);
  const [myBids, setMyBids] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('auctions');

  useEffect(() => {
    setLoading(true);
    Promise.all([
      getMyAuctions().catch(() => ({ data: [] })),
      getMyBids().catch(() => ({ data: [] })),
    ])
      .then(([auctionsRes, bidsRes]) => {
        setMyAuctions(auctionsRes.data.results || auctionsRes.data || []);
        setMyBids(bidsRes.data.results || bidsRes.data || []);
      })
      .finally(() => setLoading(false));
  }, []);

  const wonAuctions = myBids.filter(
    (a) =>
      a.status === 'ended' &&
      (a.highest_bidder_name === user?.username || a.highest_bidder_username === user?.username)
  );

  return (
    <div className="content-shell" style={{ maxWidth: 1100, margin: '1rem auto' }}>
      {/* Header */}
      <div style={{ marginBottom: '2rem' }}>
        <p className="eyebrow">User Central</p>
        <h1 style={{ fontSize: '2rem' }}>Welcome back, {user?.username || 'Trader'}!</h1>
        <p style={{ color: 'var(--text-muted)' }}>
          Monitor your active listings, track bids in real-time, and review your won auctions.
        </p>
      </div>

      {/* Metrics Row */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
        <div
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: '18px',
            padding: '1.5rem',
            boxShadow: 'var(--shadow-soft)'
          }}
        >
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>My Listed Auctions</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '4px', color: '#ffb366' }}>
            {myAuctions.length}
          </div>
        </div>

        <div
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: '18px',
            padding: '1.5rem',
            boxShadow: 'var(--shadow-soft)'
          }}
        >
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Auctions Bid On</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '4px', color: '#60a5fa' }}>
            {myBids.length}
          </div>
        </div>

        <div
          style={{
            background: 'var(--bg-card)',
            border: '1px solid var(--border)',
            borderRadius: '18px',
            padding: '1.5rem',
            boxShadow: 'var(--shadow-soft)'
          }}
        >
          <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>Won Auctions</span>
          <div style={{ fontSize: '2rem', fontWeight: 800, marginTop: '4px', color: '#34d399' }}>
            {wonAuctions.length}
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: '10px', borderBottom: '1px solid rgba(255,255,255,0.1)', marginBottom: '1.5rem' }}>
        <button
          onClick={() => setActiveTab('auctions')}
          style={{
            background: 'none',
            border: 'none',
            borderBottom: activeTab === 'auctions' ? '2px solid var(--primary)' : '2px solid transparent',
            color: activeTab === 'auctions' ? '#ffb366' : 'var(--text-muted)',
            fontWeight: 700,
            fontSize: '1rem',
            padding: '10px 16px',
            cursor: 'pointer'
          }}
        >
          📦 My Listed Auctions ({myAuctions.length})
        </button>

        <button
          onClick={() => setActiveTab('bids')}
          style={{
            background: 'none',
            border: 'none',
            borderBottom: activeTab === 'bids' ? '2px solid var(--primary)' : '2px solid transparent',
            color: activeTab === 'bids' ? '#ffb366' : 'var(--text-muted)',
            fontWeight: 700,
            fontSize: '1rem',
            padding: '10px 16px',
            cursor: 'pointer'
          }}
        >
          🏷️ Auctions I've Bid On ({myBids.length})
        </button>
      </div>

      {/* Tab Content */}
      {loading ? (
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', padding: '2rem' }}>Loading your dashboard...</p>
      ) : activeTab === 'auctions' ? (
        <div>
          {myAuctions.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem', background: 'var(--bg-card)', borderRadius: '16px' }}>
              <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>You haven't listed any auctions yet.</p>
              <Link to="/create" className="btn btn-primary">
                + Create Your First Auction
              </Link>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.25rem' }}>
              {myAuctions.map((auction) => (
                <div
                  key={auction.id}
                  style={{
                    background: 'var(--bg-card)',
                    border: '1px solid var(--border)',
                    borderRadius: '16px',
                    padding: '1.25rem',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'space-between'
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span
                        style={{
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          padding: '2px 8px',
                          borderRadius: '8px',
                          background: auction.status === 'active' ? 'rgba(43,182,115,0.2)' : 'rgba(239,68,68,0.2)',
                          color: auction.status === 'active' ? '#34d399' : '#f87171'
                        }}
                      >
                        {auction.status.toUpperCase()}
                      </span>
                      <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                        {auction.bid_count ?? 0} bids
                      </span>
                    </div>

                    <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{auction.title}</h3>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                      Current highest bid: <strong style={{ color: '#ffb366' }}>{formatINR(auction.current_highest_bid > 0 ? auction.current_highest_bid : auction.base_price)}</strong>
                    </p>
                  </div>

                  <Link
                    to={`/auction/${auction.id}`}
                    style={{
                      display: 'block',
                      textAlign: 'center',
                      padding: '8px',
                      borderRadius: '8px',
                      background: 'rgba(255,255,255,0.06)',
                      color: '#fff',
                      textDecoration: 'none',
                      fontSize: '0.88rem',
                      fontWeight: 600
                    }}
                  >
                    View Listing →
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        <div>
          {myBids.length === 0 ? (
            <div style={{ textAlign: 'center', padding: '3rem', background: 'var(--bg-card)', borderRadius: '16px' }}>
              <p style={{ color: 'var(--text-muted)', marginBottom: '1rem' }}>You haven't placed bids on any auctions yet.</p>
              <Link to="/" className="btn btn-primary">
                Explore Live Marketplace
              </Link>
            </div>
          ) : (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '1.25rem' }}>
              {myBids.map((auction) => {
                const isLeading =
                  auction.highest_bidder_name === user?.username ||
                  auction.highest_bidder_username === user?.username;

                return (
                  <div
                    key={auction.id}
                    style={{
                      background: 'var(--bg-card)',
                      border: isLeading ? '1px solid rgba(43,182,115,0.4)' : '1px solid var(--border)',
                      borderRadius: '16px',
                      padding: '1.25rem',
                      display: 'flex',
                      flexDirection: 'column',
                      justifyContent: 'space-between'
                    }}
                  >
                    <div>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                        <span
                          style={{
                            fontSize: '0.75rem',
                            fontWeight: 700,
                            padding: '2px 8px',
                            borderRadius: '8px',
                            background: isLeading ? 'rgba(43,182,115,0.2)' : 'rgba(251,191,36,0.2)',
                            color: isLeading ? '#34d399' : '#fbbf24'
                          }}
                        >
                          {isLeading ? '🟢 Highest Bidder' : '🟠 Outbid'}
                        </span>
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                          Status: {auction.status}
                        </span>
                      </div>

                      <h3 style={{ fontSize: '1.1rem', marginBottom: '0.5rem' }}>{auction.title}</h3>
                      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                        Current bid: <strong style={{ color: '#ffb366' }}>{formatINR(auction.current_highest_bid)}</strong>
                      </p>
                    </div>

                    <Link
                      to={`/auction/${auction.id}`}
                      style={{
                        display: 'block',
                        textAlign: 'center',
                        padding: '8px',
                        borderRadius: '8px',
                        background: 'rgba(255,255,255,0.06)',
                        color: '#fff',
                        textDecoration: 'none',
                        fontSize: '0.88rem',
                        fontWeight: 600
                      }}
                    >
                      {isLeading ? 'View Status →' : 'Bid Again →'}
                    </Link>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default Dashboard;
