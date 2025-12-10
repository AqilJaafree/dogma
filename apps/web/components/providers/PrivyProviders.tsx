"use client";

// Temporarily disabled for build testing
// import { PrivyProvider } from "@privy-io/react-auth";

interface PrivyProvidersProps {
  children: React.ReactNode;
}

export function PrivyProviders({ children }: PrivyProvidersProps) {
  // Temporarily disabled Privy
  return <>{children}</>;
}
