"use client";

import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { User } from 'lucide-react';

interface ProfileGreetingProps {
  name: string;
}

export function ProfileGreeting({ name }: ProfileGreetingProps) {
  const [greeting, setGreeting] = useState('Hello');

  useEffect(() => {
    // Calculate greeting only on client side to avoid hydration mismatch
    const hour = new Date().getHours();
    if (hour < 12) {
      setGreeting('Good Morning');
    } else if (hour < 18) {
      setGreeting('Good Afternoon');
    } else {
      setGreeting('Good Evening');
    }
  }, []);

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      className="flex items-center gap-4 mb-6"
    >
      <div className="w-12 h-12 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border-2 border-white/30">
        <User className="w-6 h-6 text-white" />
      </div>

      <div>
        <div className="text-white/80 text-sm font-light tracking-wide" suppressHydrationWarning>
          {greeting},
        </div>
        <div className="text-white text-2xl font-semibold -tracking-tight">
          {name}
        </div>
      </div>
    </motion.div>
  );
}
