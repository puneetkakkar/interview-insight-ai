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
          <span className="rounded bg-white/10 px-2 py-0.5 text-xs text-white/70">
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
          {item.content}
        </p>
      </motion.div>
    </div>
  );
});

function groupByWindow(items: TimelineEntry[]) {
  const windows: { label: string; items: TimelineEntry[] }[] = [];
  let current: TimelineEntry[] = [];
  let currentLabel = "0:00 - 0:05";

  for (const it of items) {
    current.push(it);
    if (current.length >= 3) {
      windows.push({ label: currentLabel, items: current });
      current = [];
      const parts = currentLabel.split(" - ");
      currentLabel = `${parts[1]} - ${bump(parts[1] ?? "0:00")}`;
    }
  }
  if (current.length) windows.push({ label: currentLabel, items: current });
  return windows;
}

function bump(label: string) {
  // naive bump by 5 minutes for demo; backend already provides timestamps per entry
  const [minPart] = label.split(":");
  const mins = parseInt(minPart?.split(" ").pop() ?? "0", 10) + 5;
  const m = String(mins).padStart(2, "0");
  return `0:${m}`;
}
