import type { CartItem, PaymentMethod, ShippingOption } from "./cart";

export interface Customer {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  phone?: string;
  document?: string;
}

export interface Address {
  id: string;
  street: string;
  number: string;
  complement?: string;
  neighborhood: string;
  city: string;
  state: string;
  zipCode: string;
  country: string;
  isDefault: boolean;
}

export interface OrderItem extends CartItem {
  // Same as CartItem but with order context
}

export interface Order {
  id: string;
  orderNumber: string;
  customerId: string;
  customer: Customer;
  items: OrderItem[];
  shippingAddress: Address;
  billingAddress?: Address;
  shipping: {
    option: ShippingOption;
    trackingCode?: string;
    estimatedDelivery: string;
  };
  payment: {
    method: PaymentMethod;
    status:
      | "pending"
      | "processing"
      | "paid"
      | "failed"
      | "cancelled"
      | "refunded";
    transactionId?: string;
    paidAt?: string;
  };
  status:
    | "pending"
    | "confirmed"
    | "processing"
    | "shipped"
    | "delivered"
    | "cancelled";
  itemsSubtotalInCents: number;
  shippingInCents: number;
  discountInCents?: number;
  totalInCents: number;
  notes?: string;
  createdAt: string;
  updatedAt: string;
  confirmedAt?: string;
  shippedAt?: string;
  deliveredAt?: string;
  cancelledAt?: string;
}

export interface OrderFilters {
  status?: Order["status"][];
  paymentStatus?: Order["payment"]["status"][];
  dateFrom?: string;
  dateTo?: string;
  customerId?: string;
  page?: number;
  limit?: number;
}

export interface OrderListResponse {
  orders: Order[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export interface CreateOrderRequest {
  cartId: string;
  shippingAddressId: string;
  billingAddressId?: string;
  shippingOptionId: string;
  paymentMethodId: string;
  notes?: string;
}
