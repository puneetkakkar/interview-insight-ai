"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { FileText, Send, Sparkles, Clock, TrendingUp } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { LoadingSpinner } from "@/components/ui/loading-spinner";
import { InteractiveTimeline } from "@/components/interactive-timeline";
import { EntityCards } from "@/components/entity-cards";
import { SentimentAnalysis } from "@/components/sentiment-analysis";
import type { TranscriptInput, TranscriptAnalysisResponse, InterviewSummaryState } from "@/types/interview";

export function TranscriptAnalyzer() {
  const [state, setState] = useState<InterviewSummaryState>({
    transcript: "",
    summary: null,
    isLoading: false,
    error: null,
  });

  const handleSubmit = async () => {
    if (!state.transcript.trim()) {
      setState(prev => ({ ...prev, error: "Please enter an interview transcript" }));
      return;
    }

    setState(prev => ({ ...prev, isLoading: true, error: null }));

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
        throw new Error(errorData.message ?? `HTTP error! status: ${response.status}`);
      }
      
      const analysisData = data as TranscriptAnalysisResponse;

      if (analysisData.success && analysisData.data) {
        setState(prev => ({
          ...prev,
          summary: analysisData.data,
          isLoading: false,
        }));
      } else {
        setState(prev => ({
          ...prev,
          error: analysisData.message ?? "Failed to generate summary",
          isLoading: false,
        }));
      }
    } catch {
      setState(prev => ({
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
        <Card className="backdrop-blur-sm bg-white/80 dark:bg-slate-900/80 border-slate-200/50 dark:border-slate-700/50 shadow-xl">
          <CardHeader className="text-center pb-6">
            <div className="flex items-center justify-center gap-3 mb-4">
              <div className="p-3 rounded-full bg-blue-100 dark:bg-blue-900/30">
                <FileText className="w-6 h-6 text-blue-600 dark:text-blue-400" />
              </div>
              <CardTitle className="text-2xl font-bold text-slate-800 dark:text-slate-100">
                Analyze Your Interview Transcript
              </CardTitle>
            </div>
            <p className="text-slate-600 dark:text-slate-300">
              Paste your interview transcript below and let our AI extract valuable insights, 
              timelines, and sentiment analysis to help you understand the conversation better.
            </p>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <div className="space-y-4">
              <Textarea
                placeholder="Paste your interview transcript here... 

Example format:
00:01:00 - Hi, can you tell me about yourself?
00:01:05 - Sure, I'm John Doe, a software engineer with 5 years of experience..."
                value={state.transcript}
                onChange={(e) => setState(prev => ({ ...prev, transcript: e.target.value, error: null }))}
                className="min-h-[200px] text-sm leading-relaxed resize-y border-slate-200 dark:border-slate-700 focus:border-blue-500 dark:focus:border-blue-400 transition-colors"
                disabled={state.isLoading}
              />
              
              <div className="flex justify-between items-center text-sm text-slate-500 dark:text-slate-400">
                <span>{state.transcript.length} characters</span>
                <span className="flex items-center gap-1">
                  <Sparkles className="w-4 h-4" />
                  Recommended: 500+ characters for best results
                </span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row gap-3 sm:justify-between sm:items-center">
              <div className="flex gap-3">
                <Button
                  onClick={handleSubmit}
                  disabled={state.isLoading || !state.transcript.trim()}
                  size="lg"
                  className="flex-1 sm:flex-none bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white shadow-lg hover:shadow-xl transition-all duration-200"
                >
                  {state.isLoading ? (
                    <>
                      <LoadingSpinner size="sm" className="mr-2 p-0" />
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
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
                    className="border-slate-300 dark:border-slate-600 hover:bg-slate-50 dark:hover:bg-slate-800"
                  >
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
                <Alert variant="destructive" className="border-red-200 dark:border-red-800">
                  <AlertDescription className="flex justify-between items-center">
                    <span>{state.error}</span>
                    <Button
                      onClick={handleSubmit}
                      variant="outline"
                      size="sm"
                      className="ml-3 text-red-600 border-red-300 hover:bg-red-50 dark:text-red-400 dark:border-red-700 dark:hover:bg-red-950"
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
                <Card className="p-8 border-dashed border-2 border-slate-300 dark:border-slate-600 bg-slate-50 dark:bg-slate-800/50">
                  <div className="text-center space-y-4">
                    <div className="flex items-center justify-center gap-3">
                      <LoadingSpinner size="md" className="p-0" />
                      <span className="text-lg font-medium text-slate-700 dark:text-slate-300">
                        Analyzing your interview transcript...
                      </span>
                    </div>
                    
                    <div className="space-y-2 max-w-md mx-auto">
                      <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded animate-pulse" />
                      <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded animate-pulse w-4/5" />
                      <div className="h-3 bg-slate-200 dark:bg-slate-700 rounded animate-pulse w-3/5" />
                    </div>
                    
                    <p className="text-sm text-slate-500 dark:text-slate-400">
                      This may take a few moments while we extract insights, entities, and sentiment analysis...
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
            <div className="text-center space-y-4">
              <motion.h2
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
                className="text-3xl font-bold text-slate-800 dark:text-slate-100"
              >
                Analysis Results
              </motion.h2>
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 }}
                className="text-slate-600 dark:text-slate-300 max-w-2xl mx-auto"
              >
                Your interview transcript has been analyzed and processed. 
                Explore the insights below to understand the conversation better.
              </motion.p>
            </div>

            {/* Key Metrics */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="grid grid-cols-1 md:grid-cols-3 gap-6"
            >
              <Card className="text-center bg-gradient-to-br from-blue-50 to-blue-100/50 dark:from-blue-950/30 dark:to-blue-900/30 border-blue-200 dark:border-blue-800">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-center mb-2">
                    <TrendingUp className="w-8 h-8 text-blue-600 dark:text-blue-400" />
                  </div>
                  <div className="text-3xl font-bold text-blue-700 dark:text-blue-300">
                    {state.summary.overall_sentiment}
                  </div>
                  <div className="text-sm text-blue-600 dark:text-blue-400">Overall Sentiment</div>
                </CardContent>
              </Card>

              {state.summary.total_duration && (
                <Card className="text-center bg-gradient-to-br from-green-50 to-green-100/50 dark:from-green-950/30 dark:to-green-900/30 border-green-200 dark:border-green-800">
                  <CardContent className="pt-6">
                    <div className="flex items-center justify-center mb-2">
                      <Clock className="w-8 h-8 text-green-600 dark:text-green-400" />
                    </div>
                    <div className="text-3xl font-bold text-green-700 dark:text-green-300">
                      {state.summary.total_duration}
                    </div>
                    <div className="text-sm text-green-600 dark:text-green-400">Duration</div>
                  </CardContent>
                </Card>
              )}

              <Card className="text-center bg-gradient-to-br from-purple-50 to-purple-100/50 dark:from-purple-950/30 dark:to-purple-900/30 border-purple-200 dark:border-purple-800">
                <CardContent className="pt-6">
                  <div className="flex items-center justify-center mb-2">
                    <FileText className="w-8 h-8 text-purple-600 dark:text-purple-400" />
                  </div>
                  <div className="text-3xl font-bold text-purple-700 dark:text-purple-300">
                    {state.summary.timeline.length}
                  </div>
                  <div className="text-sm text-purple-600 dark:text-purple-400">Timeline Events</div>
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
                <Card className="backdrop-blur-sm bg-white/80 dark:bg-slate-900/80 border-slate-200/50 dark:border-slate-700/50">
                  <CardHeader>
                    <CardTitle className="text-xl text-slate-800 dark:text-slate-100">Key Topics Discussed</CardTitle>
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
                            className="px-4 py-2 text-sm bg-gradient-to-r from-indigo-100 to-purple-100 dark:from-indigo-900/30 dark:to-purple-900/30 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-700"
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