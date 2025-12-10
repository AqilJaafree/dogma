"use client";

import { useEffect, useState } from 'react';
import { Battery, Signal, Wifi } from 'lucide-react';

export function StatusBar() {
  const [currentTime, setCurrentTime] = useState('9:41');

  useEffect(() => {
    // Update time only on client side to avoid hydration mismatch
    const updateTime = () => {
      const time = new Date().toLocaleTimeString('en-US', {
        hour: 'numeric',
        minute: '2-digit',
        hour12: false
      });
      setCurrentTime(time);
    };

    updateTime();
    const interval = setInterval(updateTime, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="relative z-20 flex items-center justify-between px-4 md:px-6 lg:px-8 pt-2 md:pt-3 pb-2">
      <div className="text-white font-semibold text-xs md:text-sm lg:text-base tracking-tight" suppressHydrationWarning>
        {currentTime}
      </div>

      <div className="flex items-center gap-1 md:gap-1.5 lg:gap-2">
        <Signal className="w-3 h-3 md:w-4 md:h-4 text-white" strokeWidth={2.5} />
        <Wifi className="w-3 h-3 md:w-4 md:h-4 text-white" strokeWidth={2.5} />
        <Battery className="w-4 h-4 md:w-5 md:h-5 text-white" strokeWidth={2.5} />
      </div>
    </div>
  );
}
