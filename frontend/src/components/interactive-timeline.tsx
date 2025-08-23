"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import type { TimelineEntry } from "@/types/interview";
import { motion } from "framer-motion";
import { Clock, Filter, Search, Star, X } from "lucide-react";
import { useMemo, useState } from "react";

interface InteractiveTimelineProps {
  timeline: TimelineEntry[];
}

const categoryColors = {
  introduction:
    "bg-blue-100 dark:bg-blue-900/40 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-700",
  problem_description:
    "bg-coral-100 dark:bg-coral-900/40 text-coral-700 dark:text-coral-300 border-coral-200 dark:border-coral-700",
  solution_discussion:
    "bg-emerald-100 dark:bg-emerald-900/40 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-700",
  coding:
    "bg-purple-100 dark:bg-purple-900/40 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-700",
  testing:
    "bg-amber-100 dark:bg-amber-900/40 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-700",
  questions:
    "bg-indigo-100 dark:bg-indigo-900/40 text-indigo-700 dark:text-indigo-300 border-indigo-200 dark:border-indigo-700",
  conclusion:
    "bg-slate-100 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700",
  discussion:
    "bg-slate-100 dark:bg-slate-800/40 text-slate-700 dark:text-slate-300 border-slate-200 dark:border-slate-700",
};

export function InteractiveTimeline({ timeline }: InteractiveTimelineProps) {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [sortBy, setSortBy] = useState<"time" | "confidence">("time");
  const [expandedByIndex, setExpandedByIndex] = useState<Record<number, boolean>>({});

  const categories = useMemo(() => {
    const cats = Array.from(new Set(timeline.map((item) => item.category)));
    return cats.sort();
  }, [timeline]);

  const filteredAndSortedTimeline = useMemo(() => {
    let filtered = timeline.filter((item) => {
      const matchesSearch = item.content
        .toLowerCase()
        .includes(searchTerm.toLowerCase());
      const matchesCategory =
        selectedCategory === "all" || item.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });

    if (sortBy === "confidence") {
      filtered = filtered.sort(
        (a, b) => (b.confidence_score ?? 0) - (a.confidence_score ?? 0),
      );
    } else {
      filtered = filtered.sort((a, b) => {
        if (!a.timestamp && !b.timestamp) return 0;
        if (!a.timestamp) return 1;
        if (!b.timestamp) return -1;
        return a.timestamp.localeCompare(b.timestamp);
      });
    }

    return filtered;
  }, [timeline, searchTerm, selectedCategory, sortBy]);

  if (timeline.length === 0) {
    return null;
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.8 }}
      className="space-y-6"
    >
      <div className="text-center">
        <h3 className="mb-1 text-xl font-semibold text-slate-900 dark:text-slate-100">Timeline</h3>
        <p className="text-sm text-slate-600 dark:text-slate-400">Browse interview events and filter by type</p>
      </div>

      {/* Filters */}
      <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-base font-semibold text-slate-900 dark:text-slate-100">
            <Filter className="h-4 w-4 text-slate-400" />
            <span>Filters</span>
          </CardTitle>
        </CardHeader>

        <CardContent className="space-y-4">
          <div className="flex flex-col gap-4 sm:flex-row">
            {/* Search */}
            <div className="relative flex-1">
              <Search className="absolute top-1/2 left-3 h-4 w-4 -translate-y-1/2 transform text-slate-400" />
              <Input
                placeholder="Search timeline content..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 rounded-md border border-slate-200/80 dark:border-slate-800 focus-visible:ring-0 focus:border-slate-400 dark:focus:border-slate-600 bg-white/80 dark:bg-slate-900/80"
              />
            </div>

            {/* Category Filter */}
            <Select
              value={selectedCategory}
              onValueChange={setSelectedCategory}
            >
              <SelectTrigger className="w-full sm:w-48 rounded-md border border-slate-200/80 dark:border-slate-800 focus:ring-0 focus:border-slate-400 dark:focus:border-slate-600 bg-white/80 dark:bg-slate-900/80">
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-md shadow-lg">
                <SelectItem value="all" className="hover:bg-slate-50 dark:hover:bg-slate-800">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category} className="hover:bg-slate-50 dark:hover:bg-slate-800">
                    {category
                      .replace(/_/g, " ")
                      .replace(/\b\w/g, (l) => l.toUpperCase())}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>

            {/* Sort */}
            <Select
              value={sortBy}
              onValueChange={(value) =>
                setSortBy(value as "time" | "confidence")
              }
            >
              <SelectTrigger className="w-full sm:w-48 rounded-md border border-slate-200/80 dark:border-slate-800 focus:ring-0 focus:border-slate-400 dark:focus:border-slate-600 bg-white/80 dark:bg-slate-900/80">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent className="bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 rounded-md shadow-lg">
                <SelectItem value="time" className="hover:bg-slate-50 dark:hover:bg-slate-800">Sort by Time</SelectItem>
                <SelectItem value="confidence" className="hover:bg-slate-50 dark:hover:bg-slate-800">Sort by Confidence</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="flex items-center gap-2 text-sm text-slate-600 dark:text-slate-400">
            <span>
              Showing {filteredAndSortedTimeline.length} of {timeline.length}{" "}
              events
            </span>
            {searchTerm && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setSearchTerm("")}
                className="h-auto p-1 text-xs hover:bg-slate-100 dark:hover:bg-slate-800 rounded-md"
              >
                <X className="w-3 h-3 mr-1" />
                Clear search
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Timeline */}
      <div className="relative">
        {/* Continuous rail */}
        <div className="absolute inset-y-0 left-6 w-px bg-slate-200 dark:bg-slate-700" />

        <div className="space-y-6">
          {filteredAndSortedTimeline.map((entry, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.9 + index * 0.05 }}
              className="relative pl-14"
            >
              {/* Node */}
              <div className="absolute top-5 left-6 -translate-x-1/2 flex h-8 w-8 items-center justify-center rounded-full border border-slate-200/80 bg-white shadow-sm dark:border-slate-800 dark:bg-slate-900">
                <Clock className="h-4 w-4 text-slate-500" />
              </div>

              <Card className="border border-slate-200/80 bg-white/60 shadow-sm hover:shadow-md transition-all duration-200 dark:border-slate-800 dark:bg-slate-900/60">
                <CardContent className="p-5">
                  <div className="flex-1 space-y-3">
                    {/* Header */}
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                      <div className="flex items-center gap-3">
                        {entry.timestamp && (
                          <Badge
                            variant="outline"
                            className="font-mono text-xs rounded-full border-slate-200 text-slate-700 dark:border-slate-700 dark:text-slate-300"
                          >
                            {entry.timestamp}
                          </Badge>
                        )}

                        <Badge
                          className={`${categoryColors[
                            entry.category as keyof typeof categoryColors
                          ] || categoryColors.discussion} rounded-full font-medium border`}
                        >
                          {entry.category
                            .replace(/_/g, " ")
                            .replace(/\b\w/g, (l) => l.toUpperCase())}
                        </Badge>
                      </div>

                      {entry.confidence_score && (
                        <div className="flex items-center gap-1 text-sm text-slate-600 dark:text-slate-400">
                          <Star className="h-4 w-4 text-amber-500" />
                          <span>
                            {Math.round(entry.confidence_score * 100)}%
                            confidence
                          </span>
                        </div>
                      )}
                    </div>

                    {/* Content with smart truncation */}
                    {(() => {
                      const MAX_CHARS = 160;
                      const isExpanded = !!expandedByIndex[index];
                      const content = entry.content ?? "";
                      const isLong = content.length > MAX_CHARS;
                      const text = isExpanded || !isLong ? content : `${content.slice(0, MAX_CHARS)}…`;
                      return (
                        <div>
                          <p className="break-words leading-relaxed text-slate-700 dark:text-slate-300">
                            {text}
                          </p>
                          {isLong && (
                            <Button
                              variant="ghost"
                              size="sm"
                              className="h-auto px-0 text-xs text-slate-600 hover:text-slate-900 dark:text-slate-400 dark:hover:text-slate-200"
                              onClick={() =>
                                setExpandedByIndex((prev) => ({
                                  ...prev,
                                  [index]: !isExpanded,
                                }))
                              }
                            >
                              {isExpanded ? "Show less" : "Show more"}
                            </Button>
                          )}
                        </div>
                      );
                    })()}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      {filteredAndSortedTimeline.length === 0 && (
        <Card className="border border-slate-200/80 dark:border-slate-800 bg-white/60 dark:bg-slate-900/60 shadow-sm py-12 text-center">
          <CardContent>
            <div className="space-y-2 text-slate-400 dark:text-slate-600">
              <Search className="mx-auto h-12 w-12" />
              <p className="text-lg font-medium">No timeline events found</p>
              <p className="text-sm">
                Try adjusting your search or filter criteria
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </motion.div>
  );
}
