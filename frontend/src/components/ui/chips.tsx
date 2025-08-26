"use client";

import { useState } from "react";

function Chips({ items }: { items: string[] }) {
  const MAX = 8;
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? items : items.slice(0, MAX);

  // Single-line chips with responsive end-ellipsis. Full text is available via title tooltip.

  if (items.length === 0)
    return <span className="text-xs text-white/50">—</span>;

  return (
    <div>
      <div className="flex flex-wrap gap-1.5">
        {visible.map((txt, idx) => (
          <span
            key={`${txt}-${idx}`}
            title={txt}
            aria-label={txt}
            className="inline-flex items-center overflow-hidden rounded-full border border-white/15 bg-white/5 px-2 py-0.5 text-xs leading-tight text-white/80 min-w-0 max-w-[22ch] sm:max-w-[26ch] md:max-w-[30ch] lg:max-w-[34ch] xl:max-w-[38ch]"
          >
            <span className="truncate">{txt}</span>
          </span>
        ))}
        {items.length > MAX && !showAll && (
          <button
            onClick={() => setShowAll(true)}
            className="rounded-full border border-white/15 px-2 py-0.5 text-xs text-white/70 hover:bg-white/5"
          >
            +{items.length - MAX}
          </button>
        )}
      </div>
      {showAll && items.length > MAX && (
        <button
          onClick={() => setShowAll(false)}
          className="mt-2 text-xs text-[#00A3E0] hover:underline"
        >
          Show less
        </button>
      )}
    </div>
  );
}

export { Chips };
