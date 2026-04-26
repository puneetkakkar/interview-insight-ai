"use client";

import { ExpandableList } from "@/components/expandable-lists";
import { TimelineAccordion } from "@/components/timeline-accordion";
import { Chips } from "@/components/ui/chips";
import type { TranscriptSummary } from "@/types/interview";
import { motion } from "framer-motion";
import { Brain, Clock, MessageSquare, TrendingUp, Users, Zap } from "lucide-react";

interface AnalysisDashboardProps {
  summary: TranscriptSummary;
}

export function AnalysisDashboard({ summary }: AnalysisDashboardProps) {
  const sentiment = summary.overall_sentiment?.toLowerCase() ?? "";
  const sentimentColor = sentiment.includes("positive")
    ? "text-[hsl(var(--success))]"
    : sentiment.includes("negative")
      ? "text-[hsl(var(--error))]"
      : "text-[hsl(var(--warning))]";

  const sentimentBadgeBg = sentiment.includes("positive")
    ? "bg-[hsl(var(--success))]/10 border-[hsl(var(--success))]/20"
    : sentiment.includes("negative")
      ? "bg-[hsl(var(--error))]/10 border-[hsl(var(--error))]/20"
      : "bg-[hsl(var(--warning))]/10 border-[hsl(var(--warning))]/20";

  const timelineCount = summary.timeline?.length ?? 0;
  const topicCount = summary.key_topics?.length ?? 0;

  return (
    <div className="space-y-5">

      {/* Overview strip */}
      <motion.div
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="grid grid-cols-2 gap-3 sm:grid-cols-3"
      >
        <div className={`rounded-2xl border p-4 ${sentimentBadgeBg}`}>
          <div className="mb-1.5 flex items-center gap-1.5 text-xs text-white/50">
            <Brain className="h-3.5 w-3.5" />
            Overall Sentiment
          </div>
          <div className={`text-base font-semibold capitalize ${sentimentColor}`}>
            {summary.overall_sentiment || "Neutral"}
          </div>
        </div>

        {summary.total_duration ? (
          <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
            <div className="mb-1.5 flex items-center gap-1.5 text-xs text-white/50">
              <Clock className="h-3.5 w-3.5" />
              Duration
            </div>
            <div className="text-base font-semibold text-white">
              {summary.total_duration}
            </div>
          </div>
        ) : null}

        <div className="rounded-2xl border border-white/10 bg-black/30 p-4">
          <div className="mb-1.5 flex items-center gap-1.5 text-xs text-white/50">
            <MessageSquare className="h-3.5 w-3.5" />
            Timeline Events
          </div>
          <div className="text-base font-semibold text-white">{timelineCount}</div>
        </div>
      </motion.div>

      {/* Key Topics */}
      {topicCount > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.05 }}
          className="rounded-2xl border border-white/10 bg-black/30 p-5"
        >
          <div className="mb-3 flex items-center gap-2 text-sm font-semibold text-white">
            <Zap className="h-4 w-4 text-accent" />
            Key Topics
          </div>
          <Chips items={summary.key_topics} />
        </motion.div>
      )}

      {/* Entities */}
      <motion.div
        initial={{ opacity: 0, y: 8 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4, delay: 0.1 }}
        className="rounded-2xl border border-white/10 bg-black/30 p-5"
      >
        <div className="mb-4 flex items-center gap-2 text-sm font-semibold text-white">
          <Users className="h-4 w-4 text-accent" />
          Extracted Entities
        </div>
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
          {(
            [
              { label: "People", items: summary.entities?.people ?? [] },
              { label: "Companies", items: summary.entities?.companies ?? [] },
              { label: "Technologies", items: summary.entities?.technologies ?? [] },
              { label: "Locations", items: summary.entities?.locations ?? [] },
            ] as { label: string; items: string[] }[]
          ).map(({ label, items }) => (
            <div key={label}>
              <div className="mb-2 text-xs font-medium uppercase tracking-wide text-white/40">
                {label}
              </div>
              <Chips items={items} />
            </div>
          ))}
        </div>
      </motion.div>

      {/* Highlights & Lowlights */}
      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
        <ExpandableList
          title="Highlights"
          items={summary.sentiment_analysis?.highlights ?? []}
          delay={0.05}
        />
        <ExpandableList
          title="Lowlights"
          items={summary.sentiment_analysis?.lowlights ?? []}
          delay={0.1}
        />
      </div>

      {/* Timeline */}
      {timelineCount > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.15 }}
          className="rounded-2xl border border-white/10 bg-black/30 p-5"
        >
          <div className="mb-4 flex items-center gap-2 text-sm font-semibold text-white">
            <TrendingUp className="h-4 w-4 text-accent" />
            Interview Timeline
          </div>
          <TimelineAccordion entries={summary.timeline} />
        </motion.div>
      )}

    </div>
  );
}
