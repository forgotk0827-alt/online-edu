import axios from "axios";
import { getAuthToken } from "./auth";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000/api"
});

api.interceptors.request.use((config) => {
  const token = getAuthToken();
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

export async function requestOrMock(request, fallback) {
  try {
    const { data } = await request();
    return data.data;
  } catch {
    return fallback;
  }
}
