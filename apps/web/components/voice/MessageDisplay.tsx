"use client";

import { motion } from 'framer-motion';

interface MessageDisplayProps {
  message: string;
  mode: 'listening' | 'thinking' | 'speaking' | 'signal';
}

export function MessageDisplay({ message, mode }: MessageDisplayProps) {
  const getModeIndicator = () => {
    switch (mode) {
      case 'listening':
        return '🎤';
      case 'thinking':
        return '🤔';
      case 'speaking':
        return '💬';
      default:
        return '✨';
    }
  };

  return (
    <motion.div
      className="text-center max-w-sm md:max-w-md lg:max-w-lg px-4 md:px-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
    >
      <motion.p
        className="text-white text-base md:text-lg lg:text-xl font-light leading-relaxed tracking-wide"
        style={{
          textShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
        }}
        key={message}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        {message}
      </motion.p>

      <motion.div
        className="mt-3 md:mt-4 inline-flex items-center gap-2 px-3 md:px-4 py-2 md:py-2.5 bg-white/15 backdrop-blur-md rounded-full"
        initial={{ scale: 0.8, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <span className="text-lg md:text-xl lg:text-2xl">{getModeIndicator()}</span>
        <span className="text-white/90 text-xs md:text-sm lg:text-base font-medium capitalize">
          {mode}
        </span>
      </motion.div>
    </motion.div>
  );
}
