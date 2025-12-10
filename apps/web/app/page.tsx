"use client";

import { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues
const VoiceInterface = dynamic(
  () => import('@/components/voice/VoiceInterface').then(mod => ({ default: mod.VoiceInterface })),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center">
        <div className="text-white text-xl animate-pulse">Loading Voice Interface...</div>
      </div>
    ),
  }
);

export default function Home() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center p-4">
        <div className="text-white text-xl animate-pulse">Initializing...</div>
      </main>
    );
  }

  return (
    <main className="min-h-screen w-full bg-gradient-to-br from-slate-950 via-purple-950 to-slate-950 flex items-center justify-center">
      <VoiceInterface />
    </main>
  );
}
