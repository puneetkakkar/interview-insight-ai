import { Suspense } from "react";
import { HeroSection } from "@/components/hero-section";
import InterviewSummary from "@/components/interview-summary";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { ThemeToggle } from "@/components/theme-toggle";
import { TranscriptAnalyzer } from "@/components/transcript-analyzer";

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-100 dark:from-slate-900 dark:via-slate-800 dark:to-indigo-900">
      {/* Theme Toggle */}
      <div className="fixed top-4 right-4 z-50">
        <ThemeToggle />
      </div>
      
      {/* Hero Section */}
      <HeroSection />
      
      {/* Main Content */}
      <main className="container mx-auto px-4 pb-16 -mt-8 relative z-10">
        <Suspense fallback={<LoadingSpinner size="lg" />}>
          <TranscriptAnalyzer />
        </Suspense>
      </main>
      
      {/* Background Decoration */}
      <div className="fixed inset-0 -z-10 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-32 w-96 h-96 rounded-full bg-gradient-to-br from-blue-200/30 to-indigo-300/30 blur-3xl" />
        <div className="absolute -bottom-40 -left-32 w-96 h-96 rounded-full bg-gradient-to-tr from-purple-200/20 to-pink-300/20 blur-3xl" />
      </div>
    </div>
  );
}
