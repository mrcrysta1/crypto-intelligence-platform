"""Market data ingestion worker stubs for demo mode."""

async def ingest_market_data(symbol: str):
    """Ingest latest market data for a symbol."""
    return {"status": "demo_mode", "symbol": symbol}

async def ingest_ohlcv(symbol: str, interval: str = "1h"):
    """Ingest OHLCV data for a symbol."""
    return {"status": "demo_mode", "symbol": symbol, "interval": interval}

async def ingest_derivatives(symbol: str):
    """Ingest derivatives data for a symbol."""
    return {"status": "demo_mode", "symbol": symbol}
