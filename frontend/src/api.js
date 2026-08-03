import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
});

export const registerUser = (data) => api.post("/auth/register", data);
export const loginUser = (email, password) =>
  api.post(`/auth/login?email=${email}&password=${password}`);
export const getOpenAvailability = () => api.get("/nurses/availability/open");
export const verifyNurse = (nurseId) => api.get(`/nurses/${nurseId}/verification`);
export const createBooking = (data) => api.post("/bookings/", data);
export const createPayment = (data) => api.post("/payments/", data);

export default api;
