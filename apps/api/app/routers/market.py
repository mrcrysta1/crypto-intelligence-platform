from fastapi import APIRouter

router = APIRouter(prefix="/api/market", tags=["market"])

@router.get("/overview")
async def market_overview():
    return {
        "total_market_cap": 2450000000000,
        "total_volume_24h": 98000000000,
        "btc_dominance": 54.2,
        "market_regime": "trending_up",
        "active_assets": 20,
        "long_signals": 7,
        "short_signals": 2,
        "watch_signals": 8,
        "no_trade_signals": 3,
    }

@router.get("/regime")
async def market_regime():
    return {
        "regime": "trending_up",
        "confidence": 0.78,
        "description": "Market showing bullish structure with higher highs and higher lows. BTC leading, alts following.",
        "indicators": {
            "trend_strength": 72,
            "volatility": 45,
            "volume_profile": "above_average",
            "breadth": 65,
        },
    }

@router.get("/trending")
async def trending_assets():
    return {
        "gainers": [
            {"symbol": "SHIB", "change24h": 12.56, "price": 0.00002345},
            {"symbol": "DOGE", "change24h": 8.34, "price": 0.1567},
            {"symbol": "SOL", "change24h": 5.67, "price": 178.92},
            {"symbol": "NEAR", "change24h": 4.56, "price": 7.89},
            {"symbol": "APT", "change24h": 2.78, "price": 9.45},
        ],
        "losers": [
            {"symbol": "MATIC", "change24h": -3.45, "price": 0.7891},
            {"symbol": "ADA", "change24h": -2.15, "price": 0.5123},
            {"symbol": "FIL", "change24h": -1.56, "price": 6.78},
            {"symbol": "XRP", "change24h": -1.23, "price": 0.6234},
            {"symbol": "DOT", "change24h": -0.89, "price": 8.45},
        ],
    }

@router.get("/whale-activity")
async def whale_activity():
    return {
        "events": [
            {"type": "large_transfer", "asset": "BTC", "amount_usd": 45200000, "from": "0x742d...8f2a", "to": "Coinbase", "timestamp": "2026-08-24T00:45:00Z", "sentiment": "neutral"},
            {"type": "accumulation", "asset": "ETH", "amount_usd": 12800000, "from": "Unknown Wallet", "to": "0x3f5c...9a1b", "timestamp": "2026-08-24T00:32:00Z", "sentiment": "bullish"},
            {"type": "exchange_outflow", "asset": "SOL", "amount_usd": 8500000, "from": "Binance", "to": "0x8d2e...4c7f", "timestamp": "2026-08-24T00:18:00Z", "sentiment": "bullish"},
            {"type": "distribution", "asset": "DOGE", "amount_usd": 5200000, "from": "0x1a3b...7e2d", "to": "Multiple Wallets", "timestamp": "2026-08-24T00:05:00Z", "sentiment": "bearish"},
            {"type": "large_transfer", "asset": "BTC", "amount_usd": 28900000, "from": "0x9f4e...2c8a", "to": "Kraken", "timestamp": "2026-08-23T23:52:00Z", "sentiment": "neutral"},
        ]
    }

@router.get("/news")
async def market_news():
    return {
        "articles": [
            {"title": "Bitcoin ETF inflows exceed $500M for third consecutive day", "source": "CryptoNews", "sentiment": 0.85, "impact": "high", "published_at": "2026-08-24T00:30:00Z", "related_assets": ["BTC"]},
            {"title": "Ethereum Layer 2 TVL reaches new all-time high", "source": "DeFi Pulse", "sentiment": 0.72, "impact": "high", "published_at": "2026-08-24T00:15:00Z", "related_assets": ["ETH"]},
            {"title": "SEC delays decision on Solana ETF application", "source": "Reuters", "sentiment": -0.15, "impact": "medium", "published_at": "2026-08-23T23:45:00Z", "related_assets": ["SOL"]},
            {"title": "Major bank announces crypto custody service expansion", "source": "Bloomberg", "sentiment": 0.65, "impact": "high", "published_at": "2026-08-23T23:30:00Z", "related_assets": ["BTC", "ETH"]},
            {"title": "DeFi protocol vulnerability patched before exploit", "source": "The Block", "sentiment": 0.35, "impact": "medium", "published_at": "2026-08-23T23:15:00Z", "related_assets": []},
        ]
    }
