from fastapi import APIRouter

router = APIRouter(prefix="/api/assets", tags=["assets"])

DEMO_ASSETS = [
    {"symbol": "BTC", "name": "Bitcoin", "slug": "bitcoin", "price": 67432.18, "change24h": 2.34, "marketCap": 1324000000000, "volume24h": 28500000000, "liquidityScore": 98, "fundamentalScore": 92, "technicalScore": 78, "whaleScore": 85, "derivativeScore": 71, "compositeScore": 82, "direction": "LONG", "confidence": 0.87, "riskLevel": "low"},
    {"symbol": "ETH", "name": "Ethereum", "slug": "ethereum", "price": 3521.45, "change24h": 1.87, "marketCap": 423000000000, "volume24h": 15200000000, "liquidityScore": 95, "fundamentalScore": 88, "technicalScore": 72, "whaleScore": 80, "derivativeScore": 68, "compositeScore": 78, "direction": "LONG", "confidence": 0.82, "riskLevel": "low"},
    {"symbol": "BNB", "name": "BNB", "slug": "bnb", "price": 598.32, "change24h": -0.45, "marketCap": 92000000000, "volume24h": 1800000000, "liquidityScore": 88, "fundamentalScore": 75, "technicalScore": 55, "whaleScore": 62, "derivativeScore": 58, "compositeScore": 64, "direction": "WATCH", "confidence": 0.61, "riskLevel": "medium"},
    {"symbol": "SOL", "name": "Solana", "slug": "solana", "price": 178.92, "change24h": 5.67, "marketCap": 78000000000, "volume24h": 3200000000, "liquidityScore": 85, "fundamentalScore": 82, "technicalScore": 88, "whaleScore": 75, "derivativeScore": 72, "compositeScore": 81, "direction": "LONG", "confidence": 0.85, "riskLevel": "medium"},
    {"symbol": "XRP", "name": "XRP", "slug": "xrp", "price": 0.6234, "change24h": -1.23, "marketCap": 34000000000, "volume24h": 1200000000, "liquidityScore": 82, "fundamentalScore": 65, "technicalScore": 42, "whaleScore": 55, "derivativeScore": 48, "compositeScore": 53, "direction": "WATCH", "confidence": 0.52, "riskLevel": "medium"},
    {"symbol": "ADA", "name": "Cardano", "slug": "cardano", "price": 0.5123, "change24h": -2.15, "marketCap": 18000000000, "volume24h": 520000000, "liquidityScore": 75, "fundamentalScore": 60, "technicalScore": 35, "whaleScore": 48, "derivativeScore": 42, "compositeScore": 47, "direction": "SHORT", "confidence": 0.65, "riskLevel": "medium"},
    {"symbol": "DOGE", "name": "Dogecoin", "slug": "dogecoin", "price": 0.1567, "change24h": 8.34, "marketCap": 22000000000, "volume24h": 2100000000, "liquidityScore": 80, "fundamentalScore": 35, "technicalScore": 72, "whaleScore": 68, "derivativeScore": 55, "compositeScore": 56, "direction": "WATCH", "confidence": 0.58, "riskLevel": "high"},
    {"symbol": "DOT", "name": "Polkadot", "slug": "polkadot", "price": 8.45, "change24h": -0.89, "marketCap": 12000000000, "volume24h": 380000000, "liquidityScore": 72, "fundamentalScore": 68, "technicalScore": 45, "whaleScore": 52, "derivativeScore": 45, "compositeScore": 54, "direction": "WATCH", "confidence": 0.54, "riskLevel": "medium"},
    {"symbol": "AVAX", "name": "Avalanche", "slug": "avalanche", "price": 42.67, "change24h": 3.21, "marketCap": 16000000000, "volume24h": 650000000, "liquidityScore": 78, "fundamentalScore": 72, "technicalScore": 65, "whaleScore": 58, "derivativeScore": 55, "compositeScore": 64, "direction": "LONG", "confidence": 0.72, "riskLevel": "medium"},
    {"symbol": "LINK", "name": "Chainlink", "slug": "chainlink", "price": 18.92, "change24h": 1.45, "marketCap": 11000000000, "volume24h": 420000000, "liquidityScore": 76, "fundamentalScore": 78, "technicalScore": 58, "whaleScore": 65, "derivativeScore": 52, "compositeScore": 65, "direction": "LONG", "confidence": 0.68, "riskLevel": "medium"},
    {"symbol": "MATIC", "name": "Polygon", "slug": "matic-network", "price": 0.7891, "change24h": -3.45, "marketCap": 7800000000, "volume24h": 310000000, "liquidityScore": 70, "fundamentalScore": 62, "technicalScore": 32, "whaleScore": 45, "derivativeScore": 38, "compositeScore": 45, "direction": "SHORT", "confidence": 0.62, "riskLevel": "high"},
    {"symbol": "UNI", "name": "Uniswap", "slug": "uniswap", "price": 12.34, "change24h": 2.12, "marketCap": 9500000000, "volume24h": 280000000, "liquidityScore": 74, "fundamentalScore": 70, "technicalScore": 62, "whaleScore": 55, "derivativeScore": 48, "compositeScore": 60, "direction": "WATCH", "confidence": 0.62, "riskLevel": "medium"},
    {"symbol": "SHIB", "name": "Shiba Inu", "slug": "shiba-inu", "price": 0.00002345, "change24h": 12.56, "marketCap": 14000000000, "volume24h": 1500000000, "liquidityScore": 68, "fundamentalScore": 20, "technicalScore": 75, "whaleScore": 72, "derivativeScore": 45, "compositeScore": 50, "direction": "WATCH", "confidence": 0.48, "riskLevel": "extreme"},
    {"symbol": "LTC", "name": "Litecoin", "slug": "litecoin", "price": 87.23, "change24h": 0.34, "marketCap": 6500000000, "volume24h": 420000000, "liquidityScore": 78, "fundamentalScore": 58, "technicalScore": 48, "whaleScore": 42, "derivativeScore": 40, "compositeScore": 49, "direction": "WATCH", "confidence": 0.50, "riskLevel": "low"},
    {"symbol": "BCH", "name": "Bitcoin Cash", "slug": "bitcoin-cash", "price": 478.56, "change24h": -0.67, "marketCap": 9400000000, "volume24h": 210000000, "liquidityScore": 72, "fundamentalScore": 55, "technicalScore": 42, "whaleScore": 38, "derivativeScore": 35, "compositeScore": 44, "direction": "NO_TRADE", "confidence": 0.42, "riskLevel": "medium"},
    {"symbol": "ATOM", "name": "Cosmos", "slug": "cosmos", "price": 11.23, "change24h": 1.89, "marketCap": 4300000000, "volume24h": 180000000, "liquidityScore": 65, "fundamentalScore": 62, "technicalScore": 55, "whaleScore": 48, "derivativeScore": 42, "compositeScore": 53, "direction": "WATCH", "confidence": 0.55, "riskLevel": "medium"},
    {"symbol": "NEAR", "name": "NEAR Protocol", "slug": "near", "price": 7.89, "change24h": 4.56, "marketCap": 8200000000, "volume24h": 350000000, "liquidityScore": 70, "fundamentalScore": 68, "technicalScore": 70, "whaleScore": 60, "derivativeScore": 55, "compositeScore": 64, "direction": "LONG", "confidence": 0.70, "riskLevel": "medium"},
    {"symbol": "FIL", "name": "Filecoin", "slug": "filecoin", "price": 6.78, "change24h": -1.56, "marketCap": 3600000000, "volume24h": 150000000, "liquidityScore": 62, "fundamentalScore": 58, "technicalScore": 38, "whaleScore": 42, "derivativeScore": 35, "compositeScore": 44, "direction": "NO_TRADE", "confidence": 0.40, "riskLevel": "high"},
    {"symbol": "APT", "name": "Aptos", "slug": "aptos", "price": 9.45, "change24h": 2.78, "marketCap": 4100000000, "volume24h": 220000000, "liquidityScore": 64, "fundamentalScore": 60, "technicalScore": 62, "whaleScore": 52, "derivativeScore": 48, "compositeScore": 56, "direction": "WATCH", "confidence": 0.58, "riskLevel": "medium"},
    {"symbol": "ARB", "name": "Arbitrum", "slug": "arbitrum", "price": 1.23, "change24h": -0.89, "marketCap": 3800000000, "volume24h": 280000000, "liquidityScore": 66, "fundamentalScore": 65, "technicalScore": 45, "whaleScore": 50, "derivativeScore": 42, "compositeScore": 51, "direction": "WATCH", "confidence": 0.52, "riskLevel": "medium"},
]

@router.get("/")
async def list_assets(direction: str = None, min_score: float = 0, limit: int = 20):
    assets = DEMO_ASSETS
    if direction:
        assets = [a for a in assets if a["direction"] == direction.upper()]
    if min_score > 0:
        assets = [a for a in assets if a["compositeScore"] >= min_score]
    return {"assets": assets[:limit], "total": len(assets)}

@router.get("/{symbol}")
async def get_asset(symbol: str):
    asset = next((a for a in DEMO_ASSETS if a["symbol"] == symbol.upper()), None)
    if not asset:
        return {"error": f"Asset {symbol} not found"}
    asset["signals"] = {"reasons": [
        f"Composite score {asset['compositeScore']}/100 suggests {asset['direction'].lower()} bias",
        f"Technical indicators at {asset['technicalScore']}/100",
        f"Whale activity shows {'accumulation' if asset['whaleScore'] > 60 else 'neutral'} pattern",
    ]}
    return asset
