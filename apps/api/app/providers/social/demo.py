"""Demo social provider with synthetic social media data."""

from app.providers.base import SocialProvider

class DemoSocialProvider(SocialProvider):
    async def get_sentiment(self, symbol: str) -> dict:
        sentiments = {
            "BTC": {"score": 0.78, "volume": 15000, "trend": "bullish"},
            "ETH": {"score": 0.72, "volume": 8500, "trend": "bullish"},
            "SOL": {"score": 0.65, "volume": 6200, "trend": "bullish"},
            "DOGE": {"score": 0.45, "volume": 12000, "trend": "mixed"},
            "ADA": {"score": 0.35, "volume": 3200, "trend": "bearish"},
        }
        return sentiments.get(symbol.upper(), {"score": 0.5, "volume": 1000, "trend": "neutral"})

    async def get_social_posts(self, symbol: str, limit: int = 20) -> list:
        return [
            {"platform": "twitter", "content": f"${symbol} looking strong! Technical breakout imminent.", "sentiment": 0.8, "engagement": 2500},
            {"platform": "reddit", "content": f"Bullish on {symbol} long term. DCA every week.", "sentiment": 0.6, "engagement": 1800},
            {"platform": "telegram", "content": f"Whale alert: large {symbol} transfer detected on-chain.", "sentiment": 0.5, "engagement": 3200},
        ][:limit]
