"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Home, Menu, Sparkles, X } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";

export function Navigation() {
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    {
      href: "/",
      label: "Home",
      icon: Home,
      description: "",
    },
  ];

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-blue-200/50 bg-white/90 shadow-xl backdrop-blur-xl dark:border-slate-700/50 dark:bg-slate-900/90">
      <div className="container mx-auto px-3 sm:px-4 md:px-6">
        <div className="flex h-12 items-center justify-between sm:h-14">
          {/* Logo/Brand */}
          <div className="group flex items-center space-x-2 sm:space-x-3">
            <div className="sm:block">
              <div className="flex items-center gap-2">
                <div className="to-coral-100 dark:to-coral-900/40 rounded-xl bg-gradient-to-br from-blue-100 p-2 dark:from-blue-900/40">
                  <Sparkles className="h-4 w-4 text-blue-600 dark:text-blue-400" />
                </div>
                <h1 className="text-sm font-bold text-blue-800 transition-colors duration-300 sm:text-base dark:text-blue-200">
                  FRAI AI
                </h1>
              </div>
            </div>
          </div>

          {/* Desktop Navigation Items */}
          <div className="hidden items-center space-x-1 md:flex">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = pathname === item.href;

              return (
                <Link key={item.href} href={item.href}>
                  <Button
                    variant={isActive ? "default" : "ghost"}
                    size="sm"
                    className={cn(
                      "relative h-9 rounded-xl px-3 font-medium transition-all duration-200",
                      isActive
                        ? "to-coral-600 hover:to-coral-700 bg-gradient-to-r from-blue-600 text-white shadow-lg hover:from-blue-700"
                        : "border border-transparent text-slate-600 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 dark:text-slate-300 dark:hover:border-blue-700/50 dark:hover:bg-blue-950/30 dark:hover:text-blue-300",
                    )}
                  >
                    <Icon className="mr-2 h-4 w-4" />
                    <span className="text-sm">{item.label}</span>
                  </Button>
                </Link>
              );
            })}
          </div>

          {/* Right side - Status indicator */}
          <div className="flex items-center space-x-2 sm:space-x-3">
            {/* Mobile menu button */}
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 rounded-xl border border-transparent p-0 text-slate-600 transition-all duration-200 hover:bg-blue-50 hover:text-blue-700 sm:h-9 sm:w-9 md:hidden dark:text-slate-300 dark:hover:bg-blue-950/30 dark:hover:text-blue-300"
              onClick={toggleMobileMenu}
            >
              {isMobileMenuOpen ? (
                <X className="h-4 w-4" />
              ) : (
                <Menu className="h-4 w-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation Menu */}
        <div
          className={cn(
            "overflow-hidden transition-all duration-300 ease-in-out md:hidden",
            isMobileMenuOpen ? "max-h-96 opacity-100" : "max-h-0 opacity-0",
          )}
        >
          <div className="border-t border-blue-200/50 bg-white/95 shadow-xl backdrop-blur-xl dark:border-slate-700/50 dark:bg-slate-900/95">
            <div className="space-y-1 px-3 py-3 sm:px-4 sm:py-4">
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = pathname === item.href;

                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <Button
                      variant={isActive ? "default" : "ghost"}
                      className={cn(
                        "h-10 w-full justify-start rounded-xl px-3 font-medium transition-all duration-200 sm:h-11 sm:px-4",
                        isActive
                          ? "to-coral-600 bg-gradient-to-r from-blue-600 text-white shadow-lg"
                          : "border border-transparent text-slate-600 hover:border-blue-200 hover:bg-blue-50 hover:text-blue-700 dark:text-slate-300 dark:hover:border-blue-700/50 dark:hover:bg-blue-950/30 dark:hover:text-blue-300",
                      )}
                    >
                      <Icon className="mr-3 h-4 w-4" />
                      <div className="text-left">
                        <div className="text-sm font-medium">{item.label}</div>
                        <div className="text-xs text-slate-500 dark:text-slate-400">
                          {item.description}
                        </div>
                      </div>
                    </Button>
                  </Link>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
