/**
 * Bitcoin Advisor Agent API Client
 *
 * Connects Next.js frontend to the Bitcoin advisor agent runtime
 */

const AGENT_API_URL = process.env.NEXT_PUBLIC_AGENT_API_URL || 'http://localhost:8000';

export interface BitcoinSignal {
  signal: 'BUY' | 'SELL' | 'HOLD' | 'STRONG_BUY' | 'STRONG_SELL';
  confidence: number;
  reasoning: string;
  data: {
    btc_price: number;
    rsi: number;
    sentiment: string;
  };
  timestamp: string;
}

export interface AgentStatus {
  running: boolean;
  cycle_count: number;
  last_signal?: BitcoinSignal;
}

/**
 * Fetch the latest trading signal from the agent
 */
export async function fetchTradingSignal(): Promise<BitcoinSignal> {
  try {
    const response = await fetch(`${AGENT_API_URL}/api/signal`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      cache: 'no-store', // Always get fresh data
    });

    if (!response.ok) {
      throw new Error(`Agent API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch trading signal:', error);
    throw error;
  }
}

/**
 * Trigger a new analysis cycle in the agent
 */
export async function triggerAnalysis(): Promise<BitcoinSignal> {
  try {
    const response = await fetch(`${AGENT_API_URL}/api/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Agent API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to trigger analysis:', error);
    throw error;
  }
}

/**
 * Get agent status
 */
export async function getAgentStatus(): Promise<AgentStatus> {
  try {
    const response = await fetch(`${AGENT_API_URL}/api/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Agent API error: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to get agent status:', error);
    throw error;
  }
}

/**
 * Check if agent is available
 */
export async function checkAgentHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${AGENT_API_URL}/health`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000), // 5 second timeout
    });

    return response.ok;
  } catch (error) {
    console.error('Agent health check failed:', error);
    return false;
  }
}
