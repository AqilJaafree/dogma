"""
News Sentiment Input Plugin

Fetches crypto news and analyzes sentiment using VADER.
"""

from typing import Dict, Any, List
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from connectors.news_api_connector import NewsAPIConnector
from utils.sentiment import SentimentAnalyzer


class NewsSentimentInput:
    """
    Input plugin for news sentiment analysis.

    Fetches latest crypto news and calculates aggregate sentiment score.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize news sentiment input.

        Args:
            config: Configuration dict with:
                - news_limit: Number of articles to analyze (default: 50)
                - sentiment_threshold: Threshold for bullish/bearish (default: 0.2)
        """
        self.config = config
        self.news_limit = config.get('news_limit', 50)
        self.sentiment_threshold = config.get('sentiment_threshold', 0.2)

        self.news_connector = NewsAPIConnector()
        self.sentiment_analyzer = SentimentAnalyzer()

    def fetch(self) -> Dict[str, Any]:
        """
        Fetch news and analyze sentiment.

        Returns:
            Dict with:
                - sentiment_score: Aggregate sentiment score (-1 to 1)
                - sentiment_label: 'bullish', 'neutral', or 'bearish'
                - news_count: Number of articles analyzed
                - latest_headlines: List of recent headlines
                - positive_count: Number of positive articles
                - negative_count: Number of negative articles
                - neutral_count: Number of neutral articles
        """
        # Fetch latest news
        articles = self.news_connector.get_latest_news(limit=self.news_limit)

        if not articles:
            return {
                'sentiment_score': 0.0,
                'sentiment_label': 'neutral',
                'news_count': 0,
                'latest_headlines': [],
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'error': 'No news articles fetched'
            }

        # Analyze sentiment for all articles
        sentiments = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for article in articles:
            # Combine title and description for sentiment analysis
            text = f"{article.get('title', '')} {article.get('description', '')}"
            sentiment = self.sentiment_analyzer.analyze(text)
            sentiments.append(sentiment)

            # Count sentiment types
            if sentiment > self.sentiment_threshold:
                positive_count += 1
            elif sentiment < -self.sentiment_threshold:
                negative_count += 1
            else:
                neutral_count += 1

        # Calculate aggregate sentiment
        if sentiments:
            aggregate_sentiment = sum(sentiments) / len(sentiments)
        else:
            aggregate_sentiment = 0.0

        # Interpret sentiment label
        sentiment_label = self._interpret_sentiment(aggregate_sentiment)

        # Extract latest headlines
        latest_headlines = [
            article.get('title', 'No title')
            for article in articles[:5]
        ]

        return {
            'sentiment_score': aggregate_sentiment,
            'sentiment_label': sentiment_label,
            'news_count': len(articles),
            'latest_headlines': latest_headlines,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count
        }

    def _interpret_sentiment(self, score: float) -> str:
        """
        Interpret sentiment score into label.

        Args:
            score: Sentiment score (-1 to 1)

        Returns:
            'bullish', 'neutral', or 'bearish'
        """
        if score > self.sentiment_threshold:
            return 'bullish'
        elif score < -self.sentiment_threshold:
            return 'bearish'
        else:
            return 'neutral'
