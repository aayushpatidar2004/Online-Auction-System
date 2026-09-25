import { createSlice } from '@reduxjs/toolkit';

const tokenFromStorage = localStorage.getItem('access_token');
const userFromStorage = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null;

const authSlice = createSlice({
  name: 'auth',
  initialState: {
    token: tokenFromStorage || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    user: userFromStorage,
    isAuthenticated: !!tokenFromStorage,
  },
  reducers: {
    setCredentials: (state, action) => {
      const { access, refresh, user } = action.payload;
      state.token = access;
      state.refreshToken = refresh;
      state.user = user;
      state.isAuthenticated = true;
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);
      if (user) localStorage.setItem('user', JSON.stringify(user));
    },
    logout: (state) => {
      state.token = null;
      state.refreshToken = null;
      state.user = null;
      state.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    },
  },
});

export const { setCredentials, logout } = authSlice.actions;
export default authSlice.reducer;
