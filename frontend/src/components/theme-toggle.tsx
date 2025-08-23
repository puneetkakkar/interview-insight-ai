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
      <Button variant="ghost" size="icon" className="w-10 h-10">
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="w-10 h-10 rounded-full glass-strong border-0 shadow-lg hover:shadow-xl transition-all duration-300 group"
    >
      {theme === "light" ? (
        <Moon className="h-5 w-5 text-blue-600 dark:text-blue-400 group-hover:text-coral-600 dark:group-hover:text-coral-400 transition-colors duration-200" />
      ) : (
        <Sun className="h-5 w-5 text-blue-600 dark:text-blue-400 group-hover:text-coral-600 dark:group-hover:text-coral-400 transition-colors duration-200" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}