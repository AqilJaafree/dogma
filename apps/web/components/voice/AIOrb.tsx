"use client";

import { motion } from 'framer-motion';

interface AIOrbProps {
  isActive: boolean;
  mode: 'listening' | 'thinking' | 'speaking' | 'signal';
}

export function AIOrb({ isActive, mode }: AIOrbProps) {
  const getOrbAnimation = () => {
    switch (mode) {
      case 'listening':
        return {
          scale: [1, 1.1, 1],
          rotate: [0, 360],
        };
      case 'thinking':
        return {
          scale: [1, 1.05, 1],
          opacity: [1, 0.8, 1],
        };
      case 'speaking':
        return {
          scale: [1, 1.15, 1, 1.05, 1],
        };
      default:
        return {};
    }
  };

  return (
    <div className="relative w-32 h-32 md:w-40 md:h-40 lg:w-48 lg:h-48 my-8 md:my-10 lg:my-12">
      {/* Outer Glow */}
      <motion.div
        className="absolute inset-0 rounded-full blur-3xl md:blur-[64px] opacity-60"
        style={{
          background: 'radial-gradient(circle, rgba(139,92,246,0.6), rgba(59,130,246,0.4))',
        }}
        animate={isActive ? {
          scale: [1, 1.3, 1],
          opacity: [0.6, 0.8, 0.6],
        } : {}}
        transition={{
          duration: 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Main Orb */}
      <motion.div
        className="absolute inset-0 rounded-full"
        style={{
          background: 'linear-gradient(135deg, #3B82F6, #8B5CF6)',
          boxShadow: `
            0 0 60px rgba(139, 92, 246, 0.6),
            0 0 120px rgba(59, 130, 246, 0.4),
            inset 0 0 30px rgba(255, 255, 255, 0.2)
          `,
        }}
        animate={isActive ? getOrbAnimation() : {}}
        transition={{
          duration: mode === 'listening' ? 4 : 2,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Inner Glow */}
      <motion.div
        className="absolute inset-2 rounded-full blur-md"
        style={{
          background: 'linear-gradient(135deg, #60A5FA, #A78BFA)',
        }}
        animate={isActive ? {
          opacity: [0.6, 1, 0.6],
        } : {}}
        transition={{
          duration: 1.5,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      />

      {/* Pulsing Rings */}
      {isActive && mode === 'listening' && (
        <>
          {[0, 1, 2].map((i) => (
            <motion.div
              key={i}
              className="absolute inset-0 rounded-full border-2 md:border-3 lg:border-4 border-white/30"
              initial={{ scale: 1, opacity: 0.8 }}
              animate={{
                scale: [1, 1.5, 2],
                opacity: [0.8, 0.3, 0],
              }}
              transition={{
                duration: 2,
                repeat: Infinity,
                delay: i * 0.6,
                ease: "easeOut"
              }}
            />
          ))}
        </>
      )}

      {/* Center Dot for Speaking Mode */}
      {mode === 'speaking' && (
        <motion.div
          className="absolute inset-0 m-auto w-4 h-4 md:w-5 md:h-5 lg:w-6 lg:h-6 rounded-full bg-white"
          animate={{
            scale: [1, 1.5, 1],
            opacity: [1, 0.6, 1],
          }}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      )}
    </div>
  );
}
