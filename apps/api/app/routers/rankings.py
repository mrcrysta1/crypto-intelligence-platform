from fastapi import APIRouter

router = APIRouter(prefix="/api/rankings", tags=["rankings"])

RANKINGS = [
    {"rank": 1, "symbol": "BTC", "composite_score": 82, "direction": "LONG", "confidence": 0.87, "price": 67432.18, "change24h": 2.34, "market_cap": 1324000000000},
    {"rank": 2, "symbol": "SOL", "composite_score": 81, "direction": "LONG", "confidence": 0.85, "price": 178.92, "change24h": 5.67, "market_cap": 78000000000},
    {"rank": 3, "symbol": "ETH", "composite_score": 78, "direction": "LONG", "confidence": 0.82, "price": 3521.45, "change24h": 1.87, "market_cap": 423000000000},
    {"rank": 4, "symbol": "AVAX", "composite_score": 64, "direction": "LONG", "confidence": 0.72, "price": 42.67, "change24h": 3.21, "market_cap": 16000000000},
    {"rank": 5, "symbol": "LINK", "composite_score": 65, "direction": "LONG", "confidence": 0.68, "price": 18.92, "change24h": 1.45, "market_cap": 11000000000},
    {"rank": 6, "symbol": "NEAR", "composite_score": 64, "direction": "LONG", "confidence": 0.70, "price": 7.89, "change24h": 4.56, "market_cap": 8200000000},
    {"rank": 7, "symbol": "BNB", "composite_score": 64, "direction": "WATCH", "confidence": 0.61, "price": 598.32, "change24h": -0.45, "market_cap": 92000000000},
    {"rank": 8, "symbol": "UNI", "composite_score": 60, "direction": "WATCH", "confidence": 0.62, "price": 12.34, "change24h": 2.12, "market_cap": 9500000000},
    {"rank": 9, "symbol": "DOGE", "composite_score": 56, "direction": "WATCH", "confidence": 0.58, "price": 0.1567, "change24h": 8.34, "market_cap": 22000000000},
    {"rank": 10, "symbol": "APT", "composite_score": 56, "direction": "WATCH", "confidence": 0.58, "price": 9.45, "change24h": 2.78, "market_cap": 4100000000},
    {"rank": 11, "symbol": "DOT", "composite_score": 54, "direction": "WATCH", "confidence": 0.54, "price": 8.45, "change24h": -0.89, "market_cap": 12000000000},
    {"rank": 12, "symbol": "ATOM", "composite_score": 53, "direction": "WATCH", "confidence": 0.55, "price": 11.23, "change24h": 1.89, "market_cap": 4300000000},
    {"rank": 13, "symbol": "XRP", "composite_score": 53, "direction": "WATCH", "confidence": 0.52, "price": 0.6234, "change24h": -1.23, "market_cap": 34000000000},
    {"rank": 14, "symbol": "ARB", "composite_score": 51, "direction": "WATCH", "confidence": 0.52, "price": 1.23, "change24h": -0.89, "market_cap": 3800000000},
    {"rank": 15, "symbol": "SHIB", "composite_score": 50, "direction": "WATCH", "confidence": 0.48, "price": 0.00002345, "change24h": 12.56, "market_cap": 14000000000},
    {"rank": 16, "symbol": "LTC", "composite_score": 49, "direction": "WATCH", "confidence": 0.50, "price": 87.23, "change24h": 0.34, "market_cap": 6500000000},
    {"rank": 17, "symbol": "ADA", "composite_score": 47, "direction": "SHORT", "confidence": 0.65, "price": 0.5123, "change24h": -2.15, "market_cap": 18000000000},
    {"rank": 18, "symbol": "BCH", "composite_score": 44, "direction": "NO_TRADE", "confidence": 0.42, "price": 478.56, "change24h": -0.67, "market_cap": 9400000000},
    {"rank": 19, "symbol": "FIL", "composite_score": 44, "direction": "NO_TRADE", "confidence": 0.40, "price": 6.78, "change24h": -1.56, "market_cap": 3600000000},
    {"rank": 20, "symbol": "MATIC", "composite_score": 45, "direction": "SHORT", "confidence": 0.62, "price": 0.7891, "change24h": -3.45, "market_cap": 7800000000},
]

@router.get("/")
async def get_rankings(min_score: float = 0, direction: str = None, limit: int = 100):
    filtered = RANKINGS
    if direction:
        filtered = [r for r in filtered if r["direction"] == direction.upper()]
    if min_score > 0:
        filtered = [r for r in filtered if r["composite_score"] >= min_score]
    return {"rankings": filtered[:limit], "total": len(filtered), "updated_at": "2026-08-24T01:00:00Z"}

@router.get("/top")
async def top_opportunities(limit: int = 10):
    return {"rankings": RANKINGS[:limit], "count": min(limit, len(RANKINGS))}

@router.get("/{symbol}")
async def get_asset_ranking(symbol: str):
    ranking = next((r for r in RANKINGS if r["symbol"] == symbol.upper()), None)
    if not ranking:
        return {"error": f"Ranking for {symbol} not found"}
    return ranking
