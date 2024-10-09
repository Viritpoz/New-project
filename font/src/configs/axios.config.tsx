import axios from 'axios';
export const API_BASE_URL = import.meta.env.VITE_API ?  `http://${import.meta.env.VITE_API}` : "http://localhost:8000"; 
export const WS_BASE_URL = import.meta.env.VITE_API ? `ws://${import.meta.env.VITE_API}/ws` : "ws://localhost:8000/ws";

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
});

export default axiosInstance;