import React, { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';
import { createAuction } from '../services/api';

function CreateAuction() {
  const navigate = useNavigate();
  const now = useMemo(() => new Date(), []);
  const defaultStart = new Date(now.getTime() - 60 * 60 * 1000).toISOString().slice(0, 16);
  const defaultEnd = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000).toISOString().slice(0, 16);

  const [form, setForm] = useState({
    title: '',
    description: '',
    category: 'general',
    condition: 'used',
    base_price: '500',
    start_time: defaultStart,
    end_time: defaultEnd,
    image: null,
  });
  const [imagePreview, setImagePreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, files } = e.target;
    if (name === 'image') {
      const file = files[0] || null;
      setForm({ ...form, image: file });
      if (file) {
        setImagePreview(URL.createObjectURL(file));
      } else {
        setImagePreview(null);
      }
      return;
    }
    setForm({ ...form, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const basePrice = Number(form.base_price);
    const start = new Date(form.start_time);
    const end = new Date(form.end_time);

    if (!form.title.trim() || !form.description.trim()) {
      toast.error('Please enter a title and description.');
      return;
    }

    if (Number.isNaN(basePrice) || basePrice <= 0) {
      toast.error('Base price must be greater than zero.');
      return;
    }

    if (form.start_time && form.end_time && end <= start) {
      toast.error('Auction end time must be after the start time.');
      return;
    }

    setLoading(true);
    try {
      const payload = new FormData();
      Object.entries(form).forEach(([key, value]) => {
        if (value !== '' && value !== null) payload.append(key, value);
      });

      const { data } = await createAuction(payload);
      toast.success('🎉 Auction created successfully!');
      navigate(`/auction/${data.id}`);
    } catch (error) {
      const message =
        error?.response?.data?.detail ||
        error?.response?.data?.non_field_errors?.[0] ||
        'Could not create auction. Please check your inputs.';
      toast.error(message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="content-shell" style={{ maxWidth: 840, margin: '1rem auto' }}>
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
        <div style={{ marginBottom: '2rem' }}>
          <p className="eyebrow">Seller Hub</p>
          <h1 style={{ fontSize: '1.8rem', marginTop: '4px' }}>Create a New Auction</h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.92rem' }}>
            List your item to verified buyers across the marketplace.
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
          <div className="form-group">
            <label htmlFor="title" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
              Auction Title *
            </label>
            <input
              id="title"
              className="form-control"
              name="title"
              placeholder="e.g., Rare 1970 Vintage Chronograph Watch"
              value={form.title}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="description" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
              Detailed Description *
            </label>
            <textarea
              id="description"
              className="form-control"
              name="description"
              placeholder="Describe provenance, specifications, imperfections, and authenticity..."
              value={form.description}
              onChange={handleChange}
              rows={4}
              required
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
            <div className="form-group">
              <label htmlFor="category" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                Category
              </label>
              <select id="category" className="form-control" name="category" value={form.category} onChange={handleChange}>
                <option value="electronics">Electronics & Gadgets</option>
                <option value="fashion">Fashion & Apparel</option>
                <option value="home">Home & Living</option>
                <option value="vehicles">Vehicles & Automobilia</option>
                <option value="art">Art & Collectibles</option>
                <option value="general">General Marketplace</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="condition" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                Condition
              </label>
              <select id="condition" className="form-control" name="condition" value={form.condition} onChange={handleChange}>
                <option value="new">Brand New (Unused)</option>
                <option value="used">Used / Pre-owned</option>
                <option value="refurbished">Refurbished / Restored</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
            <div className="form-group">
              <label htmlFor="base_price" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                Base Starting Price (₹) *
              </label>
              <input
                id="base_price"
                className="form-control"
                type="number"
                min="1"
                step="0.01"
                placeholder="500.00"
                name="base_price"
                value={form.base_price}
                onChange={handleChange}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="image" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                Item Image
              </label>
              <input
                id="image"
                className="form-control"
                type="file"
                accept="image/*"
                name="image"
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Image Preview if selected */}
          {imagePreview && (
            <div style={{ marginTop: '0.5rem', textAlign: 'center' }}>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '6px' }}>Selected Image Preview:</p>
              <img
                src={imagePreview}
                alt="Preview"
                style={{ maxHeight: 200, margin: '0 auto', borderRadius: 12, border: '1px solid var(--border)' }}
              />
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem' }}>
            <div className="form-group">
              <label htmlFor="start_time" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                Start Time
              </label>
              <input
                id="start_time"
                className="form-control"
                type="datetime-local"
                name="start_time"
                value={form.start_time}
                onChange={handleChange}
              />
            </div>

            <div className="form-group">
              <label htmlFor="end_time" style={{ display: 'block', fontWeight: 600, marginBottom: '6px' }}>
                End Time *
              </label>
              <input
                id="end_time"
                className="form-control"
                type="datetime-local"
                name="end_time"
                value={form.end_time}
                onChange={handleChange}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="btn btn-primary btn-block"
            disabled={loading}
            style={{
              marginTop: '1.5rem',
              padding: '14px',
              fontSize: '1.05rem',
              fontWeight: 700,
              borderRadius: '12px'
            }}
          >
            {loading ? 'Publishing Auction...' : '🚀 Publish Auction Listing'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default CreateAuction;
