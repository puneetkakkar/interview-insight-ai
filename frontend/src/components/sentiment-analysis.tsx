"use client";

import { motion } from "framer-motion";
import { TrendingUp, AlertTriangle, CheckCircle, Sparkles } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import type { HighlightsLowlights } from "@/types/interview";
import { Badge } from "@/components/ui/badge";

interface SentimentAnalysisProps {
  sentiment: HighlightsLowlights;
}

export function SentimentAnalysis({ sentiment }: SentimentAnalysisProps) {
  const hasHighlights = sentiment.highlights.length > 0;
  const hasLowlights = sentiment.lowlights.length > 0;

  if (!hasHighlights && !hasLowlights) {
    return null;
  }

  // Determine layout based on available content
  const getGridCols = () => {
    if (hasHighlights && hasLowlights) return "grid-cols-1 lg:grid-cols-2";
    return "grid-cols-1";
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.7 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="mb-1 text-xl font-semibold text-slate-900 dark:text-slate-100">Sentiment</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400">Highlights and areas to improve</p>
      </div>

      <div className={`grid ${getGridCols()} gap-6`}>
        {/* Highlights */}
        {hasHighlights && (
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.8 }}
            className="h-full"
          >
            <Card className="h-full border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base font-semibold text-slate-900 dark:text-slate-100">
                  <div className="p-2 rounded-md border border-slate-200/80 dark:border-slate-800">
                    <CheckCircle className="w-4 h-4 text-emerald-600" />
                  </div>
                  <span>Highlights</span>
                  <Badge variant="outline" className="ml-auto rounded-full border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs px-2 py-0.5">
                    {sentiment.highlights.length}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2.5">
                {sentiment.highlights.map((highlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.06 }}
                    className="flex items-start gap-2 rounded-md border border-emerald-200/40 dark:border-emerald-800/40 bg-emerald-50/40 dark:bg-emerald-900/10 p-3"
                  >
                    <TrendingUp className="mt-0.5 h-3.5 w-3.5 text-emerald-600" />
                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
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
            className="h-full"
          >
            <Card className="h-full border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-base font-semibold text-slate-900 dark:text-slate-100">
                  <div className="p-2 rounded-md border border-slate-200/80 dark:border-slate-800">
                    <AlertTriangle className="w-4 h-4 text-amber-600" />
                  </div>
                  <span>Areas for Improvement</span>
                  <Badge variant="outline" className="ml-auto rounded-full border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 text-xs px-2 py-0.5">
                    {sentiment.lowlights.length}
                  </Badge>
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-2.5">
                {sentiment.lowlights.map((lowlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.06 }}
                    className="flex items-start gap-2 rounded-md border border-amber-200/40 dark:border-amber-800/40 bg-amber-50/40 dark:bg-amber-900/10 p-3"
                  >
                    <AlertTriangle className="mt-0.5 h-3.5 w-3.5 text-amber-600" />
                    <p className="text-sm text-slate-700 dark:text-slate-300 leading-relaxed">
                      {lowlight}
                    </p>
                  </motion.div>
                ))}
              </CardContent>
            </Card>
          </motion.div>
        )}
      </div>

      {/* Summary Insight */}
      {(hasHighlights || hasLowlights) && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 1.0 }}
          className="text-center"
        >
          <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
            <CardContent className="pt-5">
              <div className="mb-1 flex items-center justify-center gap-2">
                <Sparkles className="w-4 h-4 text-slate-400" />
                <span className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">
                  Analysis Insight
                </span>
              </div>
              <p className="text-sm text-slate-600 dark:text-slate-400">
                {hasHighlights && hasLowlights
                  ? `Found ${sentiment.highlights.length} strengths and ${sentiment.lowlights.length} areas to improve`
                  : hasHighlights
                    ? `Identified ${sentiment.highlights.length} key strengths`
                    : `Found ${sentiment.lowlights.length} improvement opportunities`}
              </p>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </motion.div>
  );
}