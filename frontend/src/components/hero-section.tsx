"use client";

import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

// Simplified, centered hero aligned with modern dark UI

export function HeroSection() {
  return (
    <section className="relative container mx-auto -mt-8 overflow-hidden px-4 pt-24 pb-16">
      <div className="relative z-10 mx-auto w-full max-w-4xl text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          <div className="mx-auto inline-flex items-center gap-2 rounded-full border border-white/10 bg-black/30 px-3 py-1 text-xs text-white/70 shadow-sm">
            <Sparkles className="h-3.5 w-3.5 text-[#00A3E0]" />
            AI-powered transcript intelligence
          </div>

          <h1 className="text-4xl font-extrabold tracking-tight text-white sm:text-5xl md:text-6xl">
            Turn Conversations into Clarity
          </h1>
          <p className="mx-auto max-w-3xl text-base sm:text-lg md:text-xl text-white/70">
            Transform your interview transcripts into actionable insights with our AI-powered analysis platform
          </p>
        </motion.div>
      </div>
    </section>
  );
}
