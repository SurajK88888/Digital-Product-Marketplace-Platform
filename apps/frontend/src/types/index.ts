/**
 * Shared TypeScript Types & Interfaces
 * ======================================
 * Cross-domain types used throughout the frontend.
 * These mirror the backend Pydantic schemas and database models.
 * Update this file whenever backend DTOs change to keep full-stack in sync.
 */

// ── Utility Types ─────────────────────────────────────────────
export type ID = string; // UUID v4 string
export type ISODateString = string; // "2026-07-25T20:00:00.000Z"
export type Currency = "USD" | "EUR" | "GBP" | "INR";

// ── Pagination ────────────────────────────────────────────────
export interface PaginationMeta {
  limit: number;
  hasNextPage: boolean;
  nextCursor?: string;
  totalCount?: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: {
    pagination: PaginationMeta;
    timestamp: ISODateString;
    version: string;
    requestId: string;
  };
}

// ── User & Auth ───────────────────────────────────────────────
export type UserRole = "SUPERADMIN" | "VENDOR" | "CUSTOMER";
export type UserStatus = "ACTIVE" | "SUSPENDED" | "BANNED";

export interface User {
  id: ID;
  email: string;
  role: UserRole;
  status: UserStatus;
  displayName: string | null;
  avatarUrl: string | null;
  emailVerified: boolean;
  mfaEnabled: boolean;
  createdAt: ISODateString;
}

export interface LoginCredentials {
  email: string;
  password: string;
  totpCode?: string;
}

export interface RegisterCredentials {
  email: string;
  password: string;
  displayName: string;
}

export interface AuthTokenResponse {
  accessToken: string;
  user: User;
}

// ── Vendor ────────────────────────────────────────────────────
export type KycStatus = "PENDING" | "APPROVED" | "REJECTED";

export interface Vendor {
  id: ID;
  userId: ID;
  storeName: string;
  storeSlug: string;
  kycStatus: KycStatus;
  commissionRate: number;
  ratingAvg: number;
  balanceAvailable: number;
}

// ── Product Catalog ───────────────────────────────────────────
export type ProductStatus = "DRAFT" | "PUBLISHED" | "ARCHIVED";
export type LicenseType = "SINGLE_USE" | "MULTI_DOMAIN" | "UNLIMITED";

export interface Category {
  id: ID;
  parentId: ID | null;
  name: string;
  slug: string;
  description: string | null;
  isActive: boolean;
}

export interface ProductVariant {
  id: ID;
  productId: ID;
  sku: string;
  name: string;
  price: number;
  currency: Currency;
  licenseType: LicenseType;
  versionLabel: string;
  maxDownloads: number;
  isActive: boolean;
}

export interface Product {
  id: ID;
  vendorId: ID;
  categoryId: ID;
  title: string;
  slug: string;
  shortDescription: string;
  fullDescription: string;
  status: ProductStatus;
  priceBase: number;
  currency: Currency;
  ratingAvg: number;
  totalReviews: number;
  downloadCount: number;
  variants: ProductVariant[];
  vendor?: Pick<Vendor, "storeName" | "storeSlug" | "ratingAvg">;
  category?: Pick<Category, "name" | "slug">;
  createdAt: ISODateString;
}

// ── Orders ────────────────────────────────────────────────────
export type OrderStatus = "PENDING" | "PAID" | "FULFILLED" | "REFUNDED";
export type PayoutStatus = "HELD_IN_ESCROW" | "RELEASED" | "REFUNDED";

export interface OrderItem {
  id: ID;
  orderId: ID;
  productId: ID;
  variantId: ID;
  vendorId: ID;
  unitPrice: number;
  quantity: number;
  subtotal: number;
  payoutStatus: PayoutStatus;
  product?: Pick<Product, "title" | "slug">;
  variant?: Pick<ProductVariant, "name" | "licenseType" | "versionLabel">;
}

export interface Order {
  id: ID;
  orderNumber: string;
  totalAmount: number;
  taxAmount: number;
  discountAmount: number;
  currency: Currency;
  status: OrderStatus;
  items: OrderItem[];
  createdAt: ISODateString;
}

// ── Licenses & Downloads ──────────────────────────────────────
export type LicenseStatus = "ACTIVE" | "REVOKED" | "EXPIRED";

export interface LicenseGrant {
  id: ID;
  orderItemId: ID;
  variantId: ID;
  licenseKey: string;
  status: LicenseStatus;
  maxDownloads: number;
  currentDownloads: number;
  expiresAt: ISODateString | null;
  product?: Pick<Product, "title" | "slug">;
  variant?: Pick<ProductVariant, "name" | "versionLabel">;
}

export interface DownloadToken {
  url: string;
  expiresAt: ISODateString;
}

// ── Reviews ───────────────────────────────────────────────────
export type ReviewStatus = "PUBLISHED" | "MODERATED" | "HIDDEN";

export interface Review {
  id: ID;
  productId: ID;
  rating: 1 | 2 | 3 | 4 | 5;
  comment: string;
  isVerifiedPurchase: boolean;
  status: ReviewStatus;
  author?: Pick<User, "displayName" | "avatarUrl">;
  createdAt: ISODateString;
}

// ── API Response Wrappers ──────────────────────────────────────
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
