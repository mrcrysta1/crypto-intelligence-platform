"""Demo news provider with realistic crypto headlines."""

from app.providers.base import NewsProvider

DEMO_NEWS = [
    {"title": "Bitcoin ETF inflows exceed $500M for third consecutive day", "source": "CryptoNews", "sentiment": 0.85, "impact": "high", "related_assets": ["BTC"], "published_at": "2026-08-24T00:30:00Z"},
    {"title": "Ethereum Layer 2 TVL reaches new all-time high", "source": "DeFi Pulse", "sentiment": 0.72, "impact": "high", "related_assets": ["ETH"], "published_at": "2026-08-24T00:15:00Z"},
    {"title": "SEC delays decision on Solana ETF application", "source": "Reuters", "sentiment": -0.15, "impact": "medium", "related_assets": ["SOL"], "published_at": "2026-08-23T23:45:00Z"},
    {"title": "Major bank announces crypto custody service expansion", "source": "Bloomberg", "sentiment": 0.65, "impact": "high", "related_assets": ["BTC", "ETH"], "published_at": "2026-08-23T23:30:00Z"},
    {"title": "DeFi protocol vulnerability patched before exploit", "source": "The Block", "sentiment": 0.35, "impact": "medium", "related_assets": [], "published_at": "2026-08-23T23:15:00Z"},
    {"title": "Cardano faces declining developer activity", "source": "CryptoSlate", "sentiment": -0.45, "impact": "medium", "related_assets": ["ADA"], "published_at": "2026-08-23T23:00:00Z"},
    {"title": "Solana meme coin craze drives record network fees", "source": "The Block", "sentiment": 0.55, "impact": "medium", "related_assets": ["SOL"], "published_at": "2026-08-23T22:45:00Z"},
    {"title": "Polygon announces major protocol upgrade", "source": "CoinDesk", "sentiment": 0.40, "impact": "medium", "related_assets": ["MATIC"], "published_at": "2026-08-23T22:30:00Z"},
    {"title": "Institutional crypto holdings reach record $150B", "source": "Bloomberg", "sentiment": 0.80, "impact": "high", "related_assets": ["BTC", "ETH"], "published_at": "2026-08-23T22:15:00Z"},
    {"title": "Dogecoin surges on social media hype", "source": "CryptoNews", "sentiment": 0.30, "impact": "low", "related_assets": ["DOGE"], "published_at": "2026-08-23T22:00:00Z"},
]

class DemoNewsProvider(NewsProvider):
    async def get_news(self, query: str = "", limit: int = 20) -> list:
        return DEMO_NEWS[:limit]
