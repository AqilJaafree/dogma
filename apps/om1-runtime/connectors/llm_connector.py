"""
LLM Connector - Groq and OpenAI Support

Universal connector that supports both Groq and OpenAI APIs.
Groq provides faster inference with compatible OpenAI format.
"""

import os
from typing import Dict, List, Optional
from openai import OpenAI


class LLMConnector:
    """
    Universal LLM connector supporting Groq and OpenAI.

    Groq is recommended for:
    - Faster inference (especially with Llama models)
    - Free tier available
    - OpenAI-compatible API

    Usage:
        # Auto-detect from environment
        llm = LLMConnector()

        # Or specify provider
        llm = LLMConnector(provider='groq')
        llm = LLMConnector(provider='openai')
    """

    def __init__(self, provider: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize LLM connector.

        Args:
            provider: 'groq' or 'openai' (auto-detect if None)
            api_key: API key (auto-detect from env if None)
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'groq')

        if self.provider == 'groq':
            self.api_key = api_key or os.getenv('GROQ_API_KEY')
            self.model = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
            self.base_url = "https://api.groq.com/openai/v1"
        else:  # openai
            self.api_key = api_key or os.getenv('OPENAI_API_KEY')
            self.model = os.getenv('OPENAI_MODEL', 'gpt-4o')
            self.base_url = "https://api.openai.com/v1"

        # Initialize OpenAI client (works for both Groq and OpenAI)
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.2,
        max_tokens: int = 1024,
        **kwargs
    ) -> Dict:
        """
        Create a chat completion.

        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters

        Returns:
            Response dict with 'choices', 'usage', etc.

        Example:
            >>> llm = LLMConnector()
            >>> messages = [
            ...     {"role": "system", "content": "You are a Bitcoin analyst."},
            ...     {"role": "user", "content": "What's the current RSI signal?"}
            ... ]
            >>> response = llm.chat_completion(messages)
            >>> answer = response['choices'][0]['message']['content']
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            # Convert to dict for easier handling
            return {
                'id': response.id,
                'object': response.object,
                'created': response.created,
                'model': response.model,
                'choices': [
                    {
                        'index': choice.index,
                        'message': {
                            'role': choice.message.role,
                            'content': choice.message.content
                        },
                        'finish_reason': choice.finish_reason
                    }
                    for choice in response.choices
                ],
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                }
            }
        except Exception as e:
            print(f"Error in LLM chat completion: {e}")
            return {
                'error': str(e),
                'choices': [{'message': {'content': ''}}]
            }

    def analyze_bitcoin_signal(
        self,
        price: float,
        rsi: float,
        sentiment: float,
        headlines: List[str]
    ) -> str:
        """
        Generate Bitcoin trading signal analysis.

        Args:
            price: Current BTC price
            rsi: RSI value (0-100)
            sentiment: Sentiment score (-1 to 1)
            headlines: Top news headlines

        Returns:
            AI-generated analysis and signal reasoning
        """
        messages = [
            {
                "role": "system",
                "content": """You are an expert Bitcoin trading advisor specializing in RSI technical analysis and news sentiment interpretation.

Key Focus Areas:
- RSI (14-period): Oversold (<30) = potential BUY, Overbought (>70) = potential SELL
- News Sentiment: Positive sentiment = bullish, Negative sentiment = bearish
- Combined Signal: Use both RSI and sentiment to generate confident trading signals

Provide clear, concise analysis with BUY/SELL/HOLD recommendation."""
            },
            {
                "role": "user",
                "content": f"""Analyze Bitcoin and provide a trading signal:

Current Price: ${price:,.2f}
RSI (14): {rsi:.2f}
News Sentiment: {sentiment:.3f} ({'Bullish' if sentiment > 0.2 else 'Bearish' if sentiment < -0.2 else 'Neutral'})

Top Headlines:
{chr(10).join(f"- {h}" for h in headlines[:5])}

Provide:
1. Trading Signal (STRONG BUY / BUY / HOLD / SELL / STRONG SELL)
2. Confidence Score (0-100)
3. Brief reasoning (2-3 sentences)
4. Risk warning"""
            }
        ]

        response = self.chat_completion(
            messages=messages,
            temperature=0.2,
            max_tokens=512
        )

        return response['choices'][0]['message']['content']

    def generate(self, prompt: str, **kwargs) -> str:
        """
        Simple text generation from a prompt.

        Args:
            prompt: The prompt text
            **kwargs: Additional parameters for chat_completion

        Returns:
            Generated text response
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.chat_completion(messages, **kwargs)
        return response['choices'][0]['message']['content']


# Groq Models Available
GROQ_MODELS = {
    'llama-3.3-70b-versatile': {
        'name': 'Llama 3.3 70B Versatile',
        'context': 128000,
        'speed': 'Very Fast',
        'recommended': True
    },
    'llama-3.1-70b-versatile': {
        'name': 'Llama 3.1 70B Versatile',
        'context': 128000,
        'speed': 'Very Fast'
    },
    'mixtral-8x7b-32768': {
        'name': 'Mixtral 8x7B',
        'context': 32768,
        'speed': 'Fast'
    },
    'gemma2-9b-it': {
        'name': 'Gemma 2 9B',
        'context': 8192,
        'speed': 'Ultra Fast'
    }
}
