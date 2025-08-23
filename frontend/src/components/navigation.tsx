"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Home, Menu, X } from "lucide-react";
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
    <nav className="bg-background/95 shadow-elegant sticky top-0 z-50 w-full border-b border-white/10 backdrop-blur-xl">
      <div className="container mx-auto px-3 sm:px-4 md:px-6">
        <div className="flex h-12 items-center justify-between sm:h-14">
          {/* Logo/Brand */}
          <div className="group flex items-center space-x-2 sm:space-x-3">
            <div className="sm:block">
              <h1 className="text-foreground text-sm font-semibold transition-colors duration-300 sm:text-base">
                FRAI AI
              </h1>
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
                      "relative h-9 px-3 font-medium transition-all duration-200",
                      isActive
                        ? "bg-foreground text-background hover:bg-foreground/90 shadow-elegant"
                        : "text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:border-border/30 border border-transparent",
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
              className="text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:border-border/30 h-8 w-8 border border-transparent p-0 transition-all duration-200 sm:h-9 sm:w-9 md:hidden"
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
          <div className="bg-background/95 shadow-elegant border-t border-white/10 backdrop-blur-xl">
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
                        "h-10 w-full justify-start px-3 font-medium transition-all duration-200 sm:h-11 sm:px-4",
                        isActive
                          ? "bg-foreground text-background shadow-elegant"
                          : "text-muted-foreground hover:text-foreground hover:bg-accent/50 hover:border-border/30 border border-transparent",
                      )}
                    >
                      <Icon className="mr-3 h-4 w-4" />
                      <div className="text-left">
                        <div className="text-sm font-medium">{item.label}</div>
                        <div className="text-muted-foreground text-xs">
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
