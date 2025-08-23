"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon" className="w-9 h-9">
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="w-9 h-9 rounded-full bg-white/80 dark:bg-slate-800/80 border border-slate-200/50 dark:border-slate-700/50 backdrop-blur-sm hover:bg-white dark:hover:bg-slate-800 transition-colors"
    >
      {theme === "light" ? (
        <Moon className="h-4 w-4 text-slate-600 dark:text-slate-300" />
      ) : (
        <Sun className="h-4 w-4 text-slate-600 dark:text-slate-300" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}