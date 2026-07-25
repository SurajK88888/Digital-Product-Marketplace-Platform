import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from "axios";
import { useAuthStore } from "@/store/auth.store";

// ── Constants ─────────────────────────────────────────────────
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000/api/v1";

const REQUEST_TIMEOUT_MS = 15_000; // 15 seconds

// ── API Error Shape (mirrors backend RFC 7807 format) ─────────
export interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Array<{ field: string; reason: string }>;
    traceId?: string;
  };
  meta: {
    timestamp: string;
    path: string;
    method: string;
  };
}

// ── Standard API Success Response Shape ────────────────────────
export interface ApiResponse<T = unknown> {
  success: true;
  data: T;
  meta: {
    timestamp: string;
    version: string;
    requestId: string;
    pagination?: {
      limit: number;
      hasNextPage: boolean;
      nextCursor?: string;
      totalCount?: number;
    };
  };
}

/**
 * Axios HTTP Client — Centralized API Instance
 * ==============================================
 * Reusable pattern: This client can be imported anywhere in the app.
 * All request and response transformations happen here — not in individual hooks.
 *
 * Features:
 * - Automatic JWT Bearer token injection
 * - 401 → automatic token refresh & request retry
 * - Standardized error normalization
 * - Correlation ID header injection
 */
const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: REQUEST_TIMEOUT_MS,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
  withCredentials: true, // Required for HttpOnly refresh token cookie
});

// ── Request Interceptor: Inject Access Token ──────────────────
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const accessToken = useAuthStore.getState().accessToken;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }

    // Inject a client-generated correlation ID for distributed tracing
    config.headers["X-Request-Id"] = crypto.randomUUID();

    return config;
  },
  (error: AxiosError) => Promise.reject(error),
);

// ── Response Interceptor: Handle 401 & Token Refresh ──────────
let isRefreshing = false;
let refreshFailedCallbacks: Array<(error: AxiosError) => void> = [];

apiClient.interceptors.response.use(
  (response: AxiosResponse) => response,
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & {
      _retry?: boolean;
    };

    // If 401 and not already retried, attempt token refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        // Queue additional requests that arrive during refresh
        return new Promise((_, reject) => {
          refreshFailedCallbacks.push(reject);
        });
      }

      originalRequest._retry = true;
      isRefreshing = true;

      try {
        // Refresh token is in HttpOnly cookie — POST to refresh endpoint
        const refreshResponse = await axios.post<{ data: { accessToken: string } }>(
          `${API_BASE_URL}/auth/refresh`,
          {},
          { withCredentials: true },
        );

        const newAccessToken = refreshResponse.data.data.accessToken;
        useAuthStore.getState().setAccessToken(newAccessToken);

        // Flush queued failed callbacks
        refreshFailedCallbacks = [];

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
        return apiClient(originalRequest);
      } catch (refreshError) {
        // Refresh failed — log out user and redirect to login
        refreshFailedCallbacks.forEach((cb) => cb(error));
        refreshFailedCallbacks = [];
        useAuthStore.getState().clearAuth();

        if (typeof window !== "undefined") {
          window.location.href = "/login?reason=session_expired";
        }

        return Promise.reject(refreshError);
      } finally {
        isRefreshing = false;
      }
    }

    return Promise.reject(error);
  },
);

export { apiClient };
