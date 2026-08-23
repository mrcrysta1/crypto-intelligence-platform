-- ============================================================
-- Crypto Intelligence Platform — Demo Seed Data
--
-- Populates a fresh database with a realistic demo universe.
-- Safe to re-run: uses idempotent upserts throughout.
--
-- Usage:
--   psql -U crypto -d crypto_intelligence -f demo_data.sql
--
-- Or inside docker compose:
--   docker compose exec -T postgres psql -U crypto -d crypto_intelligence \
--     < database/seeds/demo_data.sql
--
-- NOTE: For generated timeseries (90 days of candles), prefer
--   python scripts/seed.py   — richer + parameterized.
-- This file seeds the static reference data + a small sample.
-- ============================================================

BEGIN;

-- Needed for digest()/encode() used by url_hash generation below
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ------------------------------------------------------------
-- 1. Asset universe (top-20 by market cap)
-- ------------------------------------------------------------
INSERT INTO assets (symbol, name, slug, coingecko_id, binance_pair, rank_market_cap) VALUES
    ('BTC',   'Bitcoin',           'bitcoin',           'bitcoin',              'BTCUSDT',   1),
    ('ETH',   'Ethereum',          'ethereum',          'ethereum',             'ETHUSDT',   2),
    ('USDT',  'Tether',            'tether',            'tether',               NULL,        3),
    ('BNB',   'BNB',               'binancecoin',       'binancecoin',          'BNBUSDT',   4),
    ('SOL',   'Solana',            'solana',            'solana',               'SOLUSDT',   5),
    ('XRP',   'XRP',               'xrp',               'ripple',               'XRPUSDT',   6),
    ('ADA',   'Cardano',           'cardano',           'cardano',              'ADAUSDT',   7),
    ('DOGE',  'Dogecoin',          'dogecoin',          'dogecoin',             'DOGEUSDT',  8),
    ('AVAX',  'Avalanche',         'avalanche-2',       'avalanche-2',          'AVAXUSDT',  9),
    ('DOT',   'Polkadot',          'polkadot',          'polkadot',             'DOTUSDT',  10),
    ('MATIC', 'Polygon',           'matic-network',     'matic-network',        'MATICUSDT',11),
    ('LINK',  'Chainlink',         'chainlink',         'chainlink',            'LINKUSDT', 12),
    ('LTC',   'Litecoin',          'litecoin',          'litecoin',             'LTCUSDT',  13),
    ('UNI',   'Uniswap',           'uniswap',           'uniswap',              'UNIUSDT',  14),
    ('ATOM',  'Cosmos Hub',        'cosmos',            'cosmos',               'ATOMUSDT', 15),
    ('ETC',   'Ethereum Classic',  'ethereum-classic',  'ethereum-classic',     'ETCUSDT',  16),
    ('FIL',   'Filecoin',          'filecoin',          'filecoin',             'FILUSDT',  17),
    ('APT',   'Aptos',             'aptos',             'aptos',                'APTUSDT',  18),
    ('ARB',   'Arbitrum',          'arbitrum',          'arbitrum',             'ARBUSDT',  19),
    ('OP',    'Optimism',          'optimism',          'optimism',             'OPUSDT',   20)
ON CONFLICT (symbol) DO UPDATE SET
    name            = EXCLUDED.name,
    slug            = EXCLUDED.slug,
    coingecko_id    = EXCLUDED.coingecko_id,
    binance_pair    = EXCLUDED.binance_pair,
    rank_market_cap = EXCLUDED.rank_market_cap;

-- ------------------------------------------------------------
-- 2. Sample OHLCV — last 72 hours, hourly, for the top assets
--    (full history lives in scripts/seed.py output)
-- ------------------------------------------------------------
INSERT INTO ohlcv (time, symbol, open, high, low, close, volume, interval, source)
SELECT
    gs.t,
    a.symbol,
    -- Deterministic pseudo-random walk anchored per symbol
    ROUND((a.base * walk)::numeric, 6),
    ROUND((a.base * walk * 1.006)::numeric, 6),
    ROUND((a.base * walk * 0.994)::numeric, 6),
    ROUND((a.base * next_walk)::numeric, 6),
    ROUND((100000000 / a.base)::numeric, 2),
    '1h',
    'demo-seed'
FROM (
    SELECT generate_series(
        date_trunc('hour', NOW()) - interval '72 hours',
        date_trunc('hour', NOW()),
        interval '1 hour'
    ) AS t,
           ROW_NUMBER() OVER (ORDER BY 1) - 1 AS i
) AS gs
CROSS JOIN (
    SELECT symbol,
           CASE symbol
               WHEN 'BTC' THEN 67400 WHEN 'ETH' THEN 3150 WHEN 'SOL' THEN 165
               WHEN 'BNB' THEN 580 WHEN 'ADA' THEN 0.45 WHEN 'LINK' THEN 14.2
               ELSE 10
           END AS base
    FROM (VALUES ('BTC'),('ETH'),('SOL'),('BNB'),('ADA'),('LINK')) AS v(symbol)
) AS a
CROSS JOIN LATERAL (
    SELECT (1 + 0.02 * SIN(EXTRACT(EPOCH FROM gs.t)/86400.0)
               + 0.004 * ((gs.i % 7) - 3))::float8 AS walk,
           (1 + 0.02 * SIN(EXTRACT(EPOCH FROM (gs.t + interval '1 hour'))/86400.0)
               + 0.004 * ((gs.i % 7) - 2))::float8 AS next_walk
) AS w
ON CONFLICT (symbol, time, interval) DO UPDATE SET
    open = EXCLUDED.open, high = EXCLUDED.high,
    low = EXCLUDED.low, close = EXCLUDED.close,
    volume = EXCLUDED.volume, source = EXCLUDED.source;

-- ------------------------------------------------------------
-- 3. Sample sentiment snapshots — recent 24h, hourly, BTC/ETH/SOL
-- ------------------------------------------------------------
INSERT INTO sentiment_snapshots (symbol, score, sample_size, window_hours, sources, captured_at)
SELECT
    s.symbol,
    ROUND(s.score::numeric, 4),
    40 + (('x' || SUBSTRING(MD5(s.symbol || EXTRACT(HOUR FROM t.captured_at)::text), 1, 6))::BIT(24)::INT % 30),
    24,
    JSONB_BUILD_OBJECT('news', 25, 'social', 15),
    t.captured_at
FROM generate_series(
    date_trunc('hour', NOW()) - interval '24 hours',
    date_trunc('hour', NOW()),
    interval '1 hour'
) AS t(captured_at)
CROSS JOIN (
    VALUES ('BTC', 0.62), ('ETH', 0.31), ('SOL', -0.18)
) AS s(symbol, score)
ON CONFLICT (symbol, captured_at) DO NOTHING;

-- ------------------------------------------------------------
-- 4. Sample news headlines with scores
-- ------------------------------------------------------------
INSERT INTO news_items (url_hash, title, source, url, symbols, nlp_score, community_votes, published_at)
VALUES
    (encode(digest('https://demo.local/news/etf-record',      'sha256'),'hex'),
     'Spot ETF inflows hit new weekly record as institutions accumulate', 'DemoWire',
     'https://demo.local/news/etf-record', ARRAY['BTC'], 0.83,
     '{"positive": 210, "negative": 12}', NOW() - interval '2 hours'),

    (encode(digest('https://demo.local/news/eth-upgrade',     'sha256'),'hex'),
     'Ethereum staking withdrawals queue drops to zero after upgrade',    'ChainDaily',
     'https://demo.local/news/eth-upgrade', ARRAY['ETH','STETH'], 0.58,
     '{"positive": 94, "negative": 21}', NOW() - interval '5 hours'),

    (encode(digest('https://demo.local/news/sol-outage-fear', 'sha256'),'hex'),
     'Analysts debate Solana network stability after brief degradation',  'ValidatorReport',
     'https://demo.local/news/sol-outage-fear', ARRAY['SOL'], -0.44,
     '{"positive": 18, "negative": 77}', NOW() - interval '8 hours'),

    (encode(digest('https://demo.local/news/macro-rates',     'sha256'),'hex'),
     'Rate-cut odds rise; risk assets including crypto catch a bid',      'MacroPulse',
     'https://demo.local/news/macro-rates', ARRAY['BTC','ETH','SOL'], 0.41,
     '{"positive": 130, "negative": 45}', NOW() - interval '11 hours'),

    (encode(digest('https://demo.local/news/whale-btc',       'sha256'),'hex'),
     'Dormant whale wallets move 12,000 BTC in coordinated transfers',    'WhaleAlerts',
     'https://demo.local/news/whale-btc', ARRAY['BTC'], -0.22,
     '{"positive": 40, "negative": 88}', NOW() - interval '16 hours'),

    (encode(digest('https://demo.local/news/defi-tvl',        'sha256'),'hex'),
     'DeFi TVL climbs for sixth consecutive week led by L2 ecosystems',   'DeFiLens',
     'https://demo.local/news/defi-tvl', ARRAY['ARB','OP','MATIC'], 0.66,
     '{"positive": 156, "negative": 19}', NOW() - interval '20 hours')
ON CONFLICT (url_hash) DO NOTHING;

-- ------------------------------------------------------------
-- 5. Sample signals — one per major asset
-- ------------------------------------------------------------
INSERT INTO signals (symbol, action, confidence, horizon_hours, model_version, features, attributions, explanation, generated_at)
VALUES
    ('BTC', 'BUY',  0.78, 24, 'lgbm-demo-v1',
     '{"rsi_14": 38.2, "macd_histogram": 41.7, "ema_cross_score": 0.73, "sentiment_score": 0.61, "volume_zscore": 1.9}',
     '{"ema_cross_score": 0.24, "macd_histogram": 0.18, "sentiment_score": 0.15, "volume_zscore": 0.09, "rsi_14": -0.21}',
     'EMA bullish cross with rising MACD momentum; RSI shows room before overbought; news flow strongly positive.',
     NOW()),

    ('ETH', 'HOLD', 0.54, 24, 'lgbm-demo-v1',
     '{"rsi_14": 51.6, "macd_histogram": 8.3, "ema_cross_score": 0.11, "sentiment_score": 0.31, "volume_zscore": 0.4}',
     '{"sentiment_score": 0.12, "rsi_14": 0.03, "macd_histogram": 0.01}',
     'Mixed momentum: trend flat, sentiment mildly supportive. No statistical edge over baseline.',
     NOW()),

    ('SOL', 'SELL', 0.66, 24, 'lgbm-demo-v1',
     '{"rsi_14": 71.9, "macd_histogram": -33.5, "ema_cross_score": -0.42, "sentiment_score": -0.18, "volume_zscore": 2.4}',
     '{"rsi_14": 0.28, "ema_cross_score": 0.19, "volume_zscore": 0.11}',
     'Overbought RSI against fading EMA structure and elevated distribution volume; negative news cycle.',
     NOW())
RETURNING symbol;

-- ------------------------------------------------------------
-- 6. Demo user (password: demo-password-123 — bcrypt hash)
--    ONLY FOR LOCAL DEMO. Never use this hash in production.
-- ------------------------------------------------------------
INSERT INTO users (email, hashed_password, is_active)
VALUES ('demo@example.com',
        '$2b$12$LQv3c1yqBWVHxkd0gHQZGuZjCxwFvGaGpGFrkVvKz1YqGhXWmJmBu', -- demo-password-123
        TRUE)
ON CONFLICT (email) DO NOTHING;

-- ------------------------------------------------------------
-- 7. Demo portfolio position for that user
-- ------------------------------------------------------------
INSERT INTO portfolio_positions (user_id, symbol, quantity, avg_entry_price, notes)
SELECT u.id, 'BTC', 0.500000000000, 61800.0000000000, 'Seeded demo position'
FROM users u
WHERE u.email = 'demo@example.com'
ON CONFLICT DO NOTHING;

INSERT INTO portfolio_positions (user_id, symbol, quantity, avg_entry_price, notes)
SELECT u.id, 'ETH', 2.500000000000, 2980.0000000000, 'Seeded demo position'
FROM users u
WHERE u.email = 'demo@example.com'
ON CONFLICT DO NOTHING;

-- ------------------------------------------------------------
-- 8. Sample alert rule
-- ------------------------------------------------------------
INSERT INTO alerts (user_id, type, symbol, threshold, status)
SELECT u.id, 'PRICE_ABOVE', 'BTC', 70000, 'ACTIVE'
FROM users u
WHERE u.email = 'demo@example.com'
ON CONFLICT DO NOTHING;

COMMIT;

-- ============================================================
-- Verify the seed
-- ============================================================
SELECT 'assets'    AS table_name, COUNT(*) AS rows FROM assets
UNION ALL SELECT 'ohlcv (last 72h)', COUNT(*) FROM ohlcv WHERE time > NOW() - interval '73 hours'
UNION ALL SELECT 'sentiment',        COUNT(*) FROM sentiment_snapshots
UNION ALL SELECT 'news_items',       COUNT(*) FROM news_items
UNION ALL SELECT 'signals',          COUNT(*) FROM signals
UNION ALL SELECT 'users',            COUNT(*) FROM users
UNION ALL SELECT 'positions',        COUNT(*) FROM portfolio_positions
UNION ALL SELECT 'alerts',           COUNT(*) FROM alerts;
