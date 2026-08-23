"""Signal generation worker stubs for demo mode."""

async def generate_signals(symbol: str):
    """Generate trading signals for a symbol."""
    return {"status": "demo_mode", "symbol": symbol}

async def refresh_all_signals():
    """Refresh signals for all active assets."""
    return {"status": "demo_mode", "message": "Signals refreshed"}
