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
        <h3 className="mb-2 text-2xl font-bold bg-gradient-to-r from-blue-800 to-coral-700 dark:from-blue-200 dark:to-coral-200 bg-clip-text text-transparent">
          Interview Timeline
        </h3>
        <p className="text-slate-600 dark:text-slate-300">
          Interactive timeline of events and conversations during the interview
        </p>
      </div>

      {/* Filters */}
      <Card className="glass-strong border-0 shadow-xl">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-lg bg-gradient-to-r from-blue-800 to-coral-700 dark:from-blue-200 dark:to-coral-200 bg-clip-text text-transparent">
            <Filter className="h-5 w-5" />
            Filter & Sort Timeline
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
                className="pl-10 border-2 border-slate-200 dark:border-slate-700 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 rounded-xl transition-all duration-200"
              />
            </div>

            {/* Category Filter */}
            <Select
              value={selectedCategory}
              onValueChange={setSelectedCategory}
            >
              <SelectTrigger className="w-full sm:w-48 border-2 border-slate-200 dark:border-slate-700 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 rounded-xl transition-all duration-200">
                <SelectValue placeholder="Filter by category" />
              </SelectTrigger>
              <SelectContent className="bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl shadow-xl">
                <SelectItem value="all" className="hover:bg-blue-50 dark:hover:bg-blue-950/30">All Categories</SelectItem>
                {categories.map((category) => (
                  <SelectItem key={category} value={category} className="hover:bg-blue-50 dark:hover:bg-blue-950/30">
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
              <SelectTrigger className="w-full sm:w-48 border-2 border-slate-200 dark:border-slate-700 focus:border-blue-500 dark:focus:border-blue-400 focus:ring-2 focus:ring-blue-500/20 dark:focus:ring-blue-400/20 rounded-xl transition-all duration-200">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent className="bg-white dark:bg-slate-900 border-2 border-slate-200 dark:border-slate-700 rounded-xl shadow-xl">
                <SelectItem value="time" className="hover:bg-blue-50 dark:hover:bg-blue-950/30">Sort by Time</SelectItem>
                <SelectItem value="confidence" className="hover:bg-blue-50 dark:hover:bg-blue-950/30">Sort by Confidence</SelectItem>
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
                className="h-auto p-1 text-xs hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"
              >
                <X className="w-3 h-3 mr-1" />
                Clear search
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Timeline */}
      <div className="space-y-6">
        {filteredAndSortedTimeline.map((entry, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.9 + index * 0.05 }}
            className="relative"
          >
            {/* Timeline line */}
            {index < filteredAndSortedTimeline.length - 1 && (
              <div className="absolute top-16 left-6 h-16 w-0.5 bg-gradient-to-b from-blue-300 via-coral-300 to-slate-300 dark:from-blue-600 dark:via-coral-600 dark:to-slate-600" />
            )}

            <Card className="ml-12 glass-strong border-0 shadow-lg hover:shadow-xl transition-all duration-300 group">
              <CardContent className="p-6">
                <div className="flex items-start gap-4">
                  {/* Timeline dot */}
                  <div className="absolute top-6 -left-6 flex h-12 w-12 items-center justify-center rounded-full border-4 border-blue-200 dark:border-blue-700 bg-white dark:bg-slate-900 shadow-lg group-hover:border-coral-300 dark:group-hover:border-coral-600 transition-colors duration-200">
                    <Clock className="h-5 w-5 text-blue-600 dark:text-blue-400 group-hover:text-coral-600 dark:group-hover:text-coral-400 transition-colors duration-200" />
                  </div>

                  <div className="flex-1 space-y-3">
                    {/* Header */}
                    <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
                      <div className="flex items-center gap-3">
                        {entry.timestamp && (
                          <Badge
                            variant="outline"
                            className="bg-gradient-to-r from-slate-100 to-slate-200 dark:from-slate-800 dark:to-slate-700 font-mono text-xs border-slate-300 dark:border-slate-600 rounded-full"
                          >
                            {entry.timestamp}
                          </Badge>
                        )}

                        <Badge
                          className={`${categoryColors[
                            entry.category as keyof typeof categoryColors
                          ] || categoryColors.discussion} border-2 rounded-full font-medium`}
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

                    {/* Content */}
                    <p className="leading-relaxed text-slate-700 dark:text-slate-300">
                      {entry.content}
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {filteredAndSortedTimeline.length === 0 && (
        <Card className="glass-strong border-0 shadow-lg py-12 text-center">
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
