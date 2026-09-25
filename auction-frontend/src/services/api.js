import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
});

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Auto-refresh on 401
api.interceptors.response.use(
  (res) => res,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem('refresh_token');
      if (refresh) {
        try {
          const { data } = await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh });
          localStorage.setItem('access_token', data.access);
          original.headers.Authorization = `Bearer ${data.access}`;
          return api(original);
        } catch (_) {
          localStorage.clear();
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

// Auth
export const register = (data) => api.post('/users/register/', data);
export const login = (data) => api.post('/token/', data);
export const refreshToken = (refresh) => api.post('/token/refresh/', { refresh });
export const getProfile = () => api.get('/users/profile/');
export const updateProfile = (data) => api.patch('/users/profile/', data);

// Auctions
export const getAuctions = (params = {}) => api.get('/auctions/', { params });
export const getAuctionDetail = (id) => api.get(`/auctions/${id}/`);
export const createAuction = (data) =>
  api.post('/auctions/', data, { headers: { 'Content-Type': 'multipart/form-data' } });
export const updateAuction = (id, data) => api.patch(`/auctions/${id}/`, data);
export const deleteAuction = (id) => api.delete(`/auctions/${id}/`);
export const getMyAuctions = () => api.get('/auctions/my_auctions/');
export const getMyBids = () => api.get('/auctions/my_bids/');

// Bids
export const placeBid = (auctionId, bidAmount, autoBidLimit = null) =>
  api.post(`/auctions/${auctionId}/place_bid/`, {
    bid_amount: bidAmount,
    ...(autoBidLimit ? { auto_bid_limit: autoBidLimit } : {}),
  });
export const getBidHistory = (auctionId) => api.get(`/auctions/${auctionId}/bid_history/`);

// Payments
export const initiatePayment = (auctionId) =>
  api.post('/payments/initiate/', { auction_id: auctionId });
export const getMyPayments = () => api.get('/payments/');

export default api;
