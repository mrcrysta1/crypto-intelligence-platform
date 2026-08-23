"""Demo market data provider with realistic synthetic data."""

import random
import time
from app.providers.base import MarketDataProvider

ASSETS = {
    "BTC": {"name": "Bitcoin", "base_price": 67432.18, "volatility": 0.02},
    "ETH": {"name": "Ethereum", "base_price": 3521.45, "volatility": 0.025},
    "BNB": {"name": "BNB", "base_price": 598.32, "volatility": 0.018},
    "SOL": {"name": "Solana", "base_price": 178.92, "volatility": 0.035},
    "XRP": {"name": "XRP", "base_price": 0.6234, "volatility": 0.03},
    "ADA": {"name": "Cardano", "base_price": 0.5123, "volatility": 0.032},
    "DOGE": {"name": "Dogecoin", "base_price": 0.1567, "volatility": 0.05},
    "DOT": {"name": "Polkadot", "base_price": 8.45, "volatility": 0.028},
    "AVAX": {"name": "Avalanche", "base_price": 42.67, "volatility": 0.033},
    "LINK": {"name": "Chainlink", "base_price": 18.92, "volatility": 0.027},
    "MATIC": {"name": "Polygon", "base_price": 0.7891, "volatility": 0.04},
    "UNI": {"name": "Uniswap", "base_price": 12.34, "volatility": 0.035},
    "SHIB": {"name": "Shiba Inu", "base_price": 0.00002345, "volatility": 0.06},
    "LTC": {"name": "Litecoin", "base_price": 87.23, "volatility": 0.022},
    "BCH": {"name": "Bitcoin Cash", "base_price": 478.56, "volatility": 0.025},
    "ATOM": {"name": "Cosmos", "base_price": 11.23, "volatility": 0.03},
    "NEAR": {"name": "NEAR Protocol", "base_price": 7.89, "volatility": 0.038},
    "FIL": {"name": "Filecoin", "base_price": 6.78, "volatility": 0.035},
    "APT": {"name": "Aptos", "base_price": 9.45, "volatility": 0.032},
    "ARB": {"name": "Arbitrum", "base_price": 1.23, "volatility": 0.03},
}


class DemoMarketProvider(MarketDataProvider):
    async def get_price(self, symbol: str) -> dict:
        asset = ASSETS.get(symbol.upper())
        if not asset:
            return {"error": f"Unknown symbol: {symbol}"}
        price = asset["base_price"] * (1 + random.uniform(-0.02, 0.02))
        return {
            "symbol": symbol.upper(),
            "price": price,
            "change_24h": random.uniform(-5, 8),
            "volume_24h": random.uniform(1e8, 3e10),
            "market_cap": price * random.uniform(1e7, 2e10),
        }

    async def get_ohlcv(self, symbol: str, interval: str = "1h", limit: int = 100) -> list:
        asset = ASSETS.get(symbol.upper())
        if not asset:
            return []
        base = asset["base_price"]
        vol = asset["volatility"]
        now = int(time.time())
        candles = []
        price = base * 0.95
        for i in range(limit):
            ts = now - (limit - i) * 3600
            change = random.gauss(0, vol)
            o = price
            h = price * (1 + abs(random.gauss(0, vol * 0.5)))
            l = price * (1 - abs(random.gauss(0, vol * 0.5)))
            c = price * (1 + change)
            v = random.uniform(1e6, 5e8)
            candles.append({
                "timestamp": ts,
                "open": round(o, 8),
                "high": round(max(o, h, c), 8),
                "low": round(min(o, l, c), 8),
                "close": round(c, 8),
                "volume": round(v, 2),
            })
            price = c
        return candles

    async def get_market_data(self, symbol: str) -> dict:
        price_data = await self.get_price(symbol)
        ohlcv = await self.get_ohlcv(symbol, "1h", 100)
        return {**price_data, "ohlcv": ohlcv}

    async def get_derivatives(self, symbol: str) -> dict:
        return {
            "funding_rate": random.uniform(-0.0005, 0.001),
            "predicted_funding_rate": random.uniform(-0.0003, 0.0008),
            "open_interest": random.uniform(1e8, 5e9),
            "open_interest_change_24h": random.uniform(-10, 15),
            "long_short_ratio": random.uniform(0.8, 1.5),
            "liquidations_24h": random.uniform(1e6, 1e8),
        }
