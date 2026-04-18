import Link from "next/link";

interface HeroSectionProps {
  campaign: {
    title: string;
    subtitle: string;
    ctaText: string;
    ctaHref: string;
    badge?: string;
  };
}

export default function HeroSection({ campaign }: HeroSectionProps) {
  return (
    <section
      aria-labelledby="hero-title"
      className="bg-linear-to-br from-primary-dark via-primary to-primary-light text-white"
    >
      <div className="max-w-7xl mx-auto px-4 py-16 sm:px-6 md:py-24 lg:px-8 lg:py-32">
        <div className="max-w-2xl">
          {campaign.badge && (
            <span className="inline-block mb-4 rounded-full bg-white/20 px-4 py-1.5 text-sm font-semibold tracking-wide">
              {campaign.badge}
            </span>
          )}

          <h1
            id="hero-title"
            className="text-3xl font-bold leading-tight tracking-tight md:text-5xl lg:text-6xl"
          >
            {campaign.title}
          </h1>

          <p className="mt-4 text-lg leading-relaxed text-white/80 md:mt-6 md:text-xl">
            {campaign.subtitle}
          </p>

          <Link
            href={campaign.ctaHref}
            className="mt-8 inline-block min-h-11 rounded-lg bg-white px-8 py-3 text-base font-bold text-primary shadow-lg transition-transform hover:scale-105 hover:shadow-xl active:scale-100 md:px-10 md:py-4 md:text-lg"
          >
            {campaign.ctaText}
          </Link>
        </div>
      </div>
    </section>
  );
}
