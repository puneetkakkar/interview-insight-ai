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
        <h3 className="text-2xl font-bold bg-gradient-to-r from-blue-800 to-coral-700 dark:from-blue-200 dark:to-coral-200 bg-clip-text text-transparent mb-2">
          Sentiment Analysis
        </h3>
        <p className="text-slate-600 dark:text-slate-300">
          Key positive moments and areas for improvement identified in the interview
        </p>
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
            <Card className="glass-strong border-0 shadow-xl h-full hover:shadow-2xl transition-all duration-300 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-emerald-700 dark:text-emerald-300">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-emerald-100 to-emerald-200 dark:from-emerald-900/40 dark:to-emerald-800/40 group-hover:scale-110 transition-transform duration-200">
                    <CheckCircle className="w-6 h-6 text-emerald-600 dark:text-emerald-400" />
                  </div>
                  <span className="font-semibold">Highlights & Strengths</span>
                  <Badge 
                    variant="secondary" 
                    className="ml-auto bg-gradient-to-r from-emerald-100 to-emerald-200 dark:from-emerald-900/40 dark:to-emerald-800/40 text-emerald-700 dark:text-emerald-300 border-0"
                  >
                    {sentiment.highlights.length}
                  </Badge>
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {sentiment.highlights.map((highlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-emerald-50/80 to-emerald-100/60 dark:from-emerald-900/30 dark:to-emerald-800/20 rounded-xl border-2 border-emerald-200/50 dark:border-emerald-700/30 hover:border-emerald-300 dark:hover:border-emerald-600 transition-colors duration-200"
                  >
                    <div className="flex-shrink-0 mt-1">
                      <div className="p-1.5 rounded-full bg-emerald-100 dark:bg-emerald-800/50">
                        <TrendingUp className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
                      </div>
                    </div>
                    <p className="text-sm text-emerald-800 dark:text-emerald-200 leading-relaxed font-medium">
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
            <Card className="glass-strong border-0 shadow-xl h-full hover:shadow-2xl transition-all duration-300 group">
              <CardHeader>
                <CardTitle className="flex items-center gap-3 text-amber-700 dark:text-amber-300">
                  <div className="p-3 rounded-xl bg-gradient-to-br from-amber-100 to-amber-200 dark:from-amber-900/40 dark:to-amber-800/40 group-hover:scale-110 transition-transform duration-200">
                    <AlertTriangle className="w-6 h-6 text-amber-600 dark:text-amber-400" />
                  </div>
                  <span className="font-semibold">Areas for Improvement</span>
                  <Badge 
                    variant="secondary" 
                    className="ml-auto bg-gradient-to-r from-amber-100 to-amber-200 dark:from-amber-900/40 dark:to-amber-800/40 text-amber-700 dark:text-amber-300 border-0"
                  >
                    {sentiment.lowlights.length}
                  </Badge>
                </CardTitle>
              </CardHeader>
              
              <CardContent className="space-y-4">
                {sentiment.lowlights.map((lowlight, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.9 + index * 0.1 }}
                    className="flex items-start gap-3 p-4 bg-gradient-to-r from-amber-50/80 to-amber-100/60 dark:from-amber-900/30 dark:to-amber-800/20 rounded-xl border-2 border-amber-200/50 dark:border-amber-700/30 hover:border-amber-300 dark:hover:border-amber-600 transition-colors duration-200"
                  >
                    <div className="flex-shrink-0 mt-1">
                      <div className="p-1.5 rounded-full bg-amber-100 dark:bg-amber-800/50">
                        <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
                      </div>
                    </div>
                    <p className="text-sm text-amber-800 dark:text-amber-200 leading-relaxed font-medium">
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
          <Card className="glass border-0 shadow-lg">
            <CardContent className="pt-6">
              <div className="flex items-center justify-center gap-2 mb-2">
                <Sparkles className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                <span className="text-sm font-medium text-slate-600 dark:text-slate-300">
                  Analysis Insight
                </span>
              </div>
              <p className="text-sm text-slate-500 dark:text-slate-400">
                {hasHighlights && hasLowlights 
                  ? `Found ${sentiment.highlights.length} positive aspects and ${sentiment.lowlights.length} areas for improvement`
                  : hasHighlights 
                    ? `Identified ${sentiment.highlights.length} key strengths and positive moments`
                    : `Found ${sentiment.lowlights.length} areas that could be improved for future interviews`
                }
              </p>
            </CardContent>
          </Card>
        </motion.div>
      )}
    </motion.div>
  );
}