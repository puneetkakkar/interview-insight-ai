"use client";

import { EntityCards } from "@/components/entity-cards";
import { InteractiveTimeline } from "@/components/interactive-timeline";
import { SentimentAnalysis } from "@/components/sentiment-analysis";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { Textarea } from "@/components/ui/textarea";
import type {
  InterviewSummaryState,
  TranscriptAnalysisResponse,
  TranscriptInput,
} from "@/types/interview";
import { AnimatePresence, motion } from "framer-motion";
import {
  ArrowRight,
  Bot,
  Clock,
  FileText,
  ListTree,
  NotepadText,
  Send,
  Sparkles,
  TrendingUp,
  UploadCloud,
  X,
} from "lucide-react";
import { useEffect, useRef, useState, Fragment } from "react";

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
      const minHeight = 140;
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

    // Keep loading while we navigate to avoid flicker
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
        // Persist briefly for the analysis page
        try {
          sessionStorage.setItem("analysis:summary", JSON.stringify(analysisData.data));
        } catch {}
        // Do not drop loading here; navigate immediately to avoid layout shift
        window.location.assign("/analysis");
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
    setState({ transcript: "", summary: null, isLoading: false, error: null });
    try { sessionStorage.removeItem("analysis:summary"); } catch {}
  };

  // Data for the process stepper
  const processSteps = [
    {
      key: "upload",
      number: "1",
      title: "Upload",
      description:
        "Drop in raw text or upload a .txt, .docx, or .pdf file.",
      Icon: UploadCloud,
    },
    {
      key: "analyze",
      number: "2",
      title: "Analyze",
      description:
        "We auto-extract highlights, entities, and other key insights.",
      Icon: Bot,
    },
    {
      key: "summarize",
      number: "3",
      title: "Summarize",
      description:
        "See a timeline of the story with topics and timestamps.",
      Icon: ListTree,
    },
  ];

  return (
    <div className="space-y-16">
      {/* Input Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="mx-auto w-full max-w-4xl">
          <div className="animated-border rounded-xl p-[1px]">
            <div className="relative rounded-xl bg-[#0A0A0A]/80 p-4 sm:p-5">
              <div className="mb-3 flex items-center justify-between gap-3 text-white/70">
                <div className="flex items-center gap-2">
                  <NotepadText className="h-4 w-4 text-[#00A3E0]" />
                  <span className="text-xs sm:text-sm">
                    Which interview transcript would you like to analyze?
                  </span>
                </div>
                <div className="hidden items-center gap-1 text-xs sm:flex">
                  <Sparkles className="h-3 w-3 text-white/60" />
                  Smarter analysis with longer context
                </div>
              </div>
              <Textarea
                ref={textareaRef}
                placeholder="Paste your interview transcript here"
                value={state.transcript}
                onChange={(e) =>
                  setState((prev) => ({
                    ...prev,
                    transcript: e.target.value,
                    error: null,
                  }))
                }
                className="no-scrollbar max-h-[400px] min-h-[140px] resize-none rounded-lg border-0 bg-transparent text-sm leading-relaxed text-white placeholder-white/40 focus-visible:ring-0"
                disabled={state.isLoading}
              />
              <div className="mt-3 flex items-center justify-between text-xs text-white/50">
                <span className="flex items-center gap-2">
                  <div
                    className={`${state.transcript.length > 500 ? "bg-green-500" : "bg-amber-500"} h-1.5 w-1.5 rounded-full`}
                  />
                  {state.transcript.length} characters
                </span>
                <div className="ml-auto flex items-center gap-2">
                  {(state.transcript || state.summary) && (
                    <Button
                      onClick={handleClear}
                      variant="outline"
                      size="icon"
                      disabled={state.isLoading}
                      className="h-10 w-10 rounded-full border-white/10 bg-transparent text-white hover:bg-white/5"
                      aria-label="Clear"
                    >
                      <X className="h-4 w-4" />
                    </Button>
                  )}
                  <Button
                    onClick={handleSubmit}
                    disabled={state.isLoading || !state.transcript.trim()}
                    size="icon"
                    className="h-10 w-10 rounded-full bg-[#00A3E0] text-black transition-transform hover:translate-x-0.5 hover:bg-[#15b7f4]"
                    aria-label="Analyze"
                  >
                    {state.isLoading ? (
                      <LoadingSpinner size="sm" className="p-0" />
                    ) : (
                      <Send className="h-5 w-5 text-white" />
                    )}
                  </Button>
                </div>
              </div>

              {/* Error Alert */}
              {state.error && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className="mt-4"
                >
                  <Alert
                    variant="destructive"
                    className="rounded-md border border-red-500/30 bg-red-500/10 text-red-200"
                  >
                    <AlertDescription className="flex items-center justify-between">
                      <span>{state.error}</span>
                      <Button
                        onClick={handleSubmit}
                        variant="outline"
                        size="sm"
                        className="ml-3 rounded-md border-red-500/40 text-red-100 hover:bg-red-500/20"
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
                  className="mt-4"
                >
                  <div className="rounded-md border border-dashed border-white/15 bg-white/5 p-6 text-center">
                    <div className="space-y-4">
                      <div className="flex items-center justify-center gap-3">
                        <LoadingSpinner size="md" className="p-0" />
                        <span className="text-sm font-medium text-white/80">
                          Analyzing your interview transcript...
                        </span>
                      </div>
                      <div className="mx-auto max-w-md space-y-2">
                        <div className="h-2 animate-pulse rounded bg-white/10" />
                        <div className="h-2 w-4/5 animate-pulse rounded bg-white/10" />
                        <div className="h-2 w-3/5 animate-pulse rounded bg-white/10" />
                      </div>
                      <p className="text-xs text-white/60">
                        This may take a few moments while we extract insights,
                        entities, and sentiment analysis...
                      </p>
                    </div>
                  </div>
                </motion.div>
              )}
            </div>
          </div>
        </div>
      </motion.div>

      {/* Our Process Section */}
      <section className="mx-auto w-full max-w-6xl">
        <div className="flex flex-col items-center gap-8 sm:flex-row sm:items-stretch sm:justify-center sm:gap-10">
          {processSteps.map((step, index) => (
            <Fragment key={step.key}>
              <motion.div
                initial={{ opacity: 0, y: 8 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.05 }}
                className="max-w-xs text-center"
              >
                <div className="mb-1 text-md font-semibold text-white">{step.title}</div>
                <p className="mx-auto max-w-[22rem] text-sm leading-relaxed text-white/75">
                  {step.title === 'Upload'
                    ? 'Paste in your interview transcript.'
                    : step.title === 'Analyze'
                    ? 'Our AI digs into the conversation.'
                    : 'See the story unfold in a timeline.'}
                </p>
                <p className="mx-auto max-w-md text-xs leading-relaxed text-white/40">{step.description}</p>
              </motion.div>

              {index < processSteps.length - 1 && (
                <div className="hidden sm:flex items-center justify-center">
                  <div className="h-12 w-12 cursor-pointer rounded-full border border-white/20 text-white/70 transition hover:translate-x-0.5 hover:text-white flex items-center justify-center">
                    <ArrowRight className="h-5 w-5" />
                  </div>
                </div>
              )}

              {index < processSteps.length - 1 && (
                <div className="sm:hidden -my-2 flex w-full items-center justify-center">
                  <div className="h-10 w-10 cursor-pointer rounded-full border border-white/15 text-white/60 rotate-90 flex items-center justify-center">
                    <ArrowRight className="h-4 w-4" />
                  </div>
                </div>
              )}
            </Fragment>
          ))}
        </div>
      </section>

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
              <Card className="border border-slate-200/80 bg-white/60 shadow-sm dark:border-slate-800 dark:bg-slate-900/60">
                <CardContent className="pt-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs tracking-wide text-slate-500 uppercase dark:text-slate-400">
                      Overall Sentiment
                    </span>
                    <TrendingUp className="h-4 w-4 text-slate-400" />
                  </div>
                  <div className="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">
                    {state.summary.overall_sentiment}
                  </div>
                </CardContent>
              </Card>

              {state.summary.total_duration && (
                <Card className="border border-slate-200/80 bg-white/60 shadow-sm dark:border-slate-800 dark:bg-slate-900/60">
                  <CardContent className="pt-5">
                    <div className="flex items-center justify-between">
                      <span className="text-xs tracking-wide text-slate-500 uppercase dark:text-slate-400">
                        Duration
                      </span>
                      <Clock className="h-4 w-4 text-slate-400" />
                    </div>
                    <div className="mt-2 text-2xl font-semibold text-slate-900 dark:text-slate-100">
                      {state.summary.total_duration}
                    </div>
                  </CardContent>
                </Card>
              )}

              <Card className="border border-slate-200/80 bg-white/60 shadow-sm dark:border-slate-800 dark:bg-slate-900/60">
                <CardContent className="pt-5">
                  <div className="flex items-center justify-between">
                    <span className="text-xs tracking-wide text-slate-500 uppercase dark:text-slate-400">
                      Timeline Events
                    </span>
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
                            className="rounded-full border-slate-200 px-3 py-1 text-xs text-slate-700 dark:border-slate-700 dark:text-slate-300"
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
