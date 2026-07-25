import { QueryClient } from "@tanstack/react-query";

/**
 * TanStack Query Client — Global Configuration
 * ==============================================
 * Centralized query client with production-ready defaults.
 * Reusable pattern: Copy these defaults to any new project.
 *
 * Design Decisions:
 * - staleTime: 60s — prevents redundant refetches for rapidly-navigated pages
 * - retry: 1 — avoids hammering a slow API on network hiccups
 * - refetchOnWindowFocus: false in production — prevents jarring refetches
 */
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      // Data is considered fresh for 60 seconds
      staleTime: 60 * 1000,
      // Keep unused cache for 5 minutes before garbage collection
      gcTime: 5 * 60 * 1000,
      // Retry once on failure (avoids hammering endpoints during outages)
      retry: 1,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      // Do not refetch on window focus (prevents UI thrashing in production)
      refetchOnWindowFocus: process.env.NODE_ENV === "development",
      // Refetch when reconnecting to the internet
      refetchOnReconnect: true,
    },
    mutations: {
      // Retry mutations once on failure
      retry: 0,
    },
  },
});
