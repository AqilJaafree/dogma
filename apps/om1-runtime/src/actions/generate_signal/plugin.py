"""
Generate Signal Action Plugin

Uses LLM to generate trading signals based on market data.
"""

from typing import Dict, Any
import sys
from pathlib import Path
import os

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from connectors.llm_connector import LLMConnector


class GenerateSignalAction:
    """
    Action plugin for generating trading signals using LLM.

    Analyzes Bitcoin price, RSI, and news sentiment to produce
    actionable trading recommendations.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize signal generation action.

        Args:
            config: Configuration dict (currently unused)
        """
        self.config = config
        self.llm = LLMConnector(
            provider=os.getenv('LLM_PROVIDER', 'groq'),
            api_key=os.getenv('GROQ_API_KEY')
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate trading signal from context.

        Args:
            context: Dict with:
                - inputs: Dict of input data (bitcoin_price, news_sentiment)
                - timestamp: ISO timestamp
                - cycle: Cycle number

        Returns:
            Dict with signal details
        """
        signal_data = context.get('signal', {})
        inputs = context.get('inputs', {})

        # Log the signal
        print(f"\n{'='*60}")
        print(f"📊 TRADING SIGNAL GENERATED")
        print(f"{'='*60}")
        print(f"🎯 Signal: {signal_data.get('signal', 'UNKNOWN')}")
        print(f"📈 Confidence: {signal_data.get('confidence', 0)}%")
        print(f"💭 Reasoning: {signal_data.get('reasoning', 'N/A')}")
        print(f"{'='*60}\n")

        # In a real implementation, this would:
        # - Store signal in database
        # - Send to trading platform
        # - Update portfolio state

        return {
            'success': True,
            'signal': signal_data
        }
