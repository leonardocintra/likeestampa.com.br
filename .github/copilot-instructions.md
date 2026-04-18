# Like Estampa — Copilot Instructions

## Project Overview

E-commerce de camisetas. Stack: Next.js 16 (App Router) + Tailwind CSS v4 + TypeScript.
Backend (NestJS) lives in a separate workspace — this repo is **frontend only**.
Full context in `docs/PRD.md`.

## Architecture

- **Next.js 16**: App Router only, Server Components by default, Client Components when interactivity is required
- **Tailwind CSS v4**: Utility-first, design tokens via `@theme`, no CSS modules or styled-components
- **Mobile First**: Base styles for 320px, scale up with `md:` and `lg:` breakpoints
- **API consumption**: Typed fetch wrappers in `lib/api/`, types mirroring backend DTOs in `lib/types/`
- **Payment**: MercadoPago (PIX, cartão, boleto)

## Code Standards

- TypeScript strict mode, no `any`
- Files: `kebab-case`. Components: `PascalCase`. Functions: `camelCase`. Constants: `UPPER_SNAKE_CASE`
- Tests: `*.test.ts` / `*.test.tsx` (Vitest + Testing Library)
- Semantic HTML, WCAG 2.1 AA accessibility
- `next/image` for all images, `next/link` for navigation

## Language

- Code, comments, and commit messages in **English**
- Documentation and user-facing content in **Portuguese (BR)**

## Available Agents

- `@architect` — Architecture review, Next.js patterns and mobile-first enforcement
- `@developer` — Feature implementation with Next.js 16 + Tailwind v4
- `@manager` — PRD decomposition into GitHub Issues/backlog
