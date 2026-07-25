"use client";

import { useRouter } from "next/navigation";
import { useCallback } from "react";
import { apiClient } from "@/lib/api-client";
import { useAuthStore } from "@/store/auth.store";
import type { AuthTokenResponse, LoginCredentials, RegisterCredentials, User } from "@/types";

/**
 * useAuth — Authentication Hook
 * ================================
 * Provides auth state and actions to any component.
 * Abstracts away Zustand store and API calls.
 *
 * Reusable pattern: Extend this hook with new auth actions (e.g., updateProfile, enable2FA).
 */
export function useAuth() {
  const router = useRouter();
  const { user, accessToken, isAuthenticated, isLoading, setAuth, clearAuth, setLoading } =
    useAuthStore();

  // ── Login ──────────────────────────────────────────────────
  const login = useCallback(
    async (credentials: LoginCredentials): Promise<void> => {
      setLoading(true);
      try {
        const response = await apiClient.post<{ data: AuthTokenResponse }>(
          "/auth/login",
          credentials,
        );
        const { accessToken: token, user: userData } = response.data.data;
        setAuth(userData, token);
        router.push("/dashboard");
      } finally {
        setLoading(false);
      }
    },
    [setAuth, setLoading, router],
  );

  // ── Register ───────────────────────────────────────────────
  const register = useCallback(
    async (credentials: RegisterCredentials): Promise<void> => {
      setLoading(true);
      try {
        await apiClient.post("/auth/register", credentials);
        // Redirect to login after successful registration
        router.push("/login?registered=true");
      } finally {
        setLoading(false);
      }
    },
    [setLoading, router],
  );

  // ── Logout ─────────────────────────────────────────────────
  const logout = useCallback(async (): Promise<void> => {
    try {
      await apiClient.post("/auth/logout");
    } finally {
      // Always clear local auth state even if API call fails
      clearAuth();
      router.push("/login");
    }
  }, [clearAuth, router]);

  // ── Get Current User Profile ───────────────────────────────
  const getProfile = useCallback(async (): Promise<User> => {
    const response = await apiClient.get<{ data: User }>("/users/me");
    return response.data.data;
  }, []);

  return {
    // State
    user,
    accessToken,
    isAuthenticated,
    isLoading,

    // Derived
    isVendor: user?.role === "VENDOR" || user?.role === "SUPERADMIN",
    isAdmin: user?.role === "SUPERADMIN",

    // Actions
    login,
    register,
    logout,
    getProfile,
  };
}
