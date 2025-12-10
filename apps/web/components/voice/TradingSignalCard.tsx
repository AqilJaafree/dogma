"use client";

import { motion } from 'framer-motion';

interface TradingSignalCardProps {
  signal: {
    signal: string;
    confidence: number;
    reasoning: string;
    price: number;
    rsi: number;
    sentiment: string;
  };
}

export function TradingSignalCard({ signal }: TradingSignalCardProps) {
  const getSignalColor = () => {
    switch (signal.signal) {
      case 'BUY':
      case 'STRONG_BUY':
        return 'from-green-500 to-emerald-600';
      case 'SELL':
      case 'STRONG_SELL':
        return 'from-red-500 to-rose-600';
      default:
        return 'from-yellow-500 to-orange-500';
    }
  };

  const getSignalEmoji = () => {
    switch (signal.signal) {
      case 'BUY':
      case 'STRONG_BUY':
        return '📈';
      case 'SELL':
      case 'STRONG_SELL':
        return '📉';
      default:
        return '⏸️';
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-black/30 backdrop-blur-xl border border-white/10 rounded-3xl p-4 md:p-6 lg:p-8 shadow-2xl"
    >
      {/* Signal Header */}
      <div className="flex items-center justify-between mb-4 md:mb-6">
        <div className="flex items-center gap-3 md:gap-4">
          <span className="text-3xl md:text-4xl lg:text-5xl">{getSignalEmoji()}</span>
          <div>
            <motion.h3
              initial={{ x: -20, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ delay: 0.2 }}
              className={`text-xl md:text-2xl lg:text-3xl font-bold bg-gradient-to-r ${getSignalColor()} bg-clip-text text-transparent`}
            >
              {signal.signal}
            </motion.h3>
            <p className="text-white/60 text-xs md:text-sm">Trading Signal</p>
          </div>
        </div>

        <div className="text-right">
          <div className="text-2xl md:text-3xl lg:text-4xl font-bold text-white">
            {signal.confidence}%
          </div>
          <div className="text-white/60 text-xs md:text-sm">Confidence</div>
        </div>
      </div>

      {/* Market Data Grid */}
      <div className="grid grid-cols-3 gap-3 md:gap-4 lg:gap-6 mb-4 md:mb-6">
        <div className="bg-white/5 rounded-xl p-3 md:p-4 text-center">
          <div className="text-white/60 text-xs md:text-sm mb-1">Price</div>
          <div className="text-white font-semibold text-sm md:text-base lg:text-lg">
            ${signal.price.toLocaleString()}
          </div>
        </div>
        <div className="bg-white/5 rounded-xl p-3 md:p-4 text-center">
          <div className="text-white/60 text-xs md:text-sm mb-1">RSI</div>
          <div className="text-white font-semibold text-sm md:text-base lg:text-lg">{signal.rsi}</div>
        </div>
        <div className="bg-white/5 rounded-xl p-3 md:p-4 text-center">
          <div className="text-white/60 text-xs md:text-sm mb-1">Sentiment</div>
          <div className="text-white font-semibold capitalize text-sm md:text-base lg:text-lg">
            {signal.sentiment}
          </div>
        </div>
      </div>

      {/* Reasoning */}
      <div className="bg-white/5 rounded-xl p-3 md:p-4 lg:p-5">
        <h4 className="text-white font-medium mb-2 text-sm md:text-base">Analysis</h4>
        <p className="text-white/80 text-sm md:text-base lg:text-lg leading-relaxed">
          {signal.reasoning}
        </p>
      </div>

      {/* Confidence Bar */}
      <div className="mt-4 md:mt-5">
        <div className="flex justify-between text-xs text-white/60 mb-2">
          <span>Confidence Level</span>
          <span>{signal.confidence}%</span>
        </div>
        <div className="h-2 bg-white/10 rounded-full overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${signal.confidence}%` }}
            transition={{ duration: 1, ease: "easeOut" }}
            className={`h-full bg-gradient-to-r ${getSignalColor()}`}
          />
        </div>
      </div>

      {/* Warning */}
      <div className="mt-4 md:mt-5 flex items-start gap-2 md:gap-3 bg-amber-500/10 border border-amber-500/20 rounded-xl p-3 md:p-4">
        <span className="text-amber-500 text-sm md:text-base">⚠️</span>
        <p className="text-amber-200/80 text-xs md:text-sm leading-relaxed">
          This is AI-generated advice. Always do your own research and never invest more than you can afford to lose.
        </p>
      </div>
    </motion.div>
  );
}
