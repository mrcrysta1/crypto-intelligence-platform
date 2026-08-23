"""Demo blockchain provider with synthetic whale and on-chain data."""

import random
from app.providers.base import BlockchainProvider

class DemoBlockchainProvider(BlockchainProvider):
    async def get_whale_events(self, symbol: str) -> list:
        return [
            {"type": "large_transfer", "amount_usd": random.uniform(5e6, 50e6), "from": "0x742d...8f2a", "to": "Coinbase", "timestamp": "2026-08-24T00:45:00Z", "sentiment": "neutral"},
            {"type": "accumulation", "amount_usd": random.uniform(2e6, 15e6), "from": "Unknown Wallet", "to": "0x3f5c...9a1b", "timestamp": "2026-08-24T00:32:00Z", "sentiment": "bullish"},
            {"type": "exchange_outflow", "amount_usd": random.uniform(1e6, 10e6), "from": "Binance", "to": "0x8d2e...4c7f", "timestamp": "2026-08-24T00:18:00Z", "sentiment": "bullish"},
        ]

    async def get_exchange_flows(self, symbol: str) -> list:
        return [
            {"exchange": "Binance", "flow_type": "inflow", "amount_usd": random.uniform(10e6, 100e6)},
            {"exchange": "Coinbase", "flow_type": "outflow", "amount_usd": random.uniform(10e6, 100e6)},
            {"exchange": "Kraken", "flow_type": "inflow", "amount_usd": random.uniform(5e6, 50e6)},
        ]

    async def get_top_holders(self, symbol: str) -> list:
        return [
            {"address": "0x1a3b...7e2d", "label": "EXCHANGE", "balance_usd": random.uniform(1e9, 10e9)},
            {"address": "0x9f4e...2c8a", "label": "WHALE", "balance_usd": random.uniform(100e6, 1e9)},
            {"address": "0x5c8d...3f1a", "label": "TREASURY", "balance_usd": random.uniform(50e6, 500e6)},
        ]
