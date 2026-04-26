import { Footer } from "@/components/footer";
import { HeroSection } from "@/components/hero-section";
import { TranscriptAnalyzer } from "@/components/transcript-analyzer";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Suspense } from "react";

export default function Home() {
  return (
    <div className="relative flex min-h-[calc(100vh-0px)] flex-col overflow-hidden bg-gradient-to-br from-slate-50 via-slate-50 dark:from-slate-950 dark:via-black dark:to-slate-950">
      {/* Hero Section */}
      <HeroSection />

      {/* Main Content */}
      <main className="relative z-10 container mx-auto -mt-8 flex-1 px-4 pb-16">
        <Suspense fallback={<LoadingSpinner size="lg" />}>
          <TranscriptAnalyzer />
        </Suspense>
      </main>

      <Footer className="mt-auto" />
    </div>
  );
}
