"use client";

import type { TimelineEntry } from "@/types/interview";
import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { memo, useMemo, useState } from "react";

interface TimelineAccordionProps {
  entries: TimelineEntry[];
}

export const TimelineAccordion = memo(function TimelineAccordion({
  entries,
}: TimelineAccordionProps) {
  const groups = useMemo(() => groupByWindow(entries), [entries]);

  return (
    <div className="space-y-4">
      {groups.map((group, gi) => (
        <div key={gi} className="rounded-xl bg-white/5 p-3">
          <div className="mb-2 flex items-center justify-between">
            <div className="text-sm font-medium text-white/80">
              {group.label}
            </div>
            <div className="text-xs text-white/50">
              {group.items.length} events
            </div>
          </div>
          <div className="border-l border-white/10">
            {group.items.map((item, i) => (
              <TimelineRow
                key={`${gi}-${i}`}
                item={item}
                last={i === group.items.length - 1}
              />
            ))}
          </div>
        </div>
      ))}
    </div>
  );
});

const TimelineRow = memo(function TimelineRow({
  item,
  last,
}: {
  item: TimelineEntry;
  last: boolean;
}) {
  const [open, setOpen] = useState(true);
  return (
    <div className="relative pl-4">
      <div className="absolute top-2 left-[-6px] h-2 w-2 rounded-full bg-[#00A3E0]" />
      {!last && (
        <div className="absolute top-4 left-[-1px] h-full w-px bg-white/10" />
      )}
      <button
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center justify-between py-2 text-left"
      >
        <div className="flex items-center gap-3">
          <span className="rounded bg-white/10 px-2 py-0.5 text-xs text-white/70 whitespace-nowrap inline-block">
            {item.timestamp ?? "—"}
          </span>
          <span className="font-medium text-white/90">{item.category}</span>
        </div>
        <ChevronDown
          className={`h-4 w-4 text-white/60 transition-transform ${open ? "rotate-180" : ""}`}
        />
      </button>

      <motion.div
        initial={false}
        animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}
        className="overflow-hidden pl-5"
      >
        <p className="pb-3 text-sm leading-relaxed text-white/70">
          {item.summary}
        </p>
      </motion.div>
    </div>
  );
});

function groupByWindow(items: TimelineEntry[]) {
  // Group by real time windows (5 minutes) based on each item's timestamp.
  // Falls back to the first window for missing/invalid timestamps.
  const WINDOW_SECONDS = 5 * 60;

  // Parse a single timestamp like "hh:mm:ss", "mm:ss", or "ss"
  const toSecondsSingle = (ts: string | null): number | null => {
    if (!ts) return null;
    const raw = ts.trim();
    if (!raw) return null;
    const parts = raw.split(":").map((p) => p.trim());
    const nums = parts.map((p) => Number(p));
    if (nums.some((n) => Number.isNaN(n))) return null;
    if (nums.length === 3) {
      const [h, m, s] = nums as [number, number, number];
      return h * 3600 + m * 60 + s;
    }
    if (nums.length === 2) {
      const [m, s] = nums as [number, number];
      return m * 60 + s;
    }
    if (nums.length === 1) {
      return (nums as [number])[0] ?? null;
    }
    return null;
  };

  // Parse either a single timestamp ("00:00:22") or a range ("00:00:03-00:00:08").
  // Returns a [startSeconds, endSeconds] tuple. If only one timestamp is present,
  // both start and end will be that value.
  const parseTimestampOrRange = (ts: string | null): [number | null, number | null] => {
    if (!ts) return [null, null];
    const raw = ts.trim();
    if (!raw) return [null, null];
    if (raw.includes("-")) {
      const [startRaw, endRaw] = raw.split("-").map((p) => p.trim());
      const start = toSecondsSingle(startRaw ?? null);
      const end = toSecondsSingle(endRaw ?? null);
      if (start == null && end == null) return [null, null];
      // If only one side parses, treat as a single timestamp
      if (start != null && end == null) return [start, start];
      if (start == null && end != null) return [end, end];
      // Ensure start <= end
      if (start! > end!) return [end!, start!];
      return [start!, end!];
    }
    const single = toSecondsSingle(raw);
    return [single, single];
  };

  const formatTime = (seconds: number) => {
    const total = Math.max(0, Math.floor(seconds));
    const minutes = Math.floor(total / 60);
    const secs = total % 60;
    return `${minutes}:${String(secs).padStart(2, "0")}`;
  };

  // Build buckets keyed by bucket start seconds
  const buckets = new Map<number, TimelineEntry[]>();
  for (const item of items) {
    const [startSecs, endSecs] = parseTimestampOrRange(item.timestamp);

    if (startSecs == null || endSecs == null) {
      // Fallback: put in first window
      const arr = buckets.get(0) ?? [];
      arr.push(item);
      buckets.set(0, arr);
      continue;
    }

    const firstBucketStart = Math.floor(startSecs / WINDOW_SECONDS) * WINDOW_SECONDS;
    const lastBucketStart = Math.floor(endSecs / WINDOW_SECONDS) * WINDOW_SECONDS;

    for (let bucketStart = firstBucketStart; bucketStart <= lastBucketStart; bucketStart += WINDOW_SECONDS) {
      const arr = buckets.get(bucketStart) ?? [];
      arr.push(item);
      buckets.set(bucketStart, arr);
    }
  }

  // Sort by bucket start time
  const sortedStarts = Array.from(buckets.keys()).sort((a, b) => a - b);
  const windows = sortedStarts.map((start) => {
    const end = start + WINDOW_SECONDS;
    const label = `${formatTime(start)} - ${formatTime(end)}`;
    return { label, items: buckets.get(start) ?? [] };
  });

  return windows;
}
