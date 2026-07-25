/**
 * packages/shared-types/index.ts
 * ================================
 * Cross-stack TypeScript types shared between frontend and backend.
 * Import from this package in any frontend workspace:
 *   import type { User, Product } from '@marketplace/shared-types'
 *
 * These types mirror the backend Pydantic schemas exactly.
 * When backend schemas change, update this file to maintain sync.
 */

// ── Re-export all types from frontend types file ──────────────
// (In a full monorepo setup, this would be the canonical source
//  and apps/frontend/src/types/index.ts would import from here)

export type ID = string;
export type ISODateString = string;
export type Currency = "USD" | "EUR" | "GBP" | "INR";

export type UserRole = "SUPERADMIN" | "VENDOR" | "CUSTOMER";
export type UserStatus = "ACTIVE" | "SUSPENDED" | "BANNED";
export type KycStatus = "PENDING" | "APPROVED" | "REJECTED";
export type ProductStatus = "DRAFT" | "PUBLISHED" | "ARCHIVED";
export type LicenseType = "SINGLE_USE" | "MULTI_DOMAIN" | "UNLIMITED";
export type OrderStatus = "PENDING" | "PAID" | "FULFILLED" | "REFUNDED";
export type PayoutStatus = "HELD_IN_ESCROW" | "RELEASED" | "REFUNDED";
export type LicenseStatus = "ACTIVE" | "REVOKED" | "EXPIRED";
export type ReviewStatus = "PUBLISHED" | "MODERATED" | "HIDDEN";

export interface ApiSuccessResponse<T> {
  success: true;
  data: T;
  meta: {
    timestamp: ISODateString;
    version: string;
    requestId: string;
  };
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Array<{ field: string; reason: string }>;
    traceId?: string;
  };
  meta: {
    timestamp: ISODateString;
    path: string;
    method: string;
  };
}

export interface PaginationMeta {
  limit: number;
  hasNextPage: boolean;
  nextCursor?: string;
  totalCount?: number;
}
