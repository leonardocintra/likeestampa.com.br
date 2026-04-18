---
description: "Use when: writing API client functions, creating fetch wrappers, integrating with backend endpoints, defining TypeScript types for API responses. Covers typed API clients and data fetching patterns."
applyTo: ["src/lib/api/**", "src/lib/types/**"]
---
# API Client & Types Guidelines

## API Client Functions (`lib/api/`)

```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL

export async function getProducts(params?: ProductFilters): Promise<Product[]> {
  const url = new URL(`${API_URL}/products`)
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined) url.searchParams.set(key, String(value))
    })
  }
  const res = await fetch(url, { next: { revalidate: 60 } })
  if (!res.ok) throw new Error(`Failed to fetch products: ${res.status}`)
  return res.json()
}
```

- One file per domain: `products.ts`, `categories.ts`, `orders.ts`, `cart.ts`
- Always type return values — no implicit `any` from `res.json()`
- Use `next: { revalidate: N }` for ISR in Server Components
- Use `cache: 'no-store'` for dynamic data (cart, user session)
- Throw on non-2xx responses — let error boundaries handle it

## Types (`lib/types/`)

- Mirror the backend DTO contracts exactly
- One file per domain: `product.ts`, `order.ts`, `cart.ts`
- Export interfaces, not types (for declaration merging flexibility)
- Prices in **centavos** (integer) — format to BRL on the UI layer

```typescript
export interface Product {
  id: string
  slug: string
  title: string
  description: string
  basePrice: number  // centavos
  images: ProductImage[]
  variants: ProductVariant[]
  category: Category
  tags: string[]
  status: 'ACTIVE' | 'DRAFT' | 'OUT_OF_STOCK'
  createdAt: string
}
```
