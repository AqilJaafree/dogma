"""
News API Connector

Connector for fetching cryptocurrency news from the custom news API.
Endpoint: https://api-production-729e.up.railway.app/news
"""

import requests
from typing import Dict, List, Optional
import os


class NewsAPIConnector:
    """Connector for custom News API (crypto news sentiment)"""

    def __init__(self, base_url: Optional[str] = None):
        self.base_url = base_url or os.getenv(
            'NEWS_API_URL',
            'https://api-production-729e.up.railway.app/news'
        )

    def get_news(self, page: int = 1) -> Dict:
        """
        Fetch crypto news from the API.

        Args:
            page: Page number for pagination (default: 1)

        Returns:
            Dictionary containing news articles and metadata
        """
        try:
            url = f"{self.base_url}?page={page}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return {"articles": [], "error": str(e)}

    def get_multiple_pages(self, num_pages: int = 3) -> List[Dict]:
        """
        Fetch multiple pages of news articles.

        Args:
            num_pages: Number of pages to fetch (default: 3)

        Returns:
            List of news articles from all pages
        """
        all_articles = []

        for page in range(1, num_pages + 1):
            data = self.get_news(page)
            if "articles" in data:
                all_articles.extend(data["articles"])
            elif "data" in data:
                all_articles.extend(data["data"])
            else:
                # Handle different response formats
                if isinstance(data, list):
                    all_articles.extend(data)

        return all_articles

    def get_latest_news(self, limit: int = 50) -> List[Dict]:
        """
        Fetch the latest news articles.

        Args:
            limit: Maximum number of articles to fetch (default: 50)

        Returns:
            List of latest news articles
        """
        # Fetch enough pages to get desired number of articles
        pages_needed = (limit // 10) + 1  # Assuming ~10 articles per page
        articles = self.get_multiple_pages(num_pages=pages_needed)

        return articles[:limit]
