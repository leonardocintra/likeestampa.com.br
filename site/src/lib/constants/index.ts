export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";
export const CLOUDINARY_CLOUD_NAME =
  process.env.NEXT_PUBLIC_CLOUDINARY_CLOUD_NAME ?? "";

export const ROUTES = {
  HOME: "/",
  PRODUCTS: "/products",
  PRODUCT_DETAIL: (slug: string) => `/products/${slug}`,
  CATEGORY: (slug: string) => `/categories/${slug}`,
  CART: "/cart",
  CHECKOUT: "/checkout",
  ORDER_SUCCESS: "/order-success",
  LOGIN: "/login",
  REGISTER: "/register",
  PROFILE: "/profile",
  ORDERS: "/orders",
  ORDER_DETAIL: (id: string) => `/orders/${id}`,
  WISHLIST: "/wishlist",
  ABOUT: "/about",
  CONTACT: "/contact",
  FAQ: "/faq",
  PRIVACY: "/privacy",
  TERMS: "/terms",
} as const;

export const SHIPPING_METHODS = {
  STANDARD: "standard",
  EXPRESS: "express",
} as const;

export const PAYMENT_METHODS = {
  PIX: "pix",
  CREDIT_CARD: "credit_card",
  BOLETO: "boleto",
} as const;
