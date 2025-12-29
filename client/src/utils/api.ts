import axios from "axios";
import type { AxiosInstance, InternalAxiosRequestConfig, AxiosError } from "axios";
import { authApi } from "@/api/auth";

const api: AxiosInstance = axios.create({
	baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

let isRefreshing = false;
let failedQueue: Array<{
	resolve: (value?: any) => void;
	reject: (error?: any) => void;
}> = [];

const processQueue = (error: any, token: string | null = null) => {
	failedQueue.forEach((prom) => {
		if (error) {
			prom.reject(error);
		} else {
			prom.resolve(token);
		}
	});
	failedQueue = [];
};

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
	async (error: AxiosError) => {
		const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

		if (error.response?.status === 401 && !originalRequest._retry) {
			if (isRefreshing) {
				return new Promise((resolve, reject) => {
					failedQueue.push({ resolve, reject });
				})
					.then((token) => {
						if (originalRequest.headers) {
							originalRequest.headers.Authorization = `Bearer ${token}`;
						}
						return api(originalRequest);
					})
					.catch((err) => {
						return Promise.reject(err);
					});
			}

			originalRequest._retry = true;
			isRefreshing = true;

			const refreshToken = localStorage.getItem("refresh_token");

			if (!refreshToken) {
				processQueue(error, null);
				localStorage.removeItem("access_token");
				localStorage.removeItem("refresh_token");
				localStorage.removeItem("user");
				window.location.href = "/login";
				return Promise.reject(error);
			}

			try {
				const { access_token, refresh_token } = await authApi.refresh(refreshToken);
				localStorage.setItem("access_token", access_token);
				localStorage.setItem("refresh_token", refresh_token);

				if (originalRequest.headers) {
					originalRequest.headers.Authorization = `Bearer ${access_token}`;
				}

				processQueue(null, access_token);
				return api(originalRequest);
			} catch (refreshError) {
				processQueue(refreshError, null);
				localStorage.removeItem("access_token");
				localStorage.removeItem("refresh_token");
				localStorage.removeItem("user");
				window.location.href = "/login";
				return Promise.reject(refreshError);
			} finally {
				isRefreshing = false;
			}
		}

		return Promise.reject(error);
	}
);

export default api;
