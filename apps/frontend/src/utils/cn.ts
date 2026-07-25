import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

/**
 * cn — className Utility
 * =======================
 * Merges class names using clsx and deduplicates Tailwind conflicts
 * using tailwind-merge. Essential for component variants.
 *
 * Reusable pattern: Standard utility in all Tailwind+Shadcn projects.
 *
 * @example
 * cn("px-4 py-2", isActive && "bg-primary", className)
 * cn("text-sm text-red-500", "text-blue-500") // → "text-sm text-blue-500"
 */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/**
 * formatCurrency — Format monetary amounts consistently
 * @example formatCurrency(49.99, "USD") → "$49.99"
 */
export function formatCurrency(
  amount: number,
  currency = "USD",
  locale = "en-US"
): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(amount);
}

/**
 * formatDate — Format ISO date strings for display
 * @example formatDate("2026-07-25T20:00:00Z") → "Jul 25, 2026"
 */
export function formatDate(
  isoString: string,
  options: Intl.DateTimeFormatOptions = {
    year: "numeric",
    month: "short",
    day: "numeric",
  }
): string {
  return new Intl.DateTimeFormat("en-US", options).format(new Date(isoString));
}

/**
 * truncate — Truncate a string to a maximum length with ellipsis
 * @example truncate("Long product title here", 20) → "Long product title..."
 */
export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return `${str.slice(0, maxLength - 3)}...`;
}

/**
 * slugify — Convert a string to a URL-safe slug
 * @example slugify("My Product Title 2026") → "my-product-title-2026"
 */
export function slugify(str: string): string {
  return str
    .toLowerCase()
    .trim()
    .replace(/[^\w\s-]/g, "")
    .replace(/[\s_-]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

/**
 * sleep — Promise-based delay utility for testing/animations
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
