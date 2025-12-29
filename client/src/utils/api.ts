import axios from "axios";
import type { AxiosInstance, InternalAxiosRequestConfig } from "axios";

const api: AxiosInstance = axios.create({
	baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

api.interceptors.request.use(
	(config: InternalAxiosRequestConfig) => {
		const token = localStorage.getItem("access_token");
		if (token && config.headers) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		if (
			!config.headers["Content-Type"] &&
			typeof config.data === "object" &&
			!(config.data instanceof URLSearchParams) &&
			!(config.data instanceof FormData)
		) {
			config.headers["Content-Type"] = "application/json";
		}
		return config;
	},
	(error) => {
		return Promise.reject(error);
	}
);

api.interceptors.response.use(
	(response) => response,
	(error) => {
		if (error.response?.status === 401) {
			localStorage.removeItem("access_token");
			localStorage.removeItem("user");
			window.location.href = "/login";
		}
		return Promise.reject(error);
	}
);

export default api;
