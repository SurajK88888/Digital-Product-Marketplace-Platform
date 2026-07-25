import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

// ── Auth User Type ────────────────────────────────────────────
export interface AuthUser {
  id: string;
  email: string;
  role: "SUPERADMIN" | "VENDOR" | "CUSTOMER";
  displayName: string | null;
  avatarUrl: string | null;
  emailVerified: boolean;
  mfaEnabled: boolean;
}

// ── Auth Store State & Actions ────────────────────────────────
interface AuthState {
  // State
  user: AuthUser | null;
  accessToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setAuth: (user: AuthUser, accessToken: string) => void;
  setAccessToken: (accessToken: string) => void;
  setUser: (user: AuthUser) => void;
  clearAuth: () => void;
  setLoading: (loading: boolean) => void;
}

/**
 * Auth Store — Zustand Global State
 * ===================================
 * Manages authentication state across the entire frontend.
 * Uses `persist` middleware to preserve the user object in sessionStorage
 * (NOT localStorage) to clear on tab close for security.
 * Access tokens are NOT persisted — they are only held in memory.
 *
 * Reusable pattern: Copy this pattern for any authenticated app.
 */
export const useAuthStore = create<AuthState>()(
  devtools(
    persist(
      (set) => ({
        // ── Initial State ──────────────────────────────────────
        user: null,
        accessToken: null,
        isAuthenticated: false,
        isLoading: false,

        // ── Actions ────────────────────────────────────────────
        setAuth: (user: AuthUser, accessToken: string) =>
          set(
            { user, accessToken, isAuthenticated: true, isLoading: false },
            false,
            "auth/setAuth",
          ),

        setAccessToken: (accessToken: string) => set({ accessToken }, false, "auth/setAccessToken"),

        setUser: (user: AuthUser) => set({ user }, false, "auth/setUser"),

        clearAuth: () =>
          set({ user: null, accessToken: null, isAuthenticated: false }, false, "auth/clearAuth"),

        setLoading: (isLoading: boolean) => set({ isLoading }, false, "auth/setLoading"),
      }),
      {
        name: "auth-storage",
        // Use sessionStorage — clears when tab/browser closes (security)
        storage: {
          getItem: (name) => {
            if (typeof window === "undefined") return null;
            const value = sessionStorage.getItem(name);
            return value ? (JSON.parse(value) as { state: AuthState }) : null;
          },
          setItem: (name, value) => {
            if (typeof window === "undefined") return;
            // SECURITY: Never persist the accessToken — memory only
            const stateToStore = {
              ...value,
              state: { ...value.state, accessToken: null },
            };
            sessionStorage.setItem(name, JSON.stringify(stateToStore));
          },
          removeItem: (name) => {
            if (typeof window === "undefined") return;
            sessionStorage.removeItem(name);
          },
        },
      },
    ),
    { name: "AuthStore" },
  ),
);
