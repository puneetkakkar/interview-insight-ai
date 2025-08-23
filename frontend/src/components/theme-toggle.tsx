"use client";

import { Button } from "@/components/ui/button";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <Button variant="ghost" size="icon" className="h-10 w-10">
        <Sun className="h-4 w-4" />
      </Button>
    );
  }

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
      className="glass-strong group h-10 w-10 rounded-full border-0 shadow-lg transition-all duration-300 hover:shadow-xl"
    >
      {theme === "light" ? (
        <Moon className="group-hover:text-coral-600 dark:group-hover:text-coral-400 h-5 w-5 text-blue-600 transition-colors duration-200 dark:text-blue-400" />
      ) : (
        <Sun className="group-hover:text-coral-600 dark:group-hover:text-coral-400 h-5 w-5 text-blue-600 transition-colors duration-200 dark:text-blue-400" />
      )}
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
