"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Send, Sparkles, Clock, TrendingUp, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { InteractiveTimeline } from "@/components/interactive-timeline";
import { EntityCards } from "@/components/entity-cards";
import { SentimentAnalysis } from "@/components/sentiment-analysis";
import type {
  TranscriptInput,
  TranscriptAnalysisResponse,
  InterviewSummaryState,
} from "@/types/interview";

export function TranscriptAnalyzer() {
  const [state, setState] = useState<InterviewSummaryState>({
    transcript: "",
    summary: null,
    isLoading: false,
    error: null,
  });

  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Smart textarea height adjustment
  useEffect(() => {
    if (textareaRef.current) {
      const textarea = textareaRef.current;
      textarea.style.height = "auto";
      const scrollHeight = textarea.scrollHeight;
      const minHeight = 200;
      const maxHeight = 400;
      const newHeight = Math.min(Math.max(scrollHeight, minHeight), maxHeight);
      textarea.style.height = `${newHeight}px`;

      // Show scrollbar if content exceeds max height
      if (scrollHeight > maxHeight) {
        textarea.style.overflowY = "auto";
      } else {
        textarea.style.overflowY = "hidden";
      }
    }
  }, [state.transcript]);

  const handleSubmit = async () => {
    if (!state.transcript.trim()) {
      setState((prev) => ({
        ...prev,
        error: "Please enter an interview transcript",
      }));
      return;
    }

    setState((prev) => ({ ...prev, isLoading: true, error: null }));

    try {
      const requestData: TranscriptInput = {
        transcript_text: state.transcript,
      };

      const response = await fetch("/api/transcript/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const data: unknown = await response.json();

      if (!response.ok) {
        const errorData = data as { message?: string };
        throw new Error(
          errorData.message ?? `HTTP error! status: ${response.status}`,
        );
      }

      const analysisData = data as TranscriptAnalysisResponse;

      if (analysisData.success && analysisData.data) {
        setState((prev) => ({
          ...prev,
          summary: analysisData.data,
          isLoading: false,
        }));
      } else {
        setState((prev) => ({
          ...prev,
          error: analysisData.message ?? "Failed to generate summary",
          isLoading: false,
        }));
      }
    } catch {
      setState((prev) => ({
        ...prev,
        error: "Network error. Please check your connection and try again.",
        isLoading: false,
      }));
    }
  };

  const handleClear = () => {
    setState({
      transcript: "",
      summary: null,
      isLoading: false,
      error: null,
    });
  };

  return (
    <div className="space-y-8">
      {/* Input Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Card className="glass-strong border-0 shadow-lg">
          <CardHeader className="pb-6 text-center">
            <div className="mb-4 flex items-center justify-center gap-3">
              <div className="to-coral-100 dark:to-coral-900/40 rounded-full bg-gradient-to-br from-blue-100 p-3 dark:from-blue-900/40">
                <FileText className="h-6 w-6 text-blue-600 dark:text-blue-400" />
              </div>
              <CardTitle className="to-coral-700 bg-gradient-to-r from-blue-800 bg-clip-text text-2xl font-bold text-transparent dark:text-white">
                Analyze Your Interview Transcript
              </CardTitle>
            </div>
            <p className="mx-auto max-w-2xl text-slate-600 dark:text-slate-500">
              Paste your interview transcript below and let our AI extract
              valuable insights, timelines, and sentiment analysis to help you
              understand the conversation better.
            </p>
          </CardHeader>

          <CardContent className="space-y-6">
            <div className="space-y-4">
              <div className="relative">
                <Textarea
                  ref={textareaRef}
                  placeholder="Paste your interview transcript here... 

Example format:
00:01:00 - Hi, can you tell me about yourself?
00:01:05 - Sure, I'm John Doe, a software engineer with 5 years of experience..."
                  value={state.transcript}
                  onChange={(e) =>
                    setState((prev) => ({
                      ...prev,
                      transcript: e.target.value,
                      error: null,
                    }))
                  }
                  className="max-h-[400px] min-h-[200px] resize-none rounded-xl border-2 border-slate-200 p-4 text-sm leading-relaxed placeholder-slate-400 transition-all duration-200 focus:border-blue-500 focus:ring-2 focus:ring-blue-500/0 dark:border-slate-500/25 dark:focus:border-blue-400/30"
                  disabled={state.isLoading}
                />

                {/* Character count and recommendations */}
                <div className="mt-2 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
                  <span className="flex items-center gap-2">
                    <div
                      className={`h-2 w-2 rounded-full ${state.transcript.length > 500 ? "bg-green-500" : "bg-amber-500"}`}
                    />
                    {state.transcript.length} characters
                  </span>
                  <span className="flex items-center gap-1 text-xs">
                    <Sparkles className="h-3 w-3" />
                    {state.transcript.length < 500
                      ? "500+ characters recommended"
                      : "Great length!"}
                  </span>
                </div>
              </div>
            </div>

            <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex gap-3">
                <Button
                  onClick={handleSubmit}
                  disabled={state.isLoading || !state.transcript.trim()}
                  size="lg"
                  className="to-coral-600 hover:to-coral-700 flex-1 rounded-xl bg-white font-semibold text-blue-950 shadow-lg transition-all duration-200 hover:cursor-pointer hover:from-blue-700 hover:via-blue-800 hover:shadow-xl sm:flex-none"
                >
                  {state.isLoading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2 p-0" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Send className="mr-2 h-4 w-4" />
                      Generate Analysis
                    </>
                  )}
                </Button>

                {(state.transcript || state.summary) && (
                  <Button
                    onClick={handleClear}
                    variant="outline"
                    size="lg"
                    disabled={state.isLoading}
                    className="rounded-xl border-2 border-slate-300 font-medium transition-all duration-200 hover:cursor-pointer hover:bg-slate-50 dark:border-slate-600 dark:hover:bg-slate-900"
                  >
                    <X className="mr-2 h-4 w-4" />
                    Clear All
                  </Button>
                )}
              </div>
            </div>

            {/* Error Alert */}
            {state.error && (
              <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.95 }}
              >
                <Alert
                  variant="destructive"
                  className="rounded-xl border-2 border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950/50"
                >
                  <AlertDescription className="flex items-center justify-between">
                    <span>{state.error}</span>
                    <Button
                      onClick={handleSubmit}
                      variant="outline"
                      size="sm"
                      className="ml-3 rounded-lg border-red-300 text-red-600 hover:bg-red-100 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/50"
                    >
                      Retry
                    </Button>
                  </AlertDescription>
                </Alert>
              </motion.div>
            )}

            {/* Loading State */}
            {state.isLoading && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
              >
                <Card className="to-coral-50/50 dark:to-coral-950/30 rounded-xl border-2 border-dashed border-blue-300 bg-gradient-to-br from-blue-50/50 p-8 dark:border-blue-700 dark:from-blue-950/30">
                  <div className="space-y-4 text-center">
                    <div className="flex items-center justify-center gap-3">
                      <LoadingSpinner size="md" className="p-0" />
                      <span className="text-lg font-medium text-slate-700 dark:text-slate-300">
                        Analyzing your interview transcript...
                      </span>
                    </div>

                    <div className="mx-auto max-w-md space-y-2">
                      <div className="to-coral-200 dark:to-coral-800 h-3 animate-pulse rounded-full bg-gradient-to-r from-blue-200 dark:from-blue-800" />
                      <div className="to-coral-200 dark:to-coral-800 h-3 w-4/5 animate-pulse rounded-full bg-gradient-to-r from-blue-200 dark:from-blue-800" />
                      <div className="to-coral-200 dark:to-coral-800 h-3 w-3/5 animate-pulse rounded-full bg-gradient-to-r from-blue-200 dark:from-blue-800" />
                    </div>

                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      This may take a few moments while we extract insights,
                      entities, and sentiment analysis...
                    </p>
                  </div>
                </Card>
              </motion.div>
            )}
          </CardContent>
        </Card>
      </motion.div>

      {/* Results Section */}
      <AnimatePresence>
        {state.summary && !state.isLoading && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.6 }}
            className="space-y-8"
          >
            {/* Summary Header */}
            <div className="space-y-4 text-center">
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="to-coral-700 dark:to-coral-200 bg-gradient-to-r from-blue-800 bg-clip-text text-3xl font-bold text-transparent dark:from-blue-200"
              >
                Analysis Results
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="mx-auto max-w-2xl text-slate-600 dark:text-slate-300"
              >
                Your interview transcript has been analyzed and processed.
                Explore the insights below to understand the conversation
                better.
              </motion.p>
            </div>

            {/* Key Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="grid grid-cols-1 gap-6 md:grid-cols-3"
            >
              <Card className="glass-strong border-0 text-center shadow-xl">
                <CardContent className="pt-6">
                  <div className="mb-2 flex items-center justify-center">
                    <div className="rounded-full bg-gradient-to-br from-blue-100 to-blue-200 p-3 dark:from-blue-900/40 dark:to-blue-800/40">
                      <TrendingUp className="h-8 w-8 text-blue-600 dark:text-blue-400" />
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-blue-700 to-blue-800 bg-clip-text text-3xl font-bold text-transparent dark:from-blue-300 dark:to-blue-200">
                    {state.summary.overall_sentiment}
                  </div>
                  <div className="text-sm font-medium text-blue-600 dark:text-blue-400">
                    Overall Sentiment
                  </div>
                </CardContent>
              </Card>

              {state.summary.total_duration && (
                <Card className="glass-strong border-0 text-center shadow-xl">
                  <CardContent className="pt-6">
                    <div className="mb-2 flex items-center justify-center">
                      <div className="from-coral-100 to-coral-200 dark:from-coral-900/40 dark:to-coral-800/40 rounded-full bg-gradient-to-br p-3">
                        <Clock className="text-coral-600 dark:text-coral-400 h-8 w-8" />
                      </div>
                    </div>
                    <div className="from-coral-700 to-coral-800 dark:from-coral-300 dark:to-coral-200 bg-gradient-to-r bg-clip-text text-3xl font-bold text-transparent">
                      {state.summary.total_duration}
                    </div>
                    <div className="text-coral-600 dark:text-coral-400 text-sm font-medium">
                      Duration
                    </div>
                  </CardContent>
                </Card>
              )}

              <Card className="glass-strong border-0 text-center shadow-xl">
                <CardContent className="pt-6">
                  <div className="mb-2 flex items-center justify-center">
                    <div className="rounded-full bg-gradient-to-br from-purple-100 to-purple-200 p-3 dark:from-purple-900/40 dark:to-purple-800/40">
                      <FileText className="h-8 w-8 text-purple-600 dark:text-purple-400" />
                    </div>
                  </div>
                  <div className="bg-gradient-to-r from-purple-700 to-purple-800 bg-clip-text text-3xl font-bold text-transparent dark:from-purple-300 dark:to-purple-200">
                    {state.summary.timeline.length}
                  </div>
                  <div className="text-sm font-medium text-purple-600 dark:text-purple-400">
                    Timeline Events
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Key Topics */}
            {state.summary.key_topics.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Card className="glass-strong border-0 shadow-xl">
                  <CardHeader>
                    <CardTitle className="to-coral-700 dark:to-coral-200 bg-gradient-to-r from-blue-800 bg-clip-text text-xl text-transparent dark:from-blue-200">
                      Key Topics Discussed
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-3">
                      {state.summary.key_topics.map((topic, index) => (
                        <motion.div
                          key={topic}
                          initial={{ opacity: 0, scale: 0.8 }}
                          animate={{ opacity: 1, scale: 1 }}
                          transition={{ delay: 0.6 + index * 0.1 }}
                        >
                          <Badge
                            variant="secondary"
                            className="to-coral-100 dark:to-coral-900/30 rounded-full border-2 border-blue-200 bg-gradient-to-r from-blue-100 px-4 py-2 text-sm font-medium text-blue-700 dark:border-blue-700 dark:from-blue-900/30 dark:text-blue-300"
                          >
                            {topic}
                          </Badge>
                        </motion.div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            )}

            {/* Entity Cards */}
            <EntityCards entities={state.summary.entities} />

            {/* Sentiment Analysis */}
            <SentimentAnalysis sentiment={state.summary.sentiment_analysis} />

            {/* Interactive Timeline */}
            <InteractiveTimeline timeline={state.summary.timeline} />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
