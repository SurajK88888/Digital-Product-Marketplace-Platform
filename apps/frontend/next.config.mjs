/** @type {import('next').NextConfig} */
const nextConfig = {
  // ── Output ──────────────────────────────────────────────────
  // Standalone mode reduces Docker image size by ~80%
  output: "standalone",

  // ── React Strict Mode ───────────────────────────────────────
  reactStrictMode: true,

  // ── TypeScript ──────────────────────────────────────────────
  typescript: {
    // Type errors will fail the production build — enforced in CI
    ignoreBuildErrors: false,
  },

  // ── ESLint ──────────────────────────────────────────────────
  eslint: {
    ignoreDuringBuilds: false,
  },

  // ── Images ──────────────────────────────────────────────────
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "**.amazonaws.com",
      },
      {
        protocol: "https",
        hostname: "**.cloudflare.com",
      },
      {
        protocol: "https",
        hostname: "avatars.githubusercontent.com",
      },
      {
        protocol: "https",
        hostname: "lh3.googleusercontent.com",
      },
    ],
    formats: ["image/avif", "image/webp"],
  },

  // ── Experimental Features ───────────────────────────────────
  experimental: {
    // Server Actions are stable in Next.js 15
    serverActions: {
      bodySizeLimit: "10mb",
    },
  },

  // ── Environment Variables (public) ──────────────────────────
  // All NEXT_PUBLIC_* vars are automatically exposed to the browser.
  // Non-public vars are server-only and never sent to the client.

  // ── Headers for Security ────────────────────────────────────
  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "X-XSS-Protection", value: "1; mode=block" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          {
            key: "Permissions-Policy",
            value: "camera=(), microphone=(), geolocation=()",
          },
        ],
      },
    ];
  },

  // ── Webpack Aliases (mirrors tsconfig paths) ─────────────────
  // Path aliases are handled natively via tsconfig paths + Next.js
};

export default nextConfig;
