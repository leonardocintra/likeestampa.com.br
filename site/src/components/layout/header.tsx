import Link from "next/link";

export default function Header() {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <div className="shrink-0">
            <Link href="/" className="text-2xl font-bold text-primary">
              Like Estampa
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:block">
            <div className="flex items-center space-x-8">
              <Link
                href="/products"
                className="text-gray-700 hover:text-primary"
              >
                Produtos
              </Link>
              <Link
                href="/categories/camisetas"
                className="text-gray-700 hover:text-primary"
              >
                Categorias
              </Link>
            </div>
          </nav>

          {/* Cart */}
          <Link
            href="/cart"
            className="p-2 text-gray-600 hover:text-gray-900"
            aria-label="Carrinho"
          >
            <svg
              className="h-6 w-6"
              fill="none"
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              viewBox="0 0 24 24"
              stroke="currentColor"
              aria-hidden="true"
            >
              <path d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13" />
            </svg>
          </Link>
        </div>
      </div>
    </header>
  );
}
