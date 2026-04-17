import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
});

/** GET /orders with optional filters */
export const fetchOrders = async ({ status, dateFrom, dateTo } = {}) => {
  const params = {};
  if (status) params.status = status;
  if (dateFrom) params.dateFrom = dateFrom;
  if (dateTo) params.dateTo = dateTo;
  const { data } = await api.get('/orders', { params });
  return data;
};

/** GET /orders/:id */
export const fetchOrder = async (id) => {
  const { data } = await api.get(`/orders/${id}`);
  return data;
};

/** POST /orders */
export const createOrder = async (order) => {
  const { data } = await api.post('/orders', order);
  return data;
};

/** PATCH /orders/:id/status */
export const updateOrderStatus = async ({ id, status }) => {
  const { data } = await api.patch(`/orders/${id}/status`, { status });
  return data;
};

export default api;
