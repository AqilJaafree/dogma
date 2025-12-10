"use client";

import { useState, useEffect } from 'react';
import { AIOrb } from './AIOrb';
import { VoiceControls } from './VoiceControls';
import { MessageDisplay } from './MessageDisplay';
import { StatusBar } from './StatusBar';
import { ProfileGreeting } from './ProfileGreeting';
import { TradingSignalCard } from './TradingSignalCard';
// import { WalletButton } from '../wallet/WalletButton'; // Temporarily disabled for build test

type ViewMode = 'listening' | 'thinking' | 'speaking' | 'signal';

interface BitcoinSignal {
  signal: string;
  confidence: number;
  reasoning: string;
  price: number;
  rsi: number;
  sentiment: string;
}

export function VoiceInterface() {
  const [viewMode, setViewMode] = useState<ViewMode>('listening');
  const [message, setMessage] = useState("Tap to ask about Bitcoin...");
  const [currentSignal, setCurrentSignal] = useState<BitcoinSignal | null>(null);
  const [isListening, setIsListening] = useState(false);
  const [isLandscape, setIsLandscape] = useState(false);

  // Detect landscape orientation
  useEffect(() => {
    const checkOrientation = () => {
      setIsLandscape(window.innerHeight < window.innerWidth && window.innerWidth < 1024);
    };
    checkOrientation();
    window.addEventListener('resize', checkOrientation);
    return () => window.removeEventListener('resize', checkOrientation);
  }, []);

  // Simulate voice interaction (replace with actual Web Speech API)
  const handleVoiceStart = () => {
    setIsListening(true);
    setViewMode('listening');
    setMessage("Listening...");

    // Simulate user asking question
    setTimeout(() => {
      setMessage("What's the current Bitcoin trading signal?");
      setViewMode('thinking');

      // Simulate API call to Bitcoin advisor agent
      setTimeout(() => {
        fetchTradingSignal();
      }, 2000);
    }, 2000);
  };

  const fetchTradingSignal = async () => {
    setViewMode('thinking');
    setMessage("Analyzing Bitcoin market data...");

    try {
      // Import the API client dynamically
      const { triggerAnalysis } = await import('@/lib/api/bitcoin-agent');

      // Fetch from real Bitcoin advisor agent
      const data = await triggerAnalysis();

      const signal: BitcoinSignal = {
        signal: data.signal,
        confidence: data.confidence,
        reasoning: data.reasoning,
        price: data.data.btc_price || 0,
        rsi: data.data.rsi || 50.0,
        sentiment: data.data.sentiment || 'neutral'
      };

      setCurrentSignal(signal);
      setViewMode('signal');
      setMessage(`Based on current analysis, I recommend: ${signal.signal}`);
      setIsListening(false);
    } catch (error) {
      console.error('Failed to fetch signal:', error);
      setViewMode('listening');
      setMessage("Sorry, I couldn't analyze the market right now. Please try again.");
      setIsListening(false);

      // Optionally show demo data as fallback
      // const demoSignal: BitcoinSignal = { ... };
      // setCurrentSignal(demoSignal);
    }
  };

  const handleReset = () => {
    setViewMode('listening');
    setMessage("Tap to ask about Bitcoin...");
    setCurrentSignal(null);
    setIsListening(false);
  };

  return (
    <div className="voice-interface relative w-full h-screen bg-gradient-to-b from-purple-500 via-purple-600 to-blue-600 overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0 bg-gradient-to-br from-purple-500/20 via-transparent to-blue-500/20 pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_20%_30%,rgba(168,85,247,0.3),transparent_50%)] pointer-events-none" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_80%_70%,rgba(59,130,246,0.3),transparent_50%)] pointer-events-none" />

      {/* Header: Status Bar */}
      {!isLandscape && (
        <div className="relative z-20">
          <StatusBar />
        </div>
      )}

      {/* Main Content */}
      <div className="relative z-10 flex flex-col h-full">
        {viewMode === 'signal' && currentSignal ? (
          // Signal View with Card
          <div className="flex-1 flex flex-col justify-between p-4 md:p-6 lg:p-8 max-w-4xl mx-auto w-full">
            <ProfileGreeting name="Trader" />

            <div className="space-y-4 md:space-y-6">
              {/* Wallet Button - Centered */}
              {/* <div className="flex justify-center">
                <WalletButton />
              </div> */}

              <TradingSignalCard signal={currentSignal} />

              <button
                onClick={handleReset}
                className="w-full py-3 md:py-4 bg-white/10 backdrop-blur-md rounded-2xl text-white font-medium hover:bg-white/20 transition-all text-base md:text-lg"
              >
                Ask Another Question
              </button>
            </div>

            <div className="flex justify-center pb-4 md:pb-6">
              <div className="w-32 h-1.5 bg-white/50 rounded-full" />
            </div>
          </div>
        ) : (
          // Voice Interaction View
          <>
            <div className={`flex-1 flex ${isLandscape ? 'flex-row' : 'flex-col'} items-center justify-center px-4 md:px-8 lg:px-12 gap-6 md:gap-8`}>
              <MessageDisplay
                message={message}
                mode={viewMode}
              />

              <AIOrb
                isActive={isListening}
                mode={viewMode}
              />
            </div>

            {/* Wallet Button - Centered */}
            {/* <div className="flex justify-center pb-6 md:pb-8">
              <WalletButton />
            </div> */}

            <VoiceControls
              isListening={isListening}
              onStart={handleVoiceStart}
              onStop={handleReset}
            />
          </>
        )}
      </div>
    </div>
  );
}
