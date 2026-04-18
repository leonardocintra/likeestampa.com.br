# PRD — Like Estampa: E-commerce de Camisetas

> **Versão:** 2.0  
> **Data:** 2026-04-18  
> **Autor:** Product Management  
> **Status:** Draft  

---

## 1. Visão do Produto

**Like Estampa** é um e-commerce focado na venda de camisetas com estampas exclusivas. O frontend (Next.js) consome uma API REST fornecida por um backend NestJS que vive em **workspace separado**. Este workspace contém exclusivamente o frontend da loja.

### 1.1 Proposta de Valor

| Para | Valor |
|------|-------|
| **Consumidor final** | Comprar camisetas com estampas exclusivas de forma rápida, em um site mobile-first com UX fluida |
| **Negócio** | E-commerce escalável com catálogo gerenciado via admin, pagamentos via MercadoPago e frete calculado em tempo real |

### 1.2 Métricas de Sucesso (North Star)

| Métrica | Alvo (6 meses) |
|---------|-----------------|
| Taxa de conversão visita → compra | ≥ 3% |
| Tempo médio de carregamento (LCP) | ≤ 2.0s |
| NPS | ≥ 50 |
| Receita recorrente mensal (MRR) | R$ 50k |
| Taxa de abandono de carrinho | ≤ 65% |
| % de acessos mobile | Tracking (esperado ≥ 70%) |

---

## 2. Stack Tecnológica

### 2.1 Frontend (este workspace)

| Camada | Tecnologia | Justificativa |
|--------|-----------|---------------|
| **Framework** | Next.js 16 (App Router) | SSR/SSG híbrido, React Server Components, otimização de imagens nativa |
| **Estilização** | Tailwind CSS v4 | Utility-first, design tokens via CSS variables, mobile-first nativo |
| **Imagens** | Cloudinary | CDN de imagens, transformações on-the-fly, WebP/AVIF automático |
| **Linter/Formatter** | Biome 2 | Substitui ESLint + Prettier — config em `biome.json` |
| **Pagamento** | MercadoPago SDK | PIX, cartão de crédito, boleto — foco no mercado brasileiro |
| **Deploy** | Vercel | Edge functions, preview deploys, otimização automática |

### 2.2 Backend (workspace separado — referência)

| Camada | Tecnologia |
|--------|-----------|
| **Framework** | NestJS 11 |
| **ORM** | Prisma 7 |
| **Banco de dados** | PostgreSQL 17 |
| **Cache** | Redis |

> O backend é desenvolvido e mantido em outro repositório. O frontend consome a API via REST.
> **Os contratos da API ainda estão sendo definidos.** A estrutura de dados abaixo é um **rascunho de referência** e será ajustada conforme o backend for implementado.

---

## 3. Personas

### 3.1 Ana — Compradora Mobile (22 anos)
- Navega pelo Instagram, clica em um anúncio e cai no site
- Quer encontrar rapidamente, escolher tamanho/cor e comprar via PIX
- Não tem paciência para sites lentos ou formulários longos
- Espera rastreamento do pedido

### 3.2 João — Comprador Casual (25 anos)
- Procura uma camiseta para presentear
- Navega por categorias e coleções
- Sensível a frete e prazo de entrega
- Compara preços, quer promoções

### 3.3 Ricardo — Comprador Recorrente (35 anos)
- Já comprou antes e volta para novas estampas
- Usa desktop e mobile
- Quer ver novidades e lançamentos
- Espera experiência consistente entre dispositivos

---

## 4. Jornadas do Usuário

### 4.1 Jornada de Descoberta (Home → Catálogo)

```
[Home Page — Mobile First]
    → Banner com promoções/lançamentos (carrossel touch-friendly)
    → Seções: "Novidades", "Mais Vendidas", "Categorias"
    → Busca por texto com sugestões
    → Filtros: categoria, tamanho, cor, preço
    → Grid de produtos responsivo (2 colunas mobile, 4 desktop)
```

### 4.2 Jornada de Produto (PDP — Product Detail Page)

```
[Página de Produto]
    → Galeria de imagens com zoom (swipe no mobile)
    → Seleção de tamanho e cor com indicador de estoque
    → Tabela de medidas
    → Preço + parcelamento MercadoPago
    → Botão "Comprar" sticky no mobile
    → Produtos relacionados
    → Avaliações de clientes
```

### 4.3 Jornada de Checkout

```
[Carrinho]
    → Resumo dos itens (editar quantidade, remover)
    → Cálculo de frete por CEP
    → Cupom de desconto
    → Resumo do pedido
[Checkout]
    → Dados de entrega (endereço)
    → Escolha do frete (opções e prazos)
    → Pagamento via MercadoPago (PIX, cartão, boleto)
    → Confirmação do pedido
    → Redirecionamento para página de sucesso
```

### 4.4 Jornada Pós-Compra

```
[Minha Conta]
    → Histórico de pedidos
    → Rastreamento de entrega
    → Dados pessoais e endereços salvos
    → Lista de desejos (wishlist)
```

---

## 5. Arquitetura

### 5.1 Visão Geral

```
┌─────────────────────────────────────────────────────┐
│              FRONTEND (Next.js 16) — Este Workspace  │
│  App Router / RSC / Client Components / Server Actions│
│  Tailwind CSS v4 / Mobile First / Biome 2            │
└──────────────────────┬──────────────────────────────┘
                       │ REST API (fetch / Server Components)
                       │
┌──────────────────────▼──────────────────────────────┐
│          BACKEND (NestJS 11) — Outro Workspace       │
│  Auth / Catalog / Orders / Shipping / Payments       │
│  (contratos da API em definição)                     │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│              CLOUDINARY — CDN de Imagens             │
│  Upload via backend / Consumo direto via next/image  │
└─────────────────────────────────────────────────────┘
```

### 5.2 Estrutura de Pastas do Frontend

```
src/
  app/
    (shop)/
      page.tsx                # Home
      products/
        page.tsx              # Listagem / Catálogo
        [slug]/page.tsx       # Detalhe do produto (PDP)
      categories/
        [slug]/page.tsx       # Produtos por categoria
      cart/page.tsx           # Carrinho
      checkout/page.tsx       # Checkout
      order-success/page.tsx  # Confirmação
    (account)/
      login/page.tsx
      register/page.tsx
      profile/page.tsx
      orders/page.tsx         # Histórico
      orders/[id]/page.tsx    # Detalhe do pedido
      wishlist/page.tsx
    (institutional)/
      about/page.tsx
      contact/page.tsx
      faq/page.tsx
      privacy/page.tsx
      terms/page.tsx
    layout.tsx
    not-found.tsx
  components/
    ui/                       # Design system primitives (Button, Input, Modal, etc.)
    layout/                   # Header, Footer, MobileNav, Breadcrumb
    product/                  # ProductCard, ProductGrid, ProductGallery, SizeSelector
    cart/                     # CartItem, CartSummary, CartDrawer
    checkout/                 # CheckoutForm, PaymentMethods, ShippingSelector
    home/                     # HeroBanner, FeaturedProducts, CategoryShowcase
  lib/
    api/                      # API client (typed fetch wrappers for backend endpoints)
    hooks/                    # Custom React hooks
    utils/                    # Formatters, validators, helpers
    types/                    # Shared TypeScript types/interfaces (mirrors backend DTOs)
    constants/                # App-wide constants
  styles/
    globals.css               # Tailwind v4 imports + custom tokens
```

### 5.3 Modelo de Dados (Contrato da API — referência)

Estas entidades são gerenciadas pelo backend. O frontend consome via REST API e precisa conhecer os tipos de resposta:

```typescript
// Types que espelham os DTOs do backend

interface Product {
  id: string
  slug: string
  title: string
  description: string
  basePrice: number       // centavos
  images: ProductImage[]
  variants: ProductVariant[]
  category: Category
  tags: string[]
  status: 'ACTIVE' | 'DRAFT' | 'OUT_OF_STOCK'
  createdAt: string
}

interface ProductVariant {
  id: string
  size: 'PP' | 'P' | 'M' | 'G' | 'GG' | 'XGG'
  color: string
  colorHex: string
  stock: number
  sku: string
}

interface ProductImage {
  id: string
  url: string
  alt: string
  order: number
}

interface Category {
  id: string
  slug: string
  name: string
  description?: string
  imageUrl?: string
  parentId?: string
}

interface Order {
  id: string
  items: OrderItem[]
  subtotal: number
  shippingCost: number
  discount: number
  total: number
  status: 'PENDING' | 'PAID' | 'PROCESSING' | 'SHIPPED' | 'DELIVERED' | 'CANCELLED'
  trackingCode?: string
  payment: PaymentInfo
  shipping: ShippingInfo
  createdAt: string
}

interface CartItem {
  productId: string
  variantId: string
  quantity: number
}

interface ShippingOption {
  carrier: string
  service: string
  price: number           // centavos
  deliveryDays: number
}
```

---

## 6. Integrações

### 6.1 MercadoPago (Pagamentos)

| Método | Tipo | Descrição |
|--------|------|-----------|
| **PIX** | Instantâneo | QR Code gerado via API, confirmação por webhook |
| **Cartão de crédito** | Parcelado | Até 12x, processado via Checkout Pro ou Checkout Bricks |
| **Boleto** | 3 dias úteis | Gerado via API, confirmação por webhook |

Fluxo:
1. Frontend envia itens + endereço ao backend
2. Backend cria preferência no MercadoPago
3. Frontend redireciona ou renderiza Checkout Bricks
4. MercadoPago notifica backend via webhook (IPN)
5. Backend atualiza status do pedido
6. Frontend exibe confirmação

### 6.2 Frete

O cálculo de frete é feito pelo backend (integração com Correios/Jadlog/Melhor Envio). O frontend envia o CEP e exibe as opções retornadas.

---

## 7. Requisitos Não-Funcionais

| Requisito | Especificação |
|-----------|---------------|
| **Performance** | LCP < 2.0s, INP < 200ms, CLS < 0.1 (Core Web Vitals) |
| **Mobile First** | Design pensado para mobile, adaptado para desktop |
| **Responsividade** | 320px (mobile) → 1440px (desktop) sem quebras |
| **Acessibilidade** | WCAG 2.1 AA — contraste, navegação por teclado, screen readers |
| **SEO** | SSR para páginas de produto, sitemap dinâmico, structured data (JSON-LD) |
| **Segurança** | OWASP Top 10, LGPD compliance, HTTPS only |
| **Disponibilidade** | 99.5% uptime mensal |
| **Imagens** | Cloudinary CDN + `next/image` loader customizado, WebP/AVIF automático, lazy loading, blur placeholder |
| **Bundle size** | JS bundle < 150kb (first load, gzipped) |

---

## 8. Fases de Entrega

### Fase 1 — MVP (Semanas 1-4)
- [x] Setup do projeto (Next.js 16 + Tailwind v4 + TypeScript + Biome)
- [x] Deploy em staging (Vercel — rodando com página default)
- [ ] Design system base (componentes UI primitivos)
- [ ] Layout responsivo (Header, Footer, MobileNav)
- [ ] Home page com seções de destaque
- [ ] Listagem de produtos (grid, filtros, busca)
- [ ] Página de detalhe do produto (PDP)
- [ ] Carrinho (add, remove, update quantity)
- [ ] Integração com API do backend (client API typed — contratos TBD)

### Fase 2 — Checkout & Pagamento (Semanas 5-7)
- [ ] Fluxo de checkout completo
- [ ] Integração MercadoPago (PIX, cartão, boleto)
- [ ] Cálculo de frete por CEP
- [ ] Página de confirmação de pedido
- [ ] Páginas institucionais (sobre, contato, FAQ, termos, privacidade)

### Fase 3 — Conta do Usuário (Semanas 8-10)
- [ ] Login e registro (email + Google OAuth)
- [ ] Área "Minha Conta" (perfil, endereços)
- [ ] Histórico de pedidos com rastreamento
- [ ] Lista de desejos (wishlist)
- [ ] Cupom de desconto

### Fase 4 — Otimização & Launch (Semanas 11-12)
- [ ] SEO avançado (structured data, sitemap, meta tags dinâmicas)
- [ ] Performance audit (Lighthouse ≥ 95)
- [ ] Testes E2E dos fluxos críticos (Playwright)
- [ ] PWA básico (manifest, offline fallback)
- [ ] Analytics (Google Analytics / Plausible)
- [ ] Go-live em produção

---

## 9. Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Backend API não pronta a tempo | Média | Alto | Mock API com MSW (Mock Service Worker) para desenvolvimento paralelo |
| Performance ruim em mobile | Média | Alto | Lighthouse CI no pipeline, bundle analysis, image optimization |
| Integração MercadoPago complexa | Média | Médio | Usar Checkout Bricks (componente pronto) vs integração custom |
| SEO insuficiente no lançamento | Baixa | Médio | SSR por default, structured data desde a Fase 1 |
| LGPD | Baixa | Alto | Banner de cookies, política de privacidade, consentimento explícito |

---

## 10. Glossário

| Termo | Definição |
|-------|-----------|
| **PDP** | Product Detail Page — página de detalhe do produto |
| **PLP** | Product Listing Page — página de listagem/catálogo |
| **RSC** | React Server Components — componentes executados no servidor |
| **Checkout Bricks** | Componentes prontos do MercadoPago para integração de pagamento |
| **IPN** | Instant Payment Notification — webhook do MercadoPago |
| **Mobile First** | Abordagem de design que prioriza a experiência mobile |

---

## Apêndice A — Referências

- [Next.js 16 Docs](https://nextjs.org/docs)
- [Tailwind CSS v4](https://tailwindcss.com/docs)
- [MercadoPago Developers](https://www.mercadopago.com.br/developers)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [WCAG 2.1](https://www.w3.org/WAI/WCAG21/quickref/)
- [Core Web Vitals](https://web.dev/vitals/)
