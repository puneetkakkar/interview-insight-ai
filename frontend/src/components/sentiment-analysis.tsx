"use client";

import { motion } from "framer-motion";
import { TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { HighlightsLowlights } from "@/types/interview";

interface SentimentAnalysisProps {
  sentiment: HighlightsLowlights;
}

export function SentimentAnalysis({ sentiment }: SentimentAnalysisProps) {
  const hasHighlights = sentiment.highlights.length > 0;
  const hasLowlights = sentiment.lowlights.length > 0;

  if (!hasHighlights && !hasLowlights) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.7 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="text-2xl font-bold text-slate-800 dark:text-slate-100 mb-2">
          Sentiment Analysis
        </h3>
        <p className="text-slate-600 dark:text-slate-300">
          Key positive moments and areas for improvement identified in the interview
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Highlights */}
        {hasHighlights && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 }}
          >
            <Card className="h-full bg-gradient-to-br from-green-50 to-emerald-100/50 dark:from-green-950/30 dark:to-emerald-900/30 border-green-200 dark:border-green-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-green-700 dark:text-green-300">
                  <div className="p-2 rounded-lg bg-white/50 dark:bg-slate-800/50">
                    <CheckCircle className="w-5 h-5 text-green-600 dark:text-green-400" />
                  </div>
                  Highlights & Strengths
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {sentiment.highlights.map((highlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    className="flex items-start gap-3 p-3 bg-white/60 dark:bg-slate-800/60 rounded-lg border border-green-200/50 dark:border-green-700/50"
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      <TrendingUp className="w-4 h-4 text-green-600 dark:text-green-400" />
                    </div>
                    <p className="text-sm text-green-800 dark:text-green-200 leading-relaxed">
                      {highlight}
                    </p>
                  </motion.div>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )}

        {/* Lowlights */}
        {hasLowlights && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 }}
          >
            <Card className="h-full bg-gradient-to-br from-amber-50 to-orange-100/50 dark:from-amber-950/30 dark:to-orange-900/30 border-amber-200 dark:border-amber-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-amber-700 dark:text-amber-300">
                  <div className="p-2 rounded-lg bg-white/50 dark:bg-slate-800/50">
                    <AlertTriangle className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                  </div>
                  Areas for Improvement
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {sentiment.lowlights.map((lowlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    className="flex items-start gap-3 p-3 bg-white/60 dark:bg-slate-800/60 rounded-lg border border-amber-200/50 dark:border-amber-700/50"
                  >
                    <div className="flex-shrink-0 mt-0.5">
                      <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                    </div>
                    <p className="text-sm text-amber-800 dark:text-amber-200 leading-relaxed">
                      {lowlight}
                    </p>
                  </motion.div>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}