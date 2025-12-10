"""
News Sentiment Analysis Utilities

VADER-based sentiment analysis for cryptocurrency news headlines.
Uses the News API: https://api-production-729e.up.railway.app/news
"""

from typing import List, Dict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    """Sentiment analyzer using VADER."""

    def __init__(self):
        """Initialize VADER sentiment analyzer."""
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> float:
        """
        Analyze sentiment of a single text using VADER.

        Args:
            text: News headline or article text

        Returns:
            Sentiment score (-1.0 to 1.0)
        """
        if not text:
            return 0.0

        scores = self.analyzer.polarity_scores(text)
        return scores['compound']

    def analyze_bulk(self, articles: List[Dict]) -> float:
        """
        Calculate aggregate sentiment from multiple articles.

        Args:
            articles: List of article dictionaries
                     Expected format: [{"title": "...", "description": "...", ...}, ...]

        Returns:
            Aggregate sentiment score (-1.0 to 1.0)
        """
        if not articles:
            return 0.0

        scores = []
        for article in articles:
            text = f"{article.get('title', '')} {article.get('description', '')}"
            score = self.analyze(text)
            scores.append(score)

        return sum(scores) / len(scores) if scores else 0.0


def analyze_sentiment(text: str) -> float:
    """
    Analyze sentiment of a single text using VADER.

    Args:
        text: News headline or article text

    Returns:
        Sentiment score (-1.0 to 1.0)
    """
    analyzer = SentimentAnalyzer()
    return analyzer.analyze(text)


def aggregate_sentiment(articles: List[Dict]) -> Dict:
    """
    Calculate aggregate sentiment from multiple articles.

    Args:
        articles: List of article dictionaries from News API
                 Expected format: [{"title": "...", "description": "...", ...}, ...]

    Returns:
        Dictionary with sentiment score and statistics
    """
    analyzer = SentimentAnalyzer()
    score = analyzer.analyze_bulk(articles)

    # Count sentiment types
    positive_count = sum(1 for a in articles if analyzer.analyze(f"{a.get('title', '')} {a.get('description', '')}") > 0.2)
    negative_count = sum(1 for a in articles if analyzer.analyze(f"{a.get('title', '')} {a.get('description', '')}") < -0.2)
    neutral_count = len(articles) - positive_count - negative_count

    return {
        'sentiment_score': score,
        'sentiment_label': interpret_sentiment(score),
        'article_count': len(articles),
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count
    }


def interpret_sentiment(score: float) -> str:
    """
    Interpret sentiment score into label.

    Args:
        score: Sentiment score (-1.0 to 1.0)

    Returns:
        'bearish', 'neutral', or 'bullish'
    """
    if score > 0.2:
        return 'bullish'
    elif score < -0.2:
        return 'bearish'
    else:
        return 'neutral'
