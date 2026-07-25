"use client";

import { QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { ThemeProvider } from "next-themes";
import type { ReactNode } from "react";

import { queryClient } from "@/lib/query-client";

/**
 * Providers — Global Provider Wrapper
 * =====================================
 * Wraps the entire application with all necessary context providers.
 * Rendered inside RootLayout (Server Component) as a Client Component boundary.
 *
 * Reusable pattern: Add new providers here (e.g., AuthProvider, SocketProvider)
 * to make them available throughout the entire component tree.
 */
interface ProvidersProps {
  children: ReactNode;
}

export function Providers({ children }: ProvidersProps) {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <QueryClientProvider client={queryClient}>
        {children}
        {/* React Query Devtools — only visible in development */}
        {process.env.NODE_ENV === "development" && (
          <ReactQueryDevtools initialIsOpen={false} position="bottom" />
        )}
      </QueryClientProvider>
    </ThemeProvider>
  );
}
