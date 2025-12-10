/**
 * OM1 Integration Types
 *
 * TypeScript types for OM1 agent communication
 */

export interface BitcoinAnalysis {
  price: number;
  price_change_24h: number;
  rsi: number;
  rsi_signal: 'oversold' | 'neutral' | 'overbought';
  sentiment: number;
  sentiment_label: 'bearish' | 'neutral' | 'bullish';
  signal: 'STRONG BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG SELL';
  confidence: number;
  reasoning: string;
  timestamp: string;
}

export interface TradingSignal {
  signal: 'STRONG BUY' | 'BUY' | 'HOLD' | 'SELL' | 'STRONG SELL';
  rsi: number;
  sentiment: number;
  price: number;
  reasoning: string;
  timestamp: string;
}

export interface AgentUpdate {
  type: 'signal_alert' | 'price_update' | 'sentiment_update';
  data: any;
  timestamp: string;
}
