import HeroSection from "@/components/home/hero-section";

const WORLD_CUP_CAMPAIGN = {
  badge: "🏆 Edição Limitada — Copa do Mundo 2026",
  title: "Vista a Torcida. Use a Sua Estampa.",
  subtitle:
    "Camisetas exclusivas da Copa do Mundo 2026 com estampas que só a Like Estampa tem. Qualidade premium, designs únicos e entrega rápida.",
  ctaText: "Ver Coleção Copa 2026",
  ctaHref: "/products",
};

export default function HomePage() {
  return (
    <main className="flex-1">
      <HeroSection campaign={WORLD_CUP_CAMPAIGN} />
    </main>
  );
}
