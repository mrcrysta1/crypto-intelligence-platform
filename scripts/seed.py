#!/usr/bin/env python3
"""
Seed demo data for the Crypto Intelligence Platform.

Populates the database with realistic synthetic data so the platform is
immediately explorable. Works against a running stack (Docker or local).

Usage:
    python scripts/seed.py                          # default: 50 assets, 90d candles
    python scripts/seed.py --assets 20 --days 30    # smaller/faster
    python scripts/seed.py --reset                  # wipe seeded tables first

Requires DATABASE_URL (or DATABASE_SYNC_URL) env var, or falls back to
the local docker-compose defaults.
"""

from __future__ import annotations

import argparse
import asyncio
import hashlib
import math
import os
import random
import sys
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Any

DEFAULT_DATABASE_URL = "postgresql://crypto:crypto@localhost:5432/crypto_intelligence"

# ---------------------------------------------------------------------------
# Synthetic universe — plausible anchors for demo assets
# ---------------------------------------------------------------------------
ASSET_UNIVERSE: list[dict[str, Any]] = [
    {"symbol": "BTC",  "name": "Bitcoin",           "slug": "bitcoin",   "price": 67_400.0},
    {"symbol": "ETH",  "name": "Ethereum",          "slug": "ethereum",  "price": 3_150.0},
    {"symbol": "USDT", "name": "Tether",            "slug": "tether",    "price": 1.0001},
    {"symbol": "BNB",  "name": "BNB",               "slug": "binancecoin", "price": 580.0},
    {"symbol": "SOL",  "name": "Solana",            "slug": "solana",    "price": 165.0},
    {"symbol": "XRP",  "name": "XRP",               "slug": "xrp",       "price": 0.62},
    {"symbol": "ADA",  "name": "Cardano",           "slug": "cardano",   "price": 0.45},
    {"symbol": "DOGE", "name": "Dogecoin",          "slug": "dogecoin",  "price": 0.14},
    {"symbol": "AVAX", "name": "Avalanche",         "slug": "avalanche-2", "price": 28.0},
    {"symbol": "DOT",  "name": "Polkadot",          "slug": "polkadot",  "price": 6.4},
    {"symbol": "MATIC","name": "Polygon",           "slug": "matic-network", "price": 0.58},
    {"symbol": "LINK", "name": "Chainlink",         "slug": "chainlink", "price": 14.2},
    {"symbol": "LTC",  "name": "Litecoin",          "slug": "litecoin",  "price": 72.0},
    {"symbol": "UNI",  "name": "Uniswap",           "slug": "uniswap",   "price": 7.8},
    {"symbol": "ATOM", "name": "Cosmos",            "slug": "cosmos",    "price": 7.1},
    {"symbol": "ETC",  "name": "Ethereum Classic",  "slug": "ethereum-classic", "price": 26.0},
    {"symbol": "FIL",  "name": "Filecoin",          "slug": "filecoin",  "price": 4.3},
    {"symbol": "APT",  "name": "Aptos",             "slug": "aptos",     "price": 8.9},
    {"symbol": "ARB",  "name": "Arbitrum",          "slug": "arbitrum",  "price": 0.74},
    {"symbol": "OP",   "name": "Optimism",          "slug": "optimism",  "price": 1.65},
]

HEADLINE_TEMPLATES: list[tuple[str, float]] = [
    ("{sym} ETF sees record weekly inflows as institutions pile in",        0.82),
    ("Analyst upgrades {sym} outlook citing network growth metrics",         0.64),
    ("{sym} whales accumulate aggressively during recent dip",              0.55),
    ("Developer activity on {sym} chain hits all-time high",                 0.48),
    ("Major payment processor expands {sym} settlement support",             0.71),
    ("{sym} consolidates near resistance; traders eye breakout",             0.05),
    ("Market neutral: {sym} rangebound as volume cools off",                -0.02),
    ("{sym} faces profit-taking after extended rally",                      -0.35),
    ("Regulatory uncertainty weighs on {sym} short-term sentiment",         -0.58),
    ("Security researcher flags vulnerability in {sym} DeFi protocol",      -0.76),
    ("Exchange outflows spike as {sym} holders move to cold storage",        0.33),
    ("{sym} futures funding rates flip negative amid bearish positioning",  -0.61),
]


def stable_seed(*parts: str) -> int:
    """Deterministic seed from strings — same inputs always produce same stream."""
    digest = hashlib.sha256("|".join(parts).encode()).hexdigest()
    return int(digest[:16], 16)


def synth_candles(
    symbol: str,
    anchor_price: float,
    days: int,
    interval_minutes: int = 60,
) -> list[dict[str, Any]]:
    """Generate a plausible OHLCV series with trend segments and volatility regimes."""
    rng = random.Random(stable_seed(symbol, f"v{days}", str(interval_minutes)))
    points = days * (24 * 60 // interval_minutes)
    candles: list[dict[str, Any]] = []

    price = anchor_price * rng.uniform(0.85, 1.15)
    vol = 0.004 + rng.random() * 0.008          # per-candle volatility regime
    trend = rng.uniform(-0.00008, 0.00012)      # slow drift
    now = datetime.now(tz=timezone.utc)

    for i in range(points):
        # Regime shifts every ~2 days of candles
        if i % max(24 * 60 // interval_minutes, 1) == 0:
            trend = rng.uniform(-0.00012, 0.00018)
            vol = 0.003 + rng.random() * 0.010

        ret = rng.gauss(trend, vol)
        open_p = price
        close_p = max(open_p * (1 + ret), anchor_price * 0.05)   # never collapse to dust
        high = max(open_p, close_p) * (1 + abs(rng.gauss(0, vol / 2)))
        low = min(open_p, close_p) * (1 - abs(rng.gauss(0, vol / 2)))
        base_volume = rng.uniform(800, 3200) * (anchor_price / close_p) ** 0.25
        ts = now - timedelta(minutes=(points - i) * interval_minutes)

        candles.append({
            "ts": ts,
            "open": Decimal(str(round(open_p, 6))),
            "high": Decimal(str(round(high, 6))),
            "low": Decimal(str(round(low, 6))),
            "close": Decimal(str(round(close_p, 6))),
            "volume": Decimal(str(round(base_volume, 2))),
        })
        price = close_p

    return candles


def synth_headlines(symbol: str, count: int) -> list[dict[str, Any]]:
    """Deterministic scored headlines for one asset."""
    rng = random.Random(stable_seed(symbol, "headlines"))
    headlines: list[dict[str, Any]] = []
    now = datetime.now(tz=timezone.utc)
    k = min(count, len(HEADLINE_TEMPLATES))
    indices = sorted(rng.sample(range(len(HEADLINE_TEMPLATES)), k=k))
    picks = [HEADLINE_TEMPLATES[i] for i in indices]

    for tpl, polarity in picks:
        jittered_score = max(-1.0, min(1.0, polarity + rng.gauss(0, 0.12)))
        headlines.append({
            "title": tpl.format(sym=symbol),
            "source": "demo-generator",
            "url": f"https://demo.local/news/{symbol.lower()}/{stable_seed(symbol, tpl)[:12]}",
            "published_at": now - timedelta(hours=rng.uniform(0, 48)),
            "score": round(jittered_score, 4),
        })
    return headlines


def synth_signal(symbol: str, last_close: Decimal) -> dict[str, Any]:
    """Deterministic signal consistent with the asset's synthetic momentum."""
    rng = random.Random(stable_seed(symbol, "signal"))
    actions = ["BUY", "SELL", "HOLD"]
    action = rng.choices(actions, weights=[0.38, 0.27, 0.35], k=1)[0]
    confidence = round(0.52 + rng.random() * 0.44, 4)
    rsi = round(rng.uniform(22, 78), 2)
    return {
        "symbol": symbol,
        "action": action,
        "confidence": confidence,
        "model_version": "lgbm-demo-v1",
        "horizon_hours": 24,
        "features": {
            "rsi_14": rsi,
            "macd_histogram": round(rng.uniform(-120, 120), 3),
            "ema_cross_score": round(rng.uniform(-1, 1), 3),
            "sentiment_score": round(rng.uniform(-0.8, 0.9), 3),
            "volume_zscore": round(rng.uniform(-1.5, 3.0), 3),
            "last_close": float(last_close),
        },
    }


# ---------------------------------------------------------------------------
# Database layer — raw SQL via psycopg for zero heavy deps
# ---------------------------------------------------------------------------

def get_connection():
    url = (
        os.environ.get("DATABASE_SYNC_URL")
        or os.environ.get("DATABASE_URL", DEFAULT_DATABASE_URL).replace("+asyncpg", "")
    )
    try:
        import psycopg  # noqa: PLC0415
        return psycopg.connect(url), "psycopg3"
    except ImportError:
        pass
    try:
        import psycopg2  # noqa: PLC0415
        return psycopg2.connect(url), "psycopg2"
    except ImportError:
        print(
            "ERROR: Install a postgres driver to run the seeder:\n"
            "  pip install 'psycopg[binary]'   (or psycopg2-binary)",
            file=sys.stderr,
        )
        raise SystemExit(2)


SCHEMA_HINT = """
-- Tables expected by the seeder (create via database/schemas/initial_schema.sql or alembic):
CREATE TABLE IF NOT EXISTS assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ohlcv (
    time TIMESTAMPTZ NOT NULL,
    symbol VARCHAR(20) NOT NULL,
    open NUMERIC(24,10) NOT NULL,
    high NUMERIC(24,10) NOT NULL,
    low NUMERIC(24,10) NOT NULL,
    close NUMERIC(24,10) NOT NULL,
    volume NUMERIC(28,6) NOT NULL,
    PRIMARY KEY (symbol, time)
);
"""


def seed(reset: bool, n_assets: int, days: int) -> None:
    conn, driver = get_connection()
    cur = conn.cursor()

    print(f"Connected via {driver}. Seeding {n_assets} assets x {days} days...")

    cur.execute(SCHEMA_HINT)  # no-op when tables exist

    if reset:
        print("  --reset: clearing existing demo data...")
        cur.execute("TRUNCATE ohlcv, assets RESTART IDENTITY CASCADE;")
        for extra in ("signals", "sentiment_snapshots"):
            try:
                cur.execute(f"TRUNCATE {extra};")
            except Exception:
                conn.rollback()

    chosen = ASSET_UNIVERSE[:n_assets]
    now = datetime.now(tz=timezone.utc)

    for spec in chosen:
        sym = spec["symbol"]
        cur.execute(
            """
            INSERT INTO assets (symbol, name, slug, created_at)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (symbol) DO UPDATE SET name = EXCLUDED.name;
            """,
            (sym, spec["name"], spec["slug"], now),
        )

        candles = synth_candles(sym, spec["price"], days)
        cur.executemany(
            """
            INSERT INTO ohlcv (time, symbol, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (symbol, time) DO UPDATE SET
                open = EXCLUDED.open, high = EXCLUDED.high,
                low = EXCLUDED.low, close = EXCLUDED.close,
                volume = EXCLUDED.volume;
            """,
            [
                (c["ts"], sym, c["open"], c["high"], c["low"], c["close"], c["volume"])
                for c in candles
            ],
        )
        print(f"  {sym:<6} {len(candles):>6} candles  "
              f"(last close ≈ {float(candles[-1]['close']):>12,.4f})")

    conn.commit()
    total_rows = len(chosen) * days * 24
    print(f"\nSeeded ~{total_rows:,} OHLCV rows across {len(chosen)} assets.")
    print("Demo data ready. Start the API and visit http://localhost:8000/docs")

    cur.close()
    conn.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed demo data for Crypto Intelligence Platform")
    parser.add_argument("--assets", type=int, default=len(ASSET_UNIVERSE),
                        help=f"How many assets to seed (max {len(ASSET_UNIVERSE)})")
    parser.add_argument("--days", type=int, default=90, help="Days of hourly candles per asset")
    parser.add_argument("--reset", action="store_true", help="Truncate tables before seeding")
    args = parser.parse_args()

    n_assets = max(1, min(args.assets, len(ASSET_UNIVERSE)))
    days = max(1, min(args.days, 365))
    seed(args.reset, n_assets, days)


if __name__ == "__main__":
    main()
