import { create } from "zustand";
import { devtools, persist } from "zustand/middleware";

// ── Cart Item Type ────────────────────────────────────────────
export interface CartItem {
  variantId: string;
  productId: string;
  productTitle: string;
  variantName: string;
  price: number;
  currency: string;
  imageUrl: string | null;
  quantity: number;
  licenseType: "SINGLE_USE" | "MULTI_DOMAIN" | "UNLIMITED";
}

// ── Cart Store State & Actions ────────────────────────────────
interface CartState {
  // State
  items: CartItem[];
  isOpen: boolean;

  // Computed (derived)
  totalItems: () => number;
  totalPrice: () => number;

  // Actions
  addItem: (item: CartItem) => void;
  removeItem: (variantId: string) => void;
  updateQuantity: (variantId: string, quantity: number) => void;
  clearCart: () => void;
  toggleCart: () => void;
  setCartOpen: (open: boolean) => void;
}

/**
 * Cart Store — Zustand Global State
 * ===================================
 * Manages the client-side shopping cart state.
 * Persisted in localStorage so cart survives page refreshes.
 * NOTE: Prices are ALWAYS recalculated on the server at checkout —
 *       this store is for UI state only, not financial truth.
 *
 * Reusable pattern: Adapt `CartItem` type for any e-commerce project.
 */
export const useCartStore = create<CartState>()(
  devtools(
    persist(
      (set, get) => ({
        // ── Initial State ──────────────────────────────────────
        items: [],
        isOpen: false,

        // ── Computed Values ────────────────────────────────────
        totalItems: () => get().items.reduce((sum, item) => sum + item.quantity, 0),

        totalPrice: () => get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),

        // ── Actions ────────────────────────────────────────────
        addItem: (newItem: CartItem) =>
          set(
            (state) => {
              const existing = state.items.find((i) => i.variantId === newItem.variantId);
              if (existing) {
                // For digital products, quantity is always 1 (one license per item)
                return state;
              }
              return { items: [...state.items, { ...newItem, quantity: 1 }] };
            },
            false,
            "cart/addItem",
          ),

        removeItem: (variantId: string) =>
          set(
            (state) => ({
              items: state.items.filter((i) => i.variantId !== variantId),
            }),
            false,
            "cart/removeItem",
          ),

        updateQuantity: (variantId: string, quantity: number) =>
          set(
            (state) => ({
              items: state.items.map((i) =>
                i.variantId === variantId ? { ...i, quantity: Math.max(1, quantity) } : i,
              ),
            }),
            false,
            "cart/updateQuantity",
          ),

        clearCart: () => set({ items: [] }, false, "cart/clearCart"),

        toggleCart: () => set((state) => ({ isOpen: !state.isOpen }), false, "cart/toggle"),

        setCartOpen: (open: boolean) => set({ isOpen: open }, false, "cart/setOpen"),
      }),
      {
        name: "cart-storage",
        // Cart persists in localStorage (survives browser sessions)
        // Financial recalculation always happens server-side at checkout
      },
    ),
    { name: "CartStore" },
  ),
);
