export interface ProductImage {
  id: string;
  url: string;
  alt: string;
  isPrimary: boolean;
}

export interface ProductVariant {
  id: string;
  size: string;
  color: string;
  stock: number;
  priceInCents: number;
  sku: string;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  imageUrl?: string;
  parentId?: string;
  children?: Category[];
}

export interface Product {
  id: string;
  name: string;
  description: string;
  shortDescription: string;
  slug: string;
  priceInCents: number;
  originalPriceInCents?: number;
  images: ProductImage[];
  variants: ProductVariant[];
  categories: Category[];
  tags: string[];
  isFeatured: boolean;
  isActive: boolean;
  stockTotal: number;
  rating?: number;
  reviewCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface ProductFilters {
  category?: string;
  minPrice?: number;
  maxPrice?: number;
  sizes?: string[];
  colors?: string[];
  tags?: string[];
  search?: string;
  sortBy?: "name" | "price" | "newest" | "rating";
  sortOrder?: "asc" | "desc";
  page?: number;
  limit?: number;
}

export interface ProductListResponse {
  products: Product[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
  filters: {
    categories: Category[];
    priceRange: {
      min: number;
      max: number;
    };
    availableSizes: string[];
    availableColors: string[];
  };
}
