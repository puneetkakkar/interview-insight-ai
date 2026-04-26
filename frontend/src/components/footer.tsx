interface FooterProps {
  className?: string;
}

export function Footer({ className = "" }: FooterProps) {
  return (
    <footer
      className={`mt-10 border-t border-white/10 py-6 text-center text-xs text-white/50 ${className}`}
    >
      CandidateSignal — Crafted for clarity
    </footer>
  );
}
