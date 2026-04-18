---
description: "Use when: writing React components, creating pages, building UI elements, styling with Tailwind. Covers Next.js 16 component patterns, Server vs Client boundaries, and Tailwind v4 utility classes."
applyTo: "**/*.tsx"
---
# Next.js 16 + Tailwind v4 Component Guidelines

## Server vs Client Components

- Default is **Server Component** — no directive needed
- Add `'use client'` ONLY when the component uses: hooks (`useState`, `useEffect`, etc.), event handlers (`onClick`, `onChange`), browser APIs (`window`, `localStorage`), or third-party client libs
- Never fetch data in Client Components with `fetch` — use hooks or pass data as props from Server Components

## Tailwind v4 — Mobile First

```tsx
// ✅ Correct: mobile base → scale up
<div className="px-4 py-3 text-sm md:px-6 md:py-4 md:text-base lg:px-8">

// ❌ Wrong: desktop first
<div className="px-8 py-4 text-base sm:px-4 sm:py-3 sm:text-sm">
```

- Touch targets: `min-h-11` (44px) for buttons and links on mobile
- Use `gap-*` over margin for spacing between siblings
- Prefer `grid` for layouts, `flex` for alignment

## Component Pattern

```tsx
interface ProductCardProps {
  product: Product
}

export function ProductCard({ product }: ProductCardProps) {
  return (
    <article className="group rounded-lg border border-gray-200 overflow-hidden">
      {/* Semantic HTML + accessible */}
    </article>
  )
}
```

## Images

Always use `next/image` with `sizes` for responsive:
```tsx
<Image src={url} alt={alt} width={400} height={400} sizes="(max-width: 768px) 50vw, 25vw" />
```
