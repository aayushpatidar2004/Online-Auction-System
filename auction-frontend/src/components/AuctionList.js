import React, { useEffect, useState, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { getAuctions } from '../services/api';
import { formatINR } from '../utils/formatters';

const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const baseUrl = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/api$/, '');
  return `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}`;
};

const formatTimeLeft = (endTimeStr) => {
  if (!endTimeStr) return 'No limit';
  const total = Date.parse(endTimeStr) - Date.now();
  if (total <= 0) return 'Ended';
  const hours = Math.floor(total / (1000 * 60 * 60));
  const minutes = Math.floor((total / 1000 / 60) % 60);
  const seconds = Math.floor((total / 1000) % 60);
  if (hours > 24) {
    const days = Math.floor(hours / 24);
    return `${days}d ${hours % 24}h left`;
  }
  return `${hours}h ${minutes}m ${seconds}s left`;
};

const CATEGORIES = [
  { id: 'all', label: 'All Items' },
  { id: 'electronics', label: 'Electronics' },
  { id: 'fashion', label: 'Fashion' },
  { id: 'home', label: 'Home' },
  { id: 'vehicles', label: 'Vehicles' },
  { id: 'art', label: 'Art & Collectibles' },
  { id: 'general', label: 'General' },
];

function AuctionList() {
  const [auctions, setAuctions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [now, setNow] = useState(Date.now());

  // Update countdown ticks every second
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    setLoading(true);
    getAuctions()
      .then(({ data }) => {
        setAuctions(data.results || data);
      })
      .catch(() => setAuctions([]))
      .finally(() => setLoading(false));
  }, []);

  const filteredAuctions = useMemo(() => {
    return auctions.filter((item) => {
      const matchesCategory =
        selectedCategory === 'all' || (item.category && item.category.toLowerCase() === selectedCategory);
      const matchesSearch =
        !searchQuery ||
        item.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.description?.toLowerCase().includes(searchQuery.toLowerCase());
      return matchesCategory && matchesSearch;
    });
  }, [auctions, selectedCategory, searchQuery]);

  return (
    <div className="content-shell">
      {/* Hero Showcase */}
      <section className="hero-banner">
        <div>
          <p className="eyebrow">⚡ Live Bidding Exchange</p>
          <h1>Bid on India’s Best Finds.</h1>
          <p className="hero-copy">
            Explore authentic listings, verified collectibles, and high-stakes auctions in real-time with instant bidding.
          </p>
        </div>
        <div className="hero-metric">
          <span>{auctions.length}</span>
          <small>total listings</small>
        </div>
      </section>

      {/* Filter and Search Bar */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '12px', alignItems: 'center', justifyContent: 'space-between', margin: '2rem 0 1.5rem' }}>
        {/* Category Tabs */}
        <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px', maxWidth: '100%' }}>
          {CATEGORIES.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              style={{
                padding: '8px 16px',
                borderRadius: '24px',
                fontSize: '0.85rem',
                fontWeight: 600,
                border: selectedCategory === cat.id ? '1px solid var(--primary)' : '1px solid rgba(255, 255, 255, 0.1)',
                background: selectedCategory === cat.id ? 'rgba(255, 153, 51, 0.2)' : 'rgba(255, 255, 255, 0.04)',
                color: selectedCategory === cat.id ? '#ffb366' : 'var(--text-muted)',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
                whiteSpace: 'nowrap'
              }}
            >
              {cat.label}
            </button>
          ))}
        </div>

        {/* Search Box */}
        <div style={{ position: 'relative', minWidth: '240px' }}>
          <input
            type="text"
            placeholder="Search items..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            style={{
              width: '100%',
              padding: '9px 14px',
              borderRadius: '20px',
              background: 'rgba(255, 255, 255, 0.05)',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              color: 'var(--text-light)',
              fontSize: '0.88rem',
              outline: 'none'
            }}
          />
        </div>
      </div>

      <section className="section-header">
        <h2>Active & Upcoming Auctions</h2>
        <span style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
          Showing {filteredAuctions.length} of {auctions.length} items
        </span>
      </section>

      {/* Loading Skeleton */}
      {loading ? (
        <div className="auction-grid">
          {[1, 2, 3, 4, 5, 6].map((n) => (
            <article key={n} className="auction-card" style={{ opacity: 0.6, animation: 'pulse 1.5s infinite' }}>
              <div style={{ height: '200px', background: 'rgba(255,255,255,0.05)' }} />
              <div className="auction-card-body" style={{ padding: '1.25rem' }}>
                <div style={{ height: '20px', width: '60%', background: 'rgba(255,255,255,0.08)', borderRadius: '4px', marginBottom: '12px' }} />
                <div style={{ height: '14px', width: '90%', background: 'rgba(255,255,255,0.04)', borderRadius: '4px', marginBottom: '8px' }} />
                <div style={{ height: '36px', background: 'rgba(255,255,255,0.06)', borderRadius: '8px', marginTop: '1rem' }} />
              </div>
            </article>
          ))}
        </div>
      ) : filteredAuctions.length === 0 ? (
        <div className="empty-card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
          <div className="empty-icon" style={{ fontSize: '3rem', marginBottom: '1rem' }}>📦</div>
          <h3 style={{ marginBottom: '0.5rem' }}>No Auctions Found</h3>
          <p style={{ color: 'var(--text-muted)' }}>
            {searchQuery || selectedCategory !== 'all'
              ? 'Try adjusting your search criteria or category filter.'
              : 'There are currently no listings available. Be the first to list an item!'}
          </p>
          <Link
            to="/create"
            className="register-btn"
            style={{ display: 'inline-block', marginTop: '1.5rem', padding: '10px 24px' }}
          >
            Create an Auction
          </Link>
        </div>
      ) : (
        <div className="auction-grid">
          {filteredAuctions.map((auction) => {
            const isEnded = auction.status === 'ended' || (auction.end_time && Date.parse(auction.end_time) <= now);
            const timeLeft = formatTimeLeft(auction.end_time);

            return (
              <article key={auction.id} className="auction-card">
                <div style={{ position: 'relative', overflow: 'hidden' }}>
                  {auction.image ? (
                    <img
                      src={getMediaUrl(auction.image)}
                      alt={auction.title}
                      className="auction-card-image"
                      style={{ objectFit: 'cover', height: '220px', width: '100%' }}
                    />
                  ) : (
                    <div
                      className="auction-card-image"
                      style={{
                        height: '220px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        background: 'linear-gradient(135deg, rgba(255,153,51,0.15), rgba(19,136,8,0.15))',
                        fontSize: '3rem'
                      }}
                    >
                      🏷️
                    </div>
                  )}

                  {/* Time Badge Over Image */}
                  <div
                    style={{
                      position: 'absolute',
                      top: '12px',
                      right: '12px',
                      background: isEnded ? 'rgba(239, 68, 68, 0.9)' : 'rgba(15, 23, 42, 0.85)',
                      backdropFilter: 'blur(8px)',
                      color: '#fff',
                      padding: '4px 10px',
                      borderRadius: '12px',
                      fontSize: '0.78rem',
                      fontWeight: 600,
                      boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
                    }}
                  >
                    {isEnded ? '🔴 Ended' : `⏱️ ${timeLeft}`}
                  </div>

                  {/* Category Pill */}
                  <div
                    style={{
                      position: 'absolute',
                      bottom: '12px',
                      left: '12px',
                      background: 'rgba(0,0,0,0.7)',
                      backdropFilter: 'blur(6px)',
                      color: 'var(--text-light)',
                      padding: '3px 10px',
                      borderRadius: '8px',
                      fontSize: '0.72rem',
                      textTransform: 'uppercase',
                      letterSpacing: '0.04em',
                      fontWeight: 700
                    }}
                  >
                    {auction.category}
                  </div>
                </div>

                <div className="auction-card-body">
                  <div className="auction-card-topline">
                    <span
                      className="status-pill"
                      style={{
                        background: isEnded ? 'rgba(239,68,68,0.2)' : 'rgba(43,182,115,0.2)',
                        color: isEnded ? '#f87171' : '#34d399',
                        border: isEnded ? '1px solid rgba(239,68,68,0.4)' : '1px solid rgba(43,182,115,0.4)'
                      }}
                    >
                      {isEnded ? 'Closed' : 'Active'}
                    </span>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                      {auction.bid_count ?? 0} {auction.bid_count === 1 ? 'bid' : 'bids'}
                    </span>
                  </div>

                  <h3 className="auction-card-title">{auction.title}</h3>
                  <p className="auction-card-description">
                    {auction.description?.length > 100
                      ? `${auction.description.slice(0, 100)}...`
                      : auction.description}
                  </p>

                  <div className="auction-card-meta" style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span>
                      <strong>Seller:</strong> {auction.seller_name || auction.seller_username}
                    </span>
                    <span style={{ textTransform: 'capitalize' }}>
                      <strong>Cond:</strong> {auction.condition}
                    </span>
                  </div>

                  <div className="auction-card-price-row">
                    <div>
                      <label>Current Bid</label>
                      <strong style={{ color: '#ffb366', fontSize: '1.15rem' }}>
                        {formatINR(auction.current_highest_bid > 0 ? auction.current_highest_bid : auction.base_price)}
                      </strong>
                    </div>
                    <div>
                      <label>Base Price</label>
                      <strong>{formatINR(auction.base_price)}</strong>
                    </div>
                  </div>

                  <div className="auction-card-footer" style={{ marginTop: '1rem' }}>
                    <Link
                      to={`/auction/${auction.id}`}
                      className="detail-link"
                      style={{
                        display: 'block',
                        textAlign: 'center',
                        padding: '10px 16px',
                        background: isEnded
                          ? 'rgba(255,255,255,0.08)'
                          : 'linear-gradient(135deg, var(--primary) 0%, var(--primary-strong) 100%)',
                        color: '#fff',
                        fontWeight: 700,
                        borderRadius: '10px',
                        textDecoration: 'none',
                        boxShadow: isEnded ? 'none' : '0 4px 15px rgba(255,153,51,0.3)',
                        transition: 'transform 0.15s ease'
                      }}
                    >
                      {isEnded ? 'View Result' : 'Place Bid / View'}
                    </Link>
                  </div>
                </div>
              </article>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default AuctionList;
