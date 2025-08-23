"use client";

import { motion } from "framer-motion";
import { ArrowDown, Brain, Play, Sparkles, Target, Zap } from "lucide-react";
import Image from "next/image";

const features = [
  {
    icon: Brain,
    text: "AI-Powered Analysis",
    description: "Advanced machine learning algorithms",
  },
  {
    icon: Zap,
    text: "Instant Results",
    description: "Real-time processing & insights",
  },
  {
    icon: Target,
    text: "Professional Insights",
    description: "Enterprise-grade analysis",
  },
];

export function HeroSection() {
  return (
    <section className="relative container mx-auto -mt-8 overflow-hidden px-4 pt-20 pb-32">
      {/* Hero Content */}
      <div className="relative z-10 mx-auto w-full max-w-6xl">
        <div className="grid items-center gap-8 lg:grid-cols-2 lg:gap-12">
          {/* Left Column - Text Content */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="order-2 space-y-6 text-center lg:order-1 lg:space-y-8 lg:text-left"
          >
            {/* Badge */}
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: 0.2 }}
              className="to-coral-100 dark:to-coral-900/40 mb-2 inline-flex items-center gap-1 rounded-full border-2 border-blue-200/50 bg-gradient-to-r from-blue-100 px-2 py-2 text-sm font-semibold text-blue-700 dark:border-white/50 dark:from-blue-900/40 dark:text-white"
            >
              <Sparkles className="h-4 w-4" />
              Advanced AI Analysis
            </motion.div>

            {/* Main Heading */}
            <div className="space-y-4 lg:space-y-6">
              <motion.h1
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-3xl leading-tight font-bold tracking-tight sm:text-4xl md:text-5xl"
              >
                <span className="to-coral-700 bg-gradient-to-r bg-clip-text text-transparent dark:text-white">
                  Interview Transcript
                </span>
                <br />
                <span className="from-coral-700 bg-gradient-to-r bg-clip-text text-transparent dark:text-white">
                  Analyzer
                </span>
              </motion.h1>

              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
                className="mx-auto max-w-2xl text-lg leading-relaxed text-slate-600 sm:text-xl md:text-2xl lg:mx-0 dark:text-slate-300"
              >
                Transform your interview transcripts into actionable insights
                with our
                <span className="font-semibold text-slate-700 dark:text-slate-200">
                  {" "}
                  AI-powered analysis platform
                </span>
              </motion.p>
            </div>

            {/* Features */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.6 }}
              className="mx-auto grid max-w-md grid-cols-1 gap-4 sm:grid-cols-3 lg:mx-0"
            >
              {features.map((feature, index) => (
                <motion.div
                  key={feature.text}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.7 + index * 0.1 }}
                  className="group flex flex-col items-center gap-3 hover:cursor-pointer lg:items-start"
                >
                  <div className="rounded-xl border-2 border-blue-500/50 p-3 shadow-md transition-all duration-300 group-hover:scale-110 dark:border-white/30 dark:from-white/30 dark:to-white/30 dark:group-hover:border-blue-400">
                    <feature.icon className="h-5 w-5 text-blue-600 dark:text-white" />
                  </div>
                  <div className="text-center lg:text-left">
                    <span className="block text-sm font-semibold text-slate-700 dark:text-slate-200">
                      {feature.text}
                    </span>
                    <span className="text-xs text-slate-500 dark:text-slate-400">
                      {feature.description}
                    </span>
                  </div>
                </motion.div>
              ))}
            </motion.div>

            {/* CTA Button */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.8 }}
              className="flex flex-col items-center justify-center gap-4 sm:flex-row lg:justify-start"
            >
              <button className="group inline-flex w-full transform items-center justify-center gap-2 rounded-xl bg-white px-8 py-2 font-semibold text-transparent shadow-md transition-all duration-300 hover:cursor-pointer sm:w-auto">
                <span className="flex items-center gap-2 text-[rgb(0,51,102)] group-hover:text-[rgb(15,82,186)]">
                  <Play className="h-5 w-5 text-[rgb(0,51,102)] group-hover:text-[rgb(15,82,186)]" />
                  Get Started
                </span>
              </button>
              {/* <button className="to-coral-600 hover:to-coral-700 inline-flex w-full transform items-center justify-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 via-blue-700 px-8 py-4 font-semibold text-white shadow-lg transition-all duration-300 hover:scale-105 hover:from-blue-700 hover:via-blue-800 hover:shadow-xl sm:w-auto">
                <Play className="h-5 w-5" />
                Get Started
              </button> */}
              {/* <button className="inline-flex w-full items-center justify-center gap-2 rounded-xl border-2 border-slate-300 px-6 py-4 font-medium text-slate-700 transition-all duration-200 hover:bg-slate-50 sm:w-auto dark:border-slate-600 dark:text-slate-300 dark:hover:bg-slate-800">
                Learn More
              </button> */}
            </motion.div>

            {/* Scroll Indicator */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1.0 }}
              className="pt-8 lg:hidden"
            >
              <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeInOut",
                }}
                className="inline-flex flex-col items-center gap-2 text-slate-400 dark:text-slate-500"
              >
                <span className="text-sm font-medium">Scroll to explore</span>
                <ArrowDown className="h-5 w-5" />
              </motion.div>
            </motion.div>
          </motion.div>

          {/* Right Column - Image */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative order-1 flex justify-center lg:order-2"
          >
            {/* Main Image Container */}
            <div className="relative">
              {/* Background Glow */}
              {/* <div className="via-coral-400/20 absolute inset-0 rounded-3xl bg-gradient-to-br from-blue-400/20 to-purple-400/20 blur-3xl" /> */}

              {/* Image Container */}

              <Image
                src="/images/interview-analyzer-image.svg"
                alt="Interview Transcript Analyzer"
                width={600}
                height={600}
                className="h-auto w-full max-w-sm sm:max-w-md lg:max-w-lg xl:max-w-xl"
                priority
              />

              {/* Floating Elements - Hidden on mobile for better UX */}
              {/* <motion.div
                  animate={{
                    y: [0, -10, 0],
                    rotate: [0, 5, 0],
                  }}
                  transition={{
                    duration: 4,
                    repeat: Infinity,
                    ease: "easeInOut",
                  }}
                  className="to-coral-100 dark:to-coral-800/40 absolute -top-4 -right-4 hidden h-12 w-12 items-center justify-center rounded-2xl border-2 border-blue-200/50 bg-gradient-to-br from-blue-100 shadow-lg sm:block lg:h-16 lg:w-16 dark:border-blue-700/50 dark:from-blue-800/40"
                >
                  <Brain className="h-6 w-6 text-blue-600 lg:h-8 lg:w-8 dark:text-blue-400" />
                </motion.div>

                <motion.div
                  animate={{
                    y: [0, 10, 0],
                    rotate: [0, -5, 0],
                  }}
                  transition={{
                    duration: 3,
                    repeat: Infinity,
                    ease: "easeInOut",
                    delay: 1,
                  }}
                  className="from-coral-100 dark:from-coral-800/40 border-coral-200/50 dark:border-coral-700/50 absolute -bottom-4 -left-4 flex hidden h-12 w-12 items-center justify-center rounded-2xl border-2 bg-gradient-to-br to-purple-100 shadow-lg sm:block lg:h-16 lg:w-16 dark:to-purple-800/40"
                >
                  <Zap className="text-coral-600 dark:text-coral-400 h-6 w-6 lg:h-8 lg:w-8" />
                </motion.div> */}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Enhanced Animated Background Elements */}
    </section>
  );
}
