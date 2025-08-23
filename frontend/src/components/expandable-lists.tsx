import { motion } from "framer-motion";
import { useState } from "react";

function ExpandableList({
  title,
  items,
  delay = 0,
}: {
  title: string;
  items: string[];
  delay?: number;
}) {
  const MAX = 6;
  const [showAll, setShowAll] = useState(false);
  const visible = showAll ? items : items.slice(0, MAX);

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 + delay }}
      className="rounded-2xl border border-white/10 bg-black/30 p-5"
    >
      <div className="mb-3 flex items-center justify-between">
        <div className="text-lg font-semibold text-white">{title}</div>
        {items.length > MAX && (
          <button
            onClick={() => setShowAll((v) => !v)}
            className="text-xs text-[#00A3E0] hover:underline"
          >
            {showAll ? "Show less" : `Show ${items.length - MAX} more`}
          </button>
        )}
      </div>
      <ul className="space-y-2 text-sm text-white/80">
        {visible.length > 0 ? (
          visible.map((h, idx) => (
            <li key={idx} className="list-disc pl-1 marker:text-white/40">
              {h}
            </li>
          ))
        ) : (
          <li className="text-white/50">No {title.toLowerCase()} detected</li>
        )}
      </ul>
    </motion.div>
  );
}

export { ExpandableList };
