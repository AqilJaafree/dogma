"use client";

import { ReactNode } from 'react';

interface PhoneMockupProps {
  children: ReactNode;
}

export function PhoneMockup({ children }: PhoneMockupProps) {
  return (
    <div className="relative">
      {/* Phone Container */}
      <div className="phone-mockup relative w-[375px] h-[812px] bg-black rounded-[60px] shadow-2xl overflow-hidden">
        {/* Phone Frame */}
        <div className="absolute inset-0 rounded-[60px] shadow-[0_0_0_12px_#1a1a1a,0_0_0_14px_#000,0_20px_60px_rgba(0,0,0,0.6),inset_0_0_6px_rgba(255,255,255,0.1)]" />

        {/* Notch */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[180px] h-[30px] bg-black rounded-b-[20px] z-30">
          {/* Camera */}
          <div className="absolute top-[10px] left-1/2 -translate-x-1/2 w-[60px] h-[6px] bg-slate-900 rounded-full" />
          <div className="absolute top-[8px] left-[30px] w-[10px] h-[10px] bg-slate-800 rounded-full" />
        </div>

        {/* Side Buttons */}
        <div className="absolute left-[-3px] top-[150px] w-[3px] h-[30px] bg-gradient-to-b from-gray-700 to-gray-800 rounded-l" />
        <div className="absolute left-[-3px] top-[190px] w-[3px] h-[60px] bg-gradient-to-b from-gray-700 to-gray-800 rounded-l" />
        <div className="absolute right-[-3px] top-[180px] w-[3px] h-[80px] bg-gradient-to-b from-gray-700 to-gray-800 rounded-r" />

        {/* Screen Content */}
        <div className="relative w-full h-full rounded-[48px] overflow-hidden">
          {children}
        </div>
      </div>

      {/* Glow Effect */}
      <div className="absolute inset-0 -z-10 blur-3xl opacity-30 bg-gradient-to-br from-purple-500 via-blue-500 to-purple-500 animate-pulse" />
    </div>
  );
}
