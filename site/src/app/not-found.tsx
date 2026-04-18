export default function NotFound() {
  return (
    <main className="flex-1 px-4 py-8 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">404</h1>
        <h2 className="text-2xl font-semibold mb-2">Página não encontrada</h2>
        <p className="text-foreground/60">
          A página que você está procurando não existe.
        </p>
      </div>
    </main>
  );
}
