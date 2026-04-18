---
description: "Use when: writing tests, creating test files, setting up mocks, testing components with Testing Library, testing hooks, testing utilities. Covers Vitest + Testing Library patterns."
applyTo: "**/*.test.{ts,tsx}"
---
# Testing Guidelines

## Stack

- **Vitest** for test runner + assertions
- **@testing-library/react** for component tests
- **MSW (Mock Service Worker)** for API mocking

## Component Tests

```tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { ProductCard } from './product-card'

describe('ProductCard', () => {
  const mockProduct = {
    id: '1',
    slug: 'camiseta-legal',
    title: 'Camiseta Legal',
    basePrice: 5990, // R$ 59,90
    images: [{ id: '1', url: '/img.webp', alt: 'Camiseta', order: 0 }],
  }

  it('renders product title and formatted price', () => {
    render(<ProductCard product={mockProduct} />)
    expect(screen.getByText('Camiseta Legal')).toBeInTheDocument()
    expect(screen.getByText('R$ 59,90')).toBeInTheDocument()
  })
})
```

## Rules

- Test **behavior**, not implementation details
- Query by role/label (`getByRole`, `getByLabelText`) over `getByTestId`
- No snapshot tests — they break on any change and add noise
- Mock API calls with MSW, not by mocking fetch directly
- One `describe` per component, `it` blocks for each behavior
