import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Set up axios defaults
axios.defaults.headers.common['Content-Type'] = 'application/json';

// Add request interceptor to add token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Upload APIs
export const uploadAPI = {
  uploadImage: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post(`${API}/upload/image`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  },
  
  uploadMultipleImages: async (files) => {
    const formData = new FormData();
    files.forEach(file => {
      formData.append('files', file);
    });
    
    const response = await axios.post(`${API}/upload/images/bulk`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
    return response.data;
  }
};

// Product APIs
export const productAPI = {
  getAll: async (params = {}) => {
    const response = await axios.get(`${API}/products`, { params });
    return response.data;
  },
  getById: async (id) => {
    const response = await axios.get(`${API}/products/${id}`);
    return response.data;
  },
  search: async (query) => {
    const response = await axios.get(`${API}/products`, { params: { search: query } });
    return response.data;
  },
  getByCategory: async (category) => {
    const response = await axios.get(`${API}/products`, { params: { category } });
    return response.data;
  },
  create: async (productData) => {
    const response = await axios.post(`${API}/products`, productData);
    return response.data;
  },
  update: async (id, productData) => {
    const response = await axios.put(`${API}/products/${id}`, productData);
    return response.data;
  },
  delete: async (id) => {
    const response = await axios.delete(`${API}/products/${id}`);
    return response.data;
  }
};

// Category APIs
export const categoryAPI = {
  getAll: async () => {
    const response = await axios.get(`${API}/categories`);
    return response.data;
  },
  create: async (categoryData) => {
    const response = await axios.post(`${API}/categories`, categoryData);
    return response.data;
  }
};

// Order APIs
export const orderAPI = {
  create: async (orderData, isGuest = false) => {
    const endpoint = isGuest ? `${API}/orders/guest` : `${API}/orders`;
    const response = await axios.post(endpoint, orderData);
    return response.data;
  },
  getAll: async () => {
    const response = await axios.get(`${API}/orders`);
    return response.data;
  },
  getById: async (id) => {
    const response = await axios.get(`${API}/orders/${id}`);
    return response.data;
  },
  updateTracking: async (id, trackingData) => {
    const response = await axios.post(`${API}/orders/${id}/track`, trackingData);
    return response.data;
  }
};

// Payment APIs
export const paymentAPI = {
  getMethods: async () => {
    const response = await axios.get(`${API}/payments/methods`);
    return response.data;
  },
  initiateUPI: async (paymentData) => {
    const response = await axios.post(`${API}/payments/upi/initiate`, paymentData);
    return response.data;
  },
  verifyPayment: async (verificationData) => {
    const response = await axios.post(`${API}/payments/verify`, verificationData);
    return response.data;
  }
};

// Coupon APIs
export const couponAPI = {
  getActive: async () => {
    const response = await axios.get(`${API}/coupons`);
    return response.data;
  },
  validate: async (couponData) => {
    const response = await axios.post(`${API}/coupons/validate`, couponData);
    return response.data;
  },
  getByCode: async (code) => {
    const response = await axios.get(`${API}/coupons/${code}`);
    return response.data;
  }
};

// Seller APIs
export const sellerAPI = {
  getProfile: async (sellerId) => {
    const response = await axios.get(`${API}/sellers/profile/${sellerId}`);
    return response.data;
  },
  getMyProfile: async () => {
    const response = await axios.get(`${API}/sellers/my-profile`);
    return response.data;
  },
  createProfile: async (profileData) => {
    const response = await axios.post(`${API}/sellers/profile`, profileData);
    return response.data;
  },
  updateProfile: async (sellerId, profileData) => {
    const response = await axios.put(`${API}/sellers/profile/${sellerId}`, profileData);
    return response.data;
  },
  getReviews: async (sellerId) => {
    const response = await axios.get(`${API}/sellers/reviews/${sellerId}`);
    return response.data;
  },
  createReview: async (reviewData) => {
    const response = await axios.post(`${API}/sellers/reviews`, reviewData);
    return response.data;
  },
  getAll: async (params = {}) => {
    const response = await axios.get(`${API}/sellers`, { params });
    return response.data;
  }
};

// Auth APIs (already in AuthContext, but exporting for reference)
export const authAPI = {
  register: async (userData) => {
    const response = await axios.post(`${API}/auth/register`, userData);
    return response.data;
  },
  login: async (credentials) => {
    const response = await axios.post(`${API}/auth/login`, credentials);
    return response.data;
  },
  getMe: async () => {
    const response = await axios.get(`${API}/auth/me`);
    return response.data;
  }
};

export default {
  product: productAPI,
  category: categoryAPI,
  order: orderAPI,
  payment: paymentAPI,
  coupon: couponAPI,
  seller: sellerAPI,
  auth: authAPI
};