import Link from "next/link";

export default function MobileNav() {
  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="grid grid-cols-5 h-16">
        {/* Home */}
        <Link
          href="/"
          className="flex flex-col items-center justify-center min-h-[44px] text-gray-600 hover:text-primary"
          aria-label="Home"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
          </svg>
          <span className="text-xs mt-1">Home</span>
        </Link>

        {/* Categories */}
        <Link
          href="/categories/camisetas"
          className="flex flex-col items-center justify-center min-h-[44px] text-gray-600 hover:text-primary"
          aria-label="Categorias"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
          </svg>
          <span className="text-xs mt-1">Categorias</span>
        </Link>

        {/* Search */}
        <Link
          href="/products"
          className="flex flex-col items-center justify-center min-h-[44px] text-gray-600 hover:text-primary"
          aria-label="Buscar"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
          </svg>
          <span className="text-xs mt-1">Busca</span>
        </Link>

        {/* Cart */}
        <Link
          href="/cart"
          className="flex flex-col items-center justify-center min-h-[44px] text-gray-600 hover:text-primary"
          aria-label="Carrinho"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13"></path>
          </svg>
          <span className="text-xs mt-1">Carrinho</span>
        </Link>

        {/* Account */}
        <Link
          href="/profile"
          className="flex flex-col items-center justify-center min-h-[44px] text-gray-600 hover:text-primary"
          aria-label="Conta"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth="2"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
          </svg>
          <span className="text-xs mt-1">Conta</span>
        </Link>
      </div>
    </nav>
  );
}
