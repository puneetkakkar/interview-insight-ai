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
        <div className="mx-auto w-full max-w-6xl">
          <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
            <CardHeader className="pb-6 text-center">
              <div className="mb-4 flex items-center justify-center gap-3">
                <div className="rounded-md border border-slate-200/80 p-2 dark:border-slate-800">
                  <FileText className="h-4 w-4 text-slate-500" />
                </div>
                <CardTitle className="text-xl font-semibold text-slate-900 dark:text-slate-100">
                  Analyze Your Interview Transcript
                </CardTitle>
              </div>
              <p className="mx-auto max-w-2xl text-sm text-slate-600 dark:text-slate-400">
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
                  className="max-h-[400px] min-h-[200px] resize-none rounded-md border border-slate-200/80 bg-white/80 p-4 text-sm leading-relaxed placeholder-slate-400 focus-visible:ring-0 focus:border-slate-400 dark:border-slate-800 dark:bg-slate-900/80 dark:focus:border-slate-600"
                  disabled={state.isLoading}
                />

                {/* Character count and recommendations */}
                <div className="mt-2 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                  <span className="flex items-center gap-2">
                    <div className={`h-1.5 w-1.5 rounded-full ${state.transcript.length > 500 ? "bg-green-500" : "bg-amber-500"}`} />
                    {state.transcript.length} characters
                  </span>
                  <span className="flex items-center gap-1">
                    <Sparkles className="h-3 w-3 text-slate-400" />
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
                  className="flex-1 rounded-md bg-slate-900 text-white hover:bg-slate-800 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-slate-200 sm:flex-none"
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
                    className="rounded-md border border-slate-200/80 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800"
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
                  className="rounded-md border border-red-200 bg-red-50 dark:border-red-800 dark:bg-red-950/50"
                >
                  <AlertDescription className="flex items-center justify-between">
                    <span>{state.error}</span>
                    <Button
                      onClick={handleSubmit}
                      variant="outline"
                      size="sm"
                      className="ml-3 rounded-md border-red-300 text-red-600 hover:bg-red-100 dark:border-red-700 dark:text-red-400 dark:hover:bg-red-900/50"
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
                <Card className="rounded-md border border-dashed border-slate-300/70 bg-white/50 p-8 dark:border-slate-700/70 dark:bg-slate-900/30">
                  <div className="space-y-4 text-center">
                    <div className="flex items-center justify-center gap-3">
                      <LoadingSpinner size="md" className="p-0" />
                      <span className="text-sm font-medium text-slate-700 dark:text-slate-300">
                        Analyzing your interview transcript...
                      </span>
                    </div>

                    <div className="mx-auto max-w-md space-y-2">
                      <div className="h-2 animate-pulse rounded bg-slate-200/80 dark:bg-slate-800/60" />
                      <div className="h-2 w-4/5 animate-pulse rounded bg-slate-200/80 dark:bg-slate-800/60" />
                      <div className="h-2 w-3/5 animate-pulse rounded bg-slate-200/80 dark:bg-slate-800/60" />
                    </div>

                    <p className="text-xs text-slate-500 dark:text-slate-400">
                      This may take a few moments while we extract insights,
                      entities, and sentiment analysis...
                    </p>
                  </div>
                </Card>
              </motion.div>
            )}
          </CardContent>
          </Card>
        </div>
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
            <div className="mx-auto w-full max-w-6xl space-y-2 text-center">
              <motion.h2
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-2xl font-semibold text-slate-900 dark:text-slate-100"
              >
                Analysis Results
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="mx-auto max-w-2xl text-sm text-slate-600 dark:text-slate-400"
              >
                Your interview has been processed. Review the highlights below.
              </motion.p>
            </div>

            {/* Key Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-4 md:grid-cols-3"
            >
              <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
                <CardContent className="pt-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Overall Sentiment</span>
                    <TrendingUp className="h-4 w-4 text-slate-400" />
                  </div>
                  <div className="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">
                    {state.summary.overall_sentiment}
                  </div>
                </CardContent>
              </Card>

              {state.summary.total_duration && (
                <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
                  <CardContent className="pt-5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Duration</span>
                      <Clock className="h-4 w-4 text-slate-400" />
                    </div>
                    <div className="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">
                      {state.summary.total_duration}
                    </div>
                  </CardContent>
                </Card>
              )}

              <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
                <CardContent className="pt-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs uppercase tracking-wide text-slate-500 dark:text-slate-400">Timeline Events</span>
                    <FileText className="h-4 w-4 text-slate-400" />
                  </div>
                  <div className="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">
                    {state.summary.timeline.length}
                  </div>
                </CardContent>
              </Card>
            </motion.div>

            {/* Key Topics */}
            {state.summary.key_topics.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
              >
                <Card className="mx-auto w-full max-w-6xl border border-slate-200/80 bg-white/60 shadow-sm dark:border-slate-800 dark:bg-slate-900/60">
                  <CardHeader>
                    <CardTitle className="text-base font-semibold text-slate-900 dark:text-slate-100">
                      Key Topics
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="flex flex-wrap gap-2">
                      {state.summary.key_topics.map((topic, index) => (
                        <motion.div
                          key={topic}
                          initial={{ opacity: 0, y: 6 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: 0.55 + index * 0.05 }}
                        >
                          <Badge
                            variant="outline"
                            className="rounded-full border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-300 px-3 py-1 text-xs"
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
            <div className="mx-auto w-full max-w-6xl">
              <EntityCards entities={state.summary.entities} />
            </div>

            {/* Sentiment Analysis */}
            <div className="mx-auto w-full max-w-6xl">
              <SentimentAnalysis sentiment={state.summary.sentiment_analysis} />
            </div>

            {/* Interactive Timeline */}
            <div className="mx-auto w-full max-w-6xl">
              <InteractiveTimeline timeline={state.summary.timeline} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
