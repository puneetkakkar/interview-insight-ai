"use client";

import { TimelineAccordion } from "@/components/timeline-accordion";
import type { TranscriptSummary } from "@/types/interview";
import { motion } from "framer-motion";
import { Building2, Cpu, Users } from "lucide-react";
import { useState } from "react";

interface AnalysisDashboardProps {
  summary: TranscriptSummary;
}

export function AnalysisDashboard({ summary }: AnalysisDashboardProps) {
  const { sentiment_analysis, entities, timeline, overall_sentiment, total_duration } = summary;

  return (
    <div className="space-y-8">
      {/* Top meta row */}
      <div className="mx-auto w-full max-w-6xl">
        <div className="flex flex-wrap items-center justify-between gap-3 text-white/70">
          <div className="flex items-center gap-3">
            <span className="text-xs uppercase tracking-wide text-white/50">Overall sentiment</span>
            <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-white/80">{overall_sentiment}</span>
          </div>
          {total_duration && (
            <div className="flex items-center gap-3">
              <span className="text-xs uppercase tracking-wide text-white/50">Duration</span>
              <span className="rounded-full bg-white/5 px-3 py-1 text-xs text-white/80">{total_duration}</span>
            </div>
          )}
        </div>
      </div>

      {/* Highlights / Lowlights / Entities */}
      <div className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-6 md:grid-cols-3">
        {/* Highlights */}
        <ExpandableList title="Highlights" items={sentiment_analysis.highlights} />

        {/* Lowlights */}
        <ExpandableList title="Lowlights" items={sentiment_analysis.lowlights} delay={0.05} />

        {/* Entities */}
        <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="rounded-2xl border border-white/10 bg-black/30 p-5">
          <div className="mb-4 text-lg font-semibold text-white">Entities</div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-white/60">
                <Users className="h-3.5 w-3.5" /> People
              </div>
              <Chips items={entities.people} />
            </div>
            <div>
              <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-white/60">
                <Building2 className="h-3.5 w-3.5" /> Company
              </div>
              <Chips items={entities.companies} />
            </div>
            <div>
              <div className="mb-2 flex items-center gap-2 text-xs font-medium uppercase tracking-wide text-white/60">
                <Cpu className="h-3.5 w-3.5" /> Technologies
              </div>
              <Chips items={entities.technologies} />
            </div>
          </div>
        </motion.div>
      </div>

      {/* Timeline */}
      <div className="mx-auto w-full max-w-6xl">
        <div className="mb-3 text-xl font-semibold text-white">Timeline</div>
        <div className="rounded-2xl border border-white/10 bg-black/30 p-2 sm:p-3">
          <TimelineAccordion entries={timeline} />
        </div>
      </div>
    </div>
  );
}

function ExpandableList({ title, items, delay = 0 }: { title: string; items: string[]; delay?: number }) {
  const MAX = 6;
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? items : items.slice(0, MAX);

  return (
    <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.4 + delay }} className="rounded-2xl border border-white/10 bg-black/30 p-5">
      <div className="mb-3 flex items-center justify-between">
        <div className="text-lg font-semibold text-white">{title}</div>
        {items.length > MAX && (
          <button onClick={() => setShowAll((v) => !v)} className="text-xs text-[#00A3E0] hover:underline">
            {showAll ? "Show less" : `Show ${items.length - MAX} more`}
          </button>
        )}
      </div>
      <ul className="space-y-2 text-sm text-white/80">
        {visible.length > 0 ? (
          visible.map((h, idx) => (
            <li key={idx} className="list-disc pl-4 marker:text-white/40">{h}</li>
          ))
        ) : (
          <li className="text-white/50">No {title.toLowerCase()} detected</li>
        )}
      </ul>
    </motion.div>
  );
}

function Chips({ items }: { items: string[] }) {
  const MAX = 8;
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? items : items.slice(0, MAX);

  if (items.length === 0) return <span className="text-xs text-white/50">—</span>;

  return (
    <div>
      <div className="flex flex-wrap gap-1.5">
        {visible.map((txt) => (
          <span key={txt} className="rounded-full border border-white/15 bg-white/5 px-2 py-0.5 text-xs text-white/80">{txt}</span>
        ))}
        {items.length > MAX && !showAll && (
          <button onClick={() => setShowAll(true)} className="rounded-full border border-white/15 px-2 py-0.5 text-xs text-white/70 hover:bg-white/5">
            +{items.length - MAX}
          </button>
        )}
      </div>
      {showAll && items.length > MAX && (
        <button onClick={() => setShowAll(false)} className="mt-2 text-xs text-[#00A3E0] hover:underline">Show less</button>
      )}
    </div>
  );
}


