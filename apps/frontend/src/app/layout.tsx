import type { Metadata, Viewport } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";

import "./globals.css";
import { Providers } from "@/components/providers";

// ── Font Configuration ───────────────────────────────────────
const fontSans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

const fontMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-mono",
  display: "swap",
});

// ── Metadata ─────────────────────────────────────────────────
export const metadata: Metadata = {
  metadataBase: new URL(
    process.env.NEXT_PUBLIC_APP_URL ?? "http://localhost:3000"
  ),
  title: {
    default: "Digital Product Marketplace",
    template: "%s | Digital Product Marketplace",
  },
  description:
    "The enterprise marketplace for premium digital products — themes, plugins, scripts, e-books, and more.",
  keywords: [
    "digital products",
    "marketplace",
    "themes",
    "plugins",
    "scripts",
    "templates",
    "downloads",
  ],
  authors: [{ name: "Digital Product Marketplace" }],
  creator: "Digital Product Marketplace",
  robots: {
    index: true,
    follow: true,
    googleBot: { index: true, follow: true },
  },
  openGraph: {
    type: "website",
    locale: "en_US",
    url: process.env.NEXT_PUBLIC_APP_URL,
    siteName: "Digital Product Marketplace",
    title: "Digital Product Marketplace",
    description:
      "The enterprise marketplace for premium digital products.",
  },
  twitter: {
    card: "summary_large_image",
    title: "Digital Product Marketplace",
    description: "The enterprise marketplace for premium digital products.",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#0a0a0f" },
  ],
};

// ── Root Layout ───────────────────────────────────────────────
export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className={`${fontSans.variable} ${fontMono.variable}`}
    >
      <body className="min-h-screen bg-background font-sans antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
