"use client";

import { cn } from "@/lib/utils";
import { Loader2 } from "lucide-react";

interface ButtonLoaderProps {
  size?: "sm" | "default" | "lg";
  className?: string;
  text?: string;
}

export function ButtonLoader({
  size = "default",
  className,
  text = "Loading...",
}: ButtonLoaderProps) {
  const sizeClasses = {
    sm: "h-3 w-3",
    default: "h-4 w-4",
    lg: "h-5 w-5",
  };

  return (
    <div className={cn("flex items-center gap-2", className)}>
      <Loader2 className={cn("animate-spin", sizeClasses[size])} />
      {text && <span>{text}</span>}
    </div>
  );
}

export function Spinner({
  size = "default",
  className,
}: Omit<ButtonLoaderProps, "text">) {
  const sizeClasses = {
    sm: "h-3 w-3",
    default: "h-4 w-4",
    lg: "h-5 w-5",
  };

  return (
    <Loader2 className={cn("animate-spin", sizeClasses[size], className)} />
  );
}
