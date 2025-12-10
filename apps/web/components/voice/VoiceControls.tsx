"use client";

import { motion } from 'framer-motion';
import { Mic, MicOff, X } from 'lucide-react';

interface VoiceControlsProps {
  isListening: boolean;
  onStart: () => void;
  onStop: () => void;
}

export function VoiceControls({ isListening, onStart, onStop }: VoiceControlsProps) {
  return (
    <div className="pb-6 md:pb-8 px-4 md:px-6">
      <div className="flex items-center justify-center gap-4 md:gap-6">
        {/* Close Button - Larger touch target */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={onStop}
          className="w-12 h-12 md:w-14 md:h-14 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-white/60 hover:text-white hover:bg-white/20 transition-all"
        >
          <X className="w-5 h-5 md:w-6 md:h-6" />
        </motion.button>

        {/* Main Microphone Button - Minimum 44x44px touch target */}
        <motion.button
          whileTap={{ scale: 0.95 }}
          onClick={isListening ? onStop : onStart}
          className={`w-20 h-20 md:w-24 md:h-24 rounded-full flex items-center justify-center shadow-2xl transition-all ${
            isListening
              ? 'bg-gradient-to-br from-red-500 to-rose-600'
              : 'bg-gradient-to-br from-white to-gray-100'
          }`}
          animate={isListening ? {
            scale: [1, 1.05, 1],
          } : {}}
          transition={{
            duration: 1,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        >
          {isListening ? (
            <MicOff className="w-8 h-8 md:w-10 md:h-10 text-white" />
          ) : (
            <Mic className="w-8 h-8 md:w-10 md:h-10 text-purple-600" />
          )}
        </motion.button>

        {/* Info Button - Larger touch target */}
        <motion.button
          whileTap={{ scale: 0.9 }}
          className="w-12 h-12 md:w-14 md:h-14 rounded-full bg-white/10 backdrop-blur-md flex items-center justify-center text-white/60 hover:text-white hover:bg-white/20 transition-all"
        >
          <span className="text-sm md:text-base font-medium">?</span>
        </motion.button>
      </div>

      {/* Home Indicator */}
      <div className="flex justify-center mt-4 md:mt-6">
        <div className="w-32 h-1.5 bg-white/50 rounded-full" />
      </div>
    </div>
  );
}
