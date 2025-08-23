import { HeroSection } from "@/components/hero-section";
import { TranscriptAnalyzer } from "@/components/transcript-analyzer";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Suspense } from "react";
import { Footer } from "@/components/footer";

export default function Home() {
  return (
    <div className="relative min-h-screen overflow-hidden bg-gradient-to-br from-blue-50 via-slate-50 to-coral-50 dark:from-blue-950 dark:via-black dark:to-slate-950">
      {/* Hero Section */}
      <HeroSection />

      {/* Main Content */}
      <main className="relative z-10 container mx-auto -mt-8 px-4 pb-16">
        <Suspense fallback={<LoadingSpinner size="lg" />}>
          <TranscriptAnalyzer />
        </Suspense>
      </main>

      <Footer />
    </div>
  );
}
