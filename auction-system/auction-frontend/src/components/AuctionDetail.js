import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useSelector } from 'react-redux';
import { toast } from 'react-toastify';
import { getAuctionDetail, getBidHistory, placeBid, initiatePayment } from '../services/api';
import { formatINR } from '../utils/formatters';

const getMediaUrl = (path) => {
  if (!path) return null;
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  const baseUrl = (process.env.REACT_APP_API_URL || 'http://localhost:8000/api').replace(/\/api$/, '');
  return `${baseUrl}${path.startsWith('/') ? '' : '/'}${path}`;
};

function formatTimeLeft(endTimeStr) {
  if (!endTimeStr) return 'No limit';
  const total = Date.parse(endTimeStr) - Date.now();
  if (total <= 0) return { text: 'Auction Closed', isEnded: true };
  const hours = Math.floor(total / (1000 * 60 * 60));
  const minutes = Math.floor((total / 1000 / 60) % 60);
  const seconds = Math.floor((total / 1000) % 60);

  if (hours > 24) {
    const days = Math.floor(hours / 24);
    return { text: `${days}d ${hours % 24}h ${minutes}m left`, isEnded: false };
  }
  return { text: `${hours}h ${minutes}m ${seconds}s left`, isEnded: false };
}

function AuctionDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user, isAuthenticated } = useSelector((state) => state.auth);

  const [auction, setAuction] = useState(null);
  const [bids, setBids] = useState([]);
  const [bidAmount, setBidAmount] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [paying, setPaying] = useState(false);
  const [now, setNow] = useState(Date.now());

  // Refresh clock every second for countdown
  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, []);

  const loadData = useCallback(async (isInitial = false) => {
    try {
      if (isInitial) setLoading(true);
      const [auctionRes, historyRes] = await Promise.all([
        getAuctionDetail(id),
        getBidHistory(id).catch(() => ({ data: [] })),
      ]);

      const auctionData = auctionRes.data;
      setAuction(auctionData);

      const historyData = Array.isArray(historyRes.data)
        ? historyRes.data
        : auctionData.bid_history || [];
      setBids(historyData);

      // Auto-set suggested minimum bid
      if (isInitial) {
        const highest = Number(auctionData.current_highest_bid || 0);
        const base = Number(auctionData.base_price || 0);
        const nextMin = highest > 0 ? highest + 10 : base;
        setBidAmount(nextMin.toFixed(2));
      }
    } catch (err) {
      if (isInitial) {
        toast.error('Unable to load auction details.');
      }
    } finally {
      if (isInitial) setLoading(false);
    }
  }, [id]);

  // Initial load
  useEffect(() => {
    loadData(true);
  }, [loadData]);

  // Live polling every 3 seconds for active auctions
  useEffect(() => {
    if (!auction) return;
    const isEnded = auction.status === 'ended' || (auction.end_time && Date.parse(auction.end_time) <= now);
    if (isEnded) return;

    const pollInterval = setInterval(() => {
      loadData(false);
    }, 3000);

    return () => clearInterval(pollInterval);
  }, [auction, loadData, now]);

  const currentHighest = useMemo(() => {
    if (!auction) return 0;
    return Number(auction.current_highest_bid || 0);
  }, [auction]);

  const basePrice = useMemo(() => {
    if (!auction) return 0;
    return Number(auction.base_price || 0);
  }, [auction]);

  const minNextBid = useMemo(() => {
    return currentHighest > 0 ? currentHighest + 1 : basePrice;
  }, [currentHighest, basePrice]);

  const handleQuickIncrement = (inc) => {
    const curr = Number(bidAmount) || minNextBid;
    setBidAmount((curr + inc).toFixed(2));
  };

  const handleBidSubmit = async (e) => {
    e.preventDefault();
    if (!isAuthenticated) {
      toast.info('Please log in to place a bid.');
      navigate('/login');
      return;
    }

    const val = Number(bidAmount);
    if (Number.isNaN(val) || val < minNextBid) {
      toast.error(`Your bid must be at least ${formatINR(minNextBid)}.`);
      return;
    }

    setSubmitting(true);
    try {
      await placeBid(id, val);
      toast.success('🎉 Bid placed successfully!');
      await loadData(false);
      setBidAmount((val + 10).toFixed(2));
    } catch (error) {
      const msg = error?.response?.data?.detail || 'Failed to place bid. Please try again.';
      toast.error(msg);
    } finally {
      setSubmitting(false);
    }
  };

  const handlePayNow = async () => {
    setPaying(true);
    try {
      const { data } = await initiatePayment(auction.id);
      toast.success(`Payment initiated! Transaction ID: ${data.payment_id}`);
      navigate('/dashboard');
    } catch (err) {
      toast.error(err?.response?.data?.detail || 'Payment could not be started.');
    } finally {
      setPaying(false);
    }
  };

  if (loading) {
    return (
      <div style={{ maxWidth: 1000, margin: '3rem auto', padding: '0 20px', textAlign: 'center' }}>
        <div style={{ fontSize: '2rem', animation: 'spin 1s linear infinite', display: 'inline-block' }}>⏳</div>
        <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>Loading auction details...</p>
      </div>
    );
  }

  if (!auction) {
    return (
      <div style={{ maxWidth: 600, margin: '4rem auto', textAlign: 'center', padding: '2rem' }}>
        <h2>Auction Not Found</h2>
        <p style={{ color: 'var(--text-muted)', marginTop: '0.5rem' }}>
          This auction may have been removed or does not exist.
        </p>
        <Link to="/" className="btn btn-primary" style={{ display: 'inline-block', marginTop: '1.5rem' }}>
          Return to Marketplace
        </Link>
      </div>
    );
  }

  const { text: timeText, isEnded } = formatTimeLeft(auction.end_time);
  const isSeller = user && (user.id === auction.seller || user.username === auction.seller_name || user.username === auction.seller_username);
  const isWinning = user && (user.username === auction.highest_bidder_name || user.username === auction.highest_bidder_username);

  return (
    <div className="content-shell" style={{ maxWidth: 1100, margin: '1rem auto' }}>
      {/* Breadcrumb */}
      <div style={{ marginBottom: '1.5rem', fontSize: '0.88rem', color: 'var(--text-muted)' }}>
        <Link to="/" style={{ color: 'var(--text-muted)', textDecoration: 'none' }}>Home</Link>
        {' '}/ <span style={{ textTransform: 'capitalize' }}>{auction.category}</span>
        {' '}/ <span style={{ color: 'var(--text-light)' }}>{auction.title}</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(300px, 1.2fr) minmax(320px, 1fr)', gap: '2rem' }}>
        {/* Left Column: Image & Description */}
        <div>
          <div
            style={{
              position: 'relative',
              borderRadius: '20px',
              overflow: 'hidden',
              border: '1px solid var(--border)',
              background: 'var(--bg-card)',
              boxShadow: 'var(--shadow-soft)'
            }}
          >
            {auction.image ? (
              <img
                src={getMediaUrl(auction.image)}
                alt={auction.title}
                style={{ width: '100%', maxHeight: 460, objectFit: 'contain', background: '#070c14' }}
              />
            ) : (
              <div
                style={{
                  height: 380,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '5rem',
                  background: 'linear-gradient(135deg, rgba(255,153,51,0.15), rgba(19,136,8,0.15))'
                }}
              >
                🏷️
              </div>
            )}

            {/* Time overlay badge */}
            <div
              style={{
                position: 'absolute',
                top: 16,
                right: 16,
                background: isEnded ? 'rgba(239, 68, 68, 0.92)' : 'rgba(10, 16, 28, 0.88)',
                backdropFilter: 'blur(10px)',
                padding: '6px 14px',
                borderRadius: '16px',
                color: '#fff',
                fontWeight: 700,
                fontSize: '0.85rem',
                border: '1px solid rgba(255,255,255,0.12)'
              }}
            >
              {isEnded ? '🔴 Bidding Closed' : `⏱️ ${timeText}`}
            </div>
          </div>

          {/* Description Section */}
          <div
            style={{
              marginTop: '1.5rem',
              padding: '1.5rem',
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: '16px'
            }}
          >
            <h3 style={{ fontSize: '1.15rem', marginBottom: '0.8rem', color: '#ffb366' }}>About this item</h3>
            <p style={{ whiteSpace: 'pre-wrap', lineHeight: 1.7, color: 'var(--text-light)', fontSize: '0.95rem' }}>
              {auction.description}
            </p>

            <div style={{ marginTop: '1.5rem', display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', borderTop: '1px solid rgba(255,255,255,0.08)', paddingTop: '1rem' }}>
              <div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Condition</span>
                <p style={{ fontWeight: 600, textTransform: 'capitalize' }}>{auction.condition}</p>
              </div>
              <div>
                <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Listed By</span>
                <p style={{ fontWeight: 600 }}>{auction.seller_name || auction.seller_username}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Bid Control Panel & History */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          {/* Main Bid Action Card */}
          <div
            style={{
              background: 'var(--bg-card-strong)',
              border: '1px solid var(--border)',
              borderRadius: '20px',
              padding: '1.8rem',
              boxShadow: 'var(--shadow-soft)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <span
                style={{
                  background: isEnded ? 'rgba(239,68,68,0.2)' : 'rgba(43,182,115,0.2)',
                  color: isEnded ? '#f87171' : '#34d399',
                  border: isEnded ? '1px solid rgba(239,68,68,0.4)' : '1px solid rgba(43,182,115,0.4)',
                  padding: '4px 12px',
                  borderRadius: '12px',
                  fontSize: '0.8rem',
                  fontWeight: 700
                }}
              >
                {isEnded ? 'Auction Ended' : 'Live Bidding'}
              </span>
              <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                {bids.length} {bids.length === 1 ? 'total bid' : 'total bids'}
              </span>
            </div>

            <h1 style={{ fontSize: '1.65rem', margin: '0.8rem 0 1.2rem', lineHeight: 1.3 }}>{auction.title}</h1>

            {/* Price Snapshot */}
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr',
                gap: '1rem',
                background: 'rgba(255, 255, 255, 0.03)',
                padding: '1rem 1.25rem',
                borderRadius: '14px',
                border: '1px solid rgba(255, 255, 255, 0.06)'
              }}
            >
              <div>
                <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Current Bid
                </label>
                <div style={{ fontSize: '1.65rem', fontWeight: 800, color: '#ffb366' }}>
                  {formatINR(currentHighest > 0 ? currentHighest : basePrice)}
                </div>
                {auction.highest_bidder_name && (
                  <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    by {auction.highest_bidder_name}
                  </span>
                )}
              </div>
              <div>
                <label style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.04em' }}>
                  Base Starting Price
                </label>
                <div style={{ fontSize: '1.3rem', fontWeight: 600, marginTop: '4px' }}>
                  {formatINR(basePrice)}
                </div>
              </div>
            </div>

            {/* Post-Auction State / Winner CTA */}
            {isEnded && (
              <div
                style={{
                  marginTop: '1.5rem',
                  padding: '1.25rem',
                  borderRadius: '14px',
                  background: isWinning ? 'rgba(43, 182, 115, 0.15)' : 'rgba(239, 68, 68, 0.12)',
                  border: isWinning ? '1px solid rgba(43, 182, 115, 0.4)' : '1px solid rgba(239, 68, 68, 0.3)'
                }}
              >
                {isWinning ? (
                  <div>
                    <h4 style={{ color: '#34d399', marginBottom: '0.4rem' }}>🏆 Congratulations! You Won this Auction!</h4>
                    <p style={{ fontSize: '0.88rem', color: 'var(--text-light)', marginBottom: '1rem' }}>
                      You are the highest bidder at {formatINR(currentHighest)}. Proceed to checkout to complete your acquisition.
                    </p>
                    <button
                      onClick={handlePayNow}
                      disabled={paying}
                      className="btn btn-primary btn-block"
                      style={{ background: 'linear-gradient(135deg, #138808 0%, #2bb673 100%)' }}
                    >
                      {paying ? 'Processing Payment...' : `Pay ${formatINR(currentHighest)} Now`}
                    </button>
                  </div>
                ) : (
                  <div>
                    <h4 style={{ color: '#f87171', marginBottom: '0.3rem' }}>Auction Has Closed</h4>
                    <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
                      Winning bidder: <strong>{auction.highest_bidder_name || 'None'}</strong> at {formatINR(currentHighest)}.
                    </p>
                  </div>
                )}
              </div>
            )}

            {/* Bid Form Component */}
            {!isEnded && (
              <form onSubmit={handleBidSubmit} style={{ marginTop: '1.5rem' }}>
                {isSeller ? (
                  <div style={{ padding: '1rem', background: 'rgba(255, 153, 51, 0.1)', borderRadius: '10px', color: '#ffb366', fontSize: '0.88rem' }}>
                    ℹ️ You are the seller of this auction. Self-bidding is disabled.
                  </div>
                ) : (
                  <>
                    <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, marginBottom: '6px' }}>
                      Enter your bid (minimum {formatINR(minNextBid)})
                    </label>

                    <div style={{ display: 'flex', gap: '8px' }}>
                      <span
                        style={{
                          display: 'flex',
                          alignItems: 'center',
                          padding: '0 14px',
                          background: 'rgba(255, 255, 255, 0.08)',
                          borderRadius: '10px',
                          fontWeight: 700,
                          fontSize: '1rem'
                        }}
                      >
                        ₹
                      </span>
                      <input
                        type="number"
                        step="0.01"
                        min={minNextBid}
                        value={bidAmount}
                        onChange={(e) => setBidAmount(e.target.value)}
                        placeholder={`Min ${minNextBid}`}
                        className="form-control"
                        style={{ fontSize: '1.1rem', fontWeight: 700 }}
                        required
                      />
                    </div>

                    {/* Quick increment pills */}
                    <div style={{ display: 'flex', gap: '6px', marginTop: '10px' }}>
                      {[50, 100, 500, 1000].map((inc) => (
                        <button
                          key={inc}
                          type="button"
                          onClick={() => handleQuickIncrement(inc)}
                          style={{
                            flex: 1,
                            padding: '6px 0',
                            borderRadius: '8px',
                            background: 'rgba(255, 255, 255, 0.06)',
                            border: '1px solid rgba(255, 255, 255, 0.12)',
                            color: 'var(--text-light)',
                            fontSize: '0.78rem',
                            fontWeight: 600,
                            cursor: 'pointer'
                          }}
                        >
                          +{inc}
                        </button>
                      ))}
                    </div>

                    <button
                      type="submit"
                      disabled={submitting}
                      className="btn btn-primary btn-block"
                      style={{ marginTop: '1.25rem', padding: '12px', fontSize: '1rem', fontWeight: 700 }}
                    >
                      {submitting ? 'Placing Bid...' : 'Place Bid Now'}
                    </button>
                  </>
                )}
              </form>
            )}
          </div>

          {/* Bid History Table */}
          <div
            style={{
              background: 'var(--bg-card)',
              border: '1px solid var(--border)',
              borderRadius: '20px',
              padding: '1.5rem',
              boxShadow: 'var(--shadow-soft)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1.1rem' }}>Bid History</h3>
              <button
                type="button"
                onClick={() => loadData(false)}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: 'var(--primary)',
                  fontSize: '0.8rem',
                  cursor: 'pointer'
                }}
              >
                🔄 Refresh
              </button>
            </div>

            {bids.length === 0 ? (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', textAlign: 'center', padding: '1.5rem 0' }}>
                No bids placed yet. Be the first to start the auction!
              </p>
            ) : (
              <div style={{ maxHeight: 300, overflowY: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.88rem' }}>
                  <thead>
                    <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', color: 'var(--text-muted)', textAlign: 'left' }}>
                      <th style={{ padding: '8px 4px' }}>Bidder</th>
                      <th style={{ padding: '8px 4px' }}>Amount</th>
                      <th style={{ padding: '8px 4px', textAlign: 'right' }}>Time</th>
                    </tr>
                  </thead>
                  <tbody>
                    {bids.map((bid, index) => (
                      <tr
                        key={`${bid.bidder_name || bid.bidder}-${index}`}
                        style={{
                          borderBottom: '1px solid rgba(255,255,255,0.04)',
                          background: index === 0 ? 'rgba(255, 153, 51, 0.05)' : 'transparent'
                        }}
                      >
                        <td style={{ padding: '10px 4px', fontWeight: index === 0 ? 700 : 400 }}>
                          {index === 0 && <span style={{ marginRight: 6 }}>👑</span>}
                          {bid.bidder_name || bid.bidder}
                        </td>
                        <td style={{ padding: '10px 4px', color: '#ffb366', fontWeight: 700 }}>
                          {formatINR(bid.amount)}
                        </td>
                        <td style={{ padding: '10px 4px', textAlign: 'right', color: 'var(--text-muted)', fontSize: '0.78rem' }}>
                          {bid.timestamp ? new Date(bid.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Recent'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default AuctionDetail;
