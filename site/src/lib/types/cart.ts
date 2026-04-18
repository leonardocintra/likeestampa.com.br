export interface CartItem {
  id: string;
  productId: string;
  variantId: string;
  productName: string;
  productSlug: string;
  variantSize: string;
  variantColor: string;
  priceInCents: number;
  quantity: number;
  imageUrl: string;
  maxStock: number;
}

export interface Cart {
  id: string;
  items: CartItem[];
  itemCount: number;
  subtotalInCents: number;
  shippingInCents?: number;
  discountInCents?: number;
  totalInCents: number;
  createdAt: string;
  updatedAt: string;
}

export interface AddToCartRequest {
  productId: string;
  variantId: string;
  quantity: number;
}

export interface UpdateCartItemRequest {
  itemId: string;
  quantity: number;
}

export interface CartCheckout {
  cart: Cart;
  shippingOptions: ShippingOption[];
  paymentMethods: PaymentMethod[];
}

export interface ShippingOption {
  id: string;
  name: string;
  description: string;
  priceInCents: number;
  estimatedDays: number;
  type: "standard" | "express";
}

export interface PaymentMethod {
  id: string;
  name: string;
  type: "pix" | "credit_card" | "boleto";
  description: string;
  isEnabled: boolean;
}
