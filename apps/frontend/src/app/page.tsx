import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Home",
  description:
    "Discover and download premium digital products — themes, plugins, scripts, templates, and more.",
};

/**
 * Root page — Phase 1 placeholder.
 * Business features (product catalog, hero section, etc.) are implemented in Phase 2+.
 * This page confirms the Next.js app router is wired correctly.
 */
export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8">
      <div className="flex max-w-2xl flex-col items-center gap-6 text-center">
        {/* Status badge */}
        <span className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary">
          <span className="relative flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
            <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
          </span>
          Phase 1 — Foundation Complete
        </span>

        <h1 className="text-5xl font-bold tracking-tight text-foreground">
          Digital Product{" "}
          <span className="bg-gradient-to-r from-primary to-brand-700 bg-clip-text text-transparent">
            Marketplace
          </span>
        </h1>

        <p className="text-lg text-muted-foreground">
          Enterprise-grade digital product marketplace platform. The boilerplate
          is fully initialized with Next.js 15, TypeScript, Tailwind CSS, Shadcn
          UI, TanStack Query, Zustand, and Framer Motion.
        </p>

        <div className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-3">
          {[
            "Next.js 15",
            "TypeScript",
            "Tailwind CSS",
            "Shadcn UI",
            "TanStack Query",
            "Zustand",
            "Framer Motion",
            "FastAPI Backend",
            "Docker Ready",
          ].map((tech) => (
            <span
              key={tech}
              className="rounded-md border border-border bg-card px-3 py-2 font-mono text-xs text-card-foreground"
            >
              ✓ {tech}
            </span>
          ))}
        </div>
      </div>
    </main>
  );
}
