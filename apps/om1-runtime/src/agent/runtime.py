"""
Bitcoin Advisor Agent Runtime

Core agent orchestration logic inspired by OM1 patterns.
Manages inputs, LLM cortex, and actions in a periodic loop.
"""

import time
import json
import os
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

class BitcoinAdvisorAgent:
    """
    Lightweight agent runtime for Bitcoin trading signals.

    Inspired by OM1 architecture:
    - Inputs: Fetch data from external sources (BTC price, news)
    - Cortex: LLM-based decision making
    - Actions: Execute trading operations (signals, alerts)
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize agent with configuration.

        Args:
            config: Agent configuration dict with inputs, actions, LLM settings
        """
        self.config = config
        self.name = config.get('name', 'bitcoin_advisor')
        self.description = config.get('description', 'AI trading agent')
        self.interval = config.get('interval', 60)  # seconds between cycles

        print(f"🤖 Initializing {self.name}")
        print(f"📝 Description: {self.description}")
        print(f"⏱️  Interval: {self.interval}s")

        # Load plugins
        self.inputs = self._load_inputs(config.get('inputs', []))
        self.actions = self._load_actions(config.get('actions', []))

        # Initialize LLM connector
        self.llm = self._init_llm(config.get('llm', {}))

        # Agent state
        self.running = False
        self.cycle_count = 0
        self.last_signal = None

        print(f"✅ Agent initialized successfully")
        print(f"   Inputs: {len(self.inputs)}")
        print(f"   Actions: {len(self.actions)}")
        print()

    def _load_inputs(self, inputs_config: List[Dict]) -> Dict[str, Any]:
        """Dynamically load input plugins."""
        inputs = {}

        for input_cfg in inputs_config:
            name = input_cfg['name']
            class_name = input_cfg['class']
            config = input_cfg.get('config', {})

            print(f"  📥 Loading input: {name} ({class_name})")

            # Dynamic import
            module_path = f"src.inputs.{name}.plugin"
            try:
                module = __import__(module_path, fromlist=[class_name])
                InputClass = getattr(module, class_name)
                inputs[name] = InputClass(config)
            except Exception as e:
                print(f"     ⚠️  Failed to load {name}: {e}")
                # Create stub for now
                inputs[name] = None

        return inputs

    def _load_actions(self, actions_config: List[Dict]) -> Dict[str, Any]:
        """Dynamically load action plugins."""
        actions = {}

        for action_cfg in actions_config:
            name = action_cfg['name']
            class_name = action_cfg['class']
            config = action_cfg.get('config', {})

            print(f"  ⚡ Loading action: {name} ({class_name})")

            # Dynamic import
            module_path = f"src.actions.{name}.plugin"
            try:
                module = __import__(module_path, fromlist=[class_name])
                ActionClass = getattr(module, class_name)
                actions[name] = ActionClass(config)
            except Exception as e:
                print(f"     ⚠️  Failed to load {name}: {e}")
                # Create stub for now
                actions[name] = None

        return actions

    def _init_llm(self, llm_config: Dict) -> Any:
        """Initialize LLM connector."""
        provider = llm_config.get('provider', 'groq')
        print(f"  🧠 Initializing LLM: {provider}")

        try:
            from connectors.llm_connector import LLMConnector
            return LLMConnector(
                provider=provider,
                api_key=os.getenv(llm_config.get('api_key', '').replace('${', '').replace('}', ''))
            )
        except Exception as e:
            print(f"     ⚠️  Failed to initialize LLM: {e}")
            return None

    def _collect_inputs(self) -> Dict[str, Any]:
        """
        Fetch data from all input plugins.

        Returns:
            Dict mapping input name to fetched data
        """
        input_data = {}

        for name, input_plugin in self.inputs.items():
            if input_plugin is None:
                continue

            try:
                print(f"  📥 Fetching {name}...", end=" ")
                data = input_plugin.fetch()
                input_data[name] = data
                print(f"✅")
            except Exception as e:
                print(f"❌ Error: {e}")
                input_data[name] = {'error': str(e)}

        return input_data

    def _generate_signal(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading signal using LLM.

        Args:
            input_data: Data from all inputs

        Returns:
            Signal dict with recommendation, confidence, reasoning
        """
        if self.llm is None:
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'reasoning': 'LLM not available'
            }

        # Build context for LLM
        btc_data = input_data.get('bitcoin_price', {})
        sentiment = input_data.get('news_sentiment', {})

        if 'error' in btc_data or 'error' in sentiment:
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'reasoning': 'Insufficient data'
            }

        prompt = self._build_prompt(btc_data, sentiment)

        try:
            print(f"  🧠 Generating signal with LLM...", end=" ")
            response = self.llm.generate(prompt)
            signal = self._parse_signal_response(response)
            print(f"✅ {signal['signal']} ({signal['confidence']}%)")
            return signal
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                'signal': 'HOLD',
                'confidence': 0,
                'reasoning': f'LLM error: {str(e)}'
            }

    def _build_prompt(self, btc_data: Dict, sentiment: Dict) -> str:
        """Build prompt for LLM signal generation."""
        return f"""
Analyze the following Bitcoin market data and provide a trading signal.

PRICE DATA:
- Current Price: ${btc_data.get('price', 0):,.2f}
- 24h Change: {btc_data.get('price_change_24h', 0):.2f}%
- RSI (14-period): {btc_data.get('rsi', 50):.2f}
- RSI Signal: {btc_data.get('rsi_signal', 'neutral')}
- Volume 24h: ${btc_data.get('volume_24h', 0):,.0f}
- Data Source: {btc_data.get('source', 'unknown')}

SENTIMENT DATA:
- Sentiment Score: {sentiment.get('sentiment_score', 0):.2f}
- Sentiment Label: {sentiment.get('sentiment_label', 'neutral')}
- News Articles Analyzed: {sentiment.get('news_count', 0)}
- Latest Headlines:
{chr(10).join(f"  • {h}" for h in sentiment.get('latest_headlines', [])[:3])}

INSTRUCTIONS:
Based on the technical indicators (RSI) and news sentiment, provide a clear trading recommendation.

Respond in this exact format:
SIGNAL: [BUY/SELL/HOLD/STRONG_BUY/STRONG_SELL]
CONFIDENCE: [0-100]
REASONING: [2-3 sentences explaining your decision]

Consider:
- RSI < 30 = oversold (potential buy)
- RSI > 70 = overbought (potential sell)
- Positive sentiment + good technicals = stronger buy signal
- Negative sentiment + poor technicals = stronger sell signal
""".strip()

    def _parse_signal_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured signal."""
        lines = response.strip().split('\n')
        signal_data = {
            'signal': 'HOLD',
            'confidence': 50,
            'reasoning': 'Unable to parse LLM response'
        }

        for line in lines:
            line = line.strip()
            if line.startswith('SIGNAL:'):
                signal_data['signal'] = line.split(':', 1)[1].strip()
            elif line.startswith('CONFIDENCE:'):
                try:
                    signal_data['confidence'] = int(line.split(':', 1)[1].strip())
                except:
                    signal_data['confidence'] = 50
            elif line.startswith('REASONING:'):
                signal_data['reasoning'] = line.split(':', 1)[1].strip()

        return signal_data

    def _execute_actions(self, signal: Dict[str, Any], input_data: Dict[str, Any]):
        """
        Execute all actions with the generated signal.

        Args:
            signal: Trading signal from LLM
            input_data: Raw input data for context
        """
        context = {
            'signal': signal,
            'inputs': input_data,
            'timestamp': datetime.now().isoformat(),
            'cycle': self.cycle_count
        }

        for name, action_plugin in self.actions.items():
            if action_plugin is None:
                continue

            try:
                print(f"  ⚡ Executing action: {name}...", end=" ")
                result = action_plugin.execute(context)
                print(f"✅")
            except Exception as e:
                print(f"❌ Error: {e}")

    def run_cycle(self):
        """Execute one agent cycle."""
        self.cycle_count += 1

        print(f"\n{'='*60}")
        print(f"🔄 Cycle #{self.cycle_count} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")

        # 1. Collect inputs
        print("📊 Collecting input data...")
        input_data = self._collect_inputs()
        print()

        # 2. Generate signal
        print("🎯 Generating trading signal...")
        signal = self._generate_signal(input_data)
        self.last_signal = signal
        print()

        # 3. Execute actions
        print("⚡ Executing actions...")
        self._execute_actions(signal, input_data)
        print()

        print(f"✅ Cycle #{self.cycle_count} complete\n")

    def run(self):
        """Main agent loop."""
        self.running = True

        print(f"🚀 Starting {self.name} agent loop...")
        print(f"⏱️  Interval: {self.interval} seconds")
        print(f"🛑 Press Ctrl+C to stop\n")

        try:
            while self.running:
                self.run_cycle()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping agent...")
            self.running = False
        except Exception as e:
            print(f"\n\n❌ Fatal error: {e}")
            self.running = False

        print(f"👋 Agent stopped after {self.cycle_count} cycles")

    def stop(self):
        """Stop the agent loop."""
        self.running = False
