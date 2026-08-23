-- ============================================================
-- Crypto Intelligence Platform — Reference Schema
--
-- This file documents the full relational model for reference
-- and manual provisioning. The app's source of truth is the
-- SQLAlchemy models + Alembic migrations; this SQL mirrors them.
--
-- Target: PostgreSQL 16 with TimescaleDB extension
--
-- Usage:
--   psql -U crypto -d crypto_intelligence -f initial_schema.sql
-- ============================================================

BEGIN;

-- ------------------------------------------------------------
-- Extensions
-- ------------------------------------------------------------
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pg_trgm;        -- fuzzy search on asset names
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";    -- uuid generation (fallback)

-- ------------------------------------------------------------
-- ENUM types
-- ------------------------------------------------------------
DO $$ BEGIN
    CREATE TYPE signal_action AS ENUM ('BUY', 'SELL', 'HOLD');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE sentiment_label AS ENUM ('BULLISH', 'NEUTRAL', 'BEARISH');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE alert_type AS ENUM (
        'PRICE_ABOVE', 'PRICE_BELOW', 'PCT_CHANGE_24H',
        'SIGNAL_ACTION', 'SENTIMENT_THRESHOLD'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE alert_status AS ENUM ('ACTIVE', 'TRIGGERED', 'CANCELLED');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE audit_action AS ENUM (
        'LOGIN', 'LOGOUT', 'REGISTER', 'REFRESH',
        'PORTFOLIO_CREATE', 'PORTFOLIO_UPDATE', 'PORTFOLIO_DELETE',
        'ALERT_CREATE', 'ALERT_CANCEL', 'ADMIN_ACTION'
    );
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- ============================================================
-- CORE: Users & Authentication
-- ============================================================
CREATE TABLE IF NOT EXISTS users (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email               VARCHAR(255) NOT NULL UNIQUE,
    hashed_password     VARCHAR(255) NOT NULL,           -- bcrypt
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    is_admin            BOOLEAN NOT NULL DEFAULT FALSE,
    api_key_hash        VARCHAR(255),                    -- optional machine access
    last_login_at       TIMESTAMPTZ,
    failed_login_count  SMALLINT NOT NULL DEFAULT 0,
    locked_until        TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);
CREATE INDEX IF NOT EXISTS idx_users_api_key ON users (api_key_hash) WHERE api_key_hash IS NOT NULL;

CREATE TABLE IF NOT EXISTS refresh_tokens (
    id            UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    token_hash    VARCHAR(255) NOT NULL UNIQUE,
    expires_at    TIMESTAMPTZ NOT NULL,
    revoked_at    TIMESTAMPTZ,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_refresh_tokens_user ON refresh_tokens (user_id);
CREATE INDEX IF NOT EXISTS idx_refresh_tokens_expiry ON refresh_tokens (expires_at) WHERE revoked_at IS NULL;

-- ============================================================
-- CORE: Assets
-- ============================================================
CREATE TABLE IF NOT EXISTS assets (
    id                SERIAL PRIMARY KEY,
    symbol            VARCHAR(20) NOT NULL UNIQUE,      -- canonical: BTC
    name              VARCHAR(100) NOT NULL,
    slug              VARCHAR(120) NOT NULL UNIQUE,     -- provider slug: bitcoin
    coingecko_id      VARCHAR(120),
    binance_pair      VARCHAR(30),                      -- BTCUSDT
    is_active         BOOLEAN NOT NULL DEFAULT TRUE,
    rank_market_cap   INTEGER,
    created_at        TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_assets_symbol_trgm ON assets USING gin (symbol gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_assets_name_trgm   ON assets USING gin (name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_assets_active_rank ON assets (is_active, rank_market_cap);

-- ============================================================
-- TIMESERIES: OHLCV (hypertable)
-- ============================================================
CREATE TABLE IF NOT EXISTS ohlcv (
    time        TIMESTAMPTZ NOT NULL,
    symbol      VARCHAR(20) NOT NULL REFERENCES assets(symbol) ON DELETE CASCADE,
    open        NUMERIC(24,10) NOT NULL CHECK (open  >= 0),
    high        NUMERIC(24,10) NOT NULL CHECK (high  >= 0),
    low         NUMERIC(24,10) NOT NULL CHECK (low   >= 0),
    close       NUMERIC(24,10) NOT NULL CHECK (close >= 0),
    volume      NUMERIC(28,6)  NOT NULL CHECK (volume >= 0),
    interval    VARCHAR(6) NOT NULL DEFAULT '1h',       -- 1m/5m/15m/1h/4h/1d
    source      VARCHAR(40) NOT NULL DEFAULT 'coingecko',
    PRIMARY KEY (symbol, time, interval)
);

SELECT create_hypertable('ohlcv', 'time', if_not_exists => TRUE);

-- Candle sanity: high must bound low/open/close
ALTER TABLE ohlcv ADD CONSTRAINT chk_ohlcv_bounds
    CHECK (high >= low AND high >= GREATEST(open, close)
                       AND low <= LEAST(open, close)) NOT VALID;

-- Continuous aggregates for common chart intervals (raw assumed 1h)
CREATE MATERIALIZED VIEW IF NOT EXISTS ohlcv_1d
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 day', time) AS day,
    symbol,
    first(open, time)  AS open,
    max(high)          AS high,
    min(low)           AS low,
    last(close, time)  AS close,
    sum(volume)        AS volume
FROM ohlcv
WHERE interval = '1h'
GROUP BY day, symbol
WITH NO DATA;

-- Retention & compression policy (adjust to taste)
ALTER TABLE ohlcv SET (
    timescaledb.compress,
    timescaledb.compress_segmentby = 'symbol'
);
SELECT add_compression_policy('ohlcv', INTERVAL '7 days', if_not_exists => TRUE);
SELECT add_retention_policy('ohlcv', INTERVAL '400 days', if_not_exists => TRUE);

-- Fast lookups: latest candle per symbol per interval
CREATE INDEX IF NOT EXISTS idx_ohlcv_latest
    ON ohlcv (symbol, interval, time DESC);

-- ============================================================
-- INTELLIGENCE: Signals (ML decisions)
-- ============================================================
CREATE TABLE IF NOT EXISTS signals (
    id              BIGSERIAL PRIMARY KEY,
    symbol          VARCHAR(20) NOT NULL REFERENCES assets(symbol) ON DELETE CASCADE,
    action          signal_action NOT NULL,
    confidence      NUMERIC(5,4) NOT NULL CHECK (confidence BETWEEN 0 AND 1),
    horizon_hours   INTEGER NOT NULL DEFAULT 24,
    model_version   VARCHAR(60) NOT NULL,
    features        JSONB NOT NULL DEFAULT '{}',        -- {rsi_14: 38.2, ...}
    attributions    JSONB,                              -- per-feature contributions
    explanation     TEXT,                               -- narrative summary
    generated_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Latest signals first; supports history pagination
CREATE INDEX IF NOT EXISTS idx_signals_symbol_time  ON signals (symbol, generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_signals_action_conf  ON signals (action, confidence DESC)
    WHERE confidence >= 0.7;
CREATE INDEX IF NOT EXISTS idx_signals_features_gin ON signals USING gin (features jsonb_path_ops);

-- Immutable ledger semantics: block updates/deletes at DB level via trigger
CREATE OR REPLACE FUNCTION block_table_mutation()
RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION '% is append-only (UPDATE/DELETE blocked)', TG_TABLE_NAME;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_signals_immutable ON signals;
CREATE TRIGGER trg_signals_immutable
    BEFORE UPDATE OR DELETE ON signals
    FOR EACH ROW EXECUTE FUNCTION block_table_mutation();

-- ============================================================
-- INTELLIGENCE: Sentiment snapshots
-- ============================================================
CREATE TABLE IF NOT EXISTS sentiment_snapshots (
    id              BIGSERIAL PRIMARY KEY,
    symbol          VARCHAR(20) NOT NULL REFERENCES assets(symbol) ON DELETE CASCADE,
    score           NUMERIC(5,4) NOT NULL CHECK (score BETWEEN -1 AND 1),
    label           sentiment_label GENERATED ALWAYS AS (
                        CASE
                            WHEN score > 0.15 THEN 'BULLISH'::sentiment_label
                            WHEN score < -0.15 THEN 'BEARISH'::sentiment_label
                            ELSE 'NEUTRAL'::sentiment_label
                        END
                    ) STORED,
    sample_size     INTEGER NOT NULL DEFAULT 0,
    window_hours    INTEGER NOT NULL DEFAULT 24,
    sources         JSONB NOT NULL DEFAULT '{}',        -- {news: 31, social: 16}
    captured_at     TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (symbol, captured_at)
);

CREATE INDEX IF NOT EXISTS idx_sentiment_symbol_time ON sentiment_snapshots (symbol, captured_at DESC);

-- Raw scored headlines backing each snapshot
CREATE TABLE IF NOT EXISTS news_items (
    id              BIGSERIAL PRIMARY KEY,
    url_hash        VARCHAR(64) NOT NULL UNIQUE,        -- sha256(url) — dedupe key
    title           TEXT NOT NULL,
    source          VARCHAR(80) NOT NULL,
    url             TEXT NOT NULL,
    symbols         VARCHAR(20)[] NOT NULL DEFAULT '{}',
    nlp_score       NUMERIC(5,4) CHECK (nlp_score BETWEEN -1 AND 1),
    community_votes JSONB,                              -- cryptopanic votes
    published_at    TIMESTAMPTZ NOT NULL,
    ingested_at     TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_news_published ON news_items (published_at DESC);
CREATE INDEX IF NOT EXISTS idx_news_symbols   ON news_items USING gin (symbols);

-- ============================================================
-- USER STATE: Portfolio
-- ============================================================
CREATE TABLE IF NOT EXISTS portfolio_positions (
    id                  BIGSERIAL PRIMARY KEY,
    user_id             UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    symbol              VARCHAR(20) NOT NULL REFERENCES assets(symbol),
    quantity            NUMERIC(28,12) NOT NULL CHECK (quantity != 0),
    avg_entry_price     NUMERIC(24,10) NOT NULL CHECK (avg_entry_price >= 0),
    notes               TEXT,
    opened_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    closed_at           TIMESTAMPTZ,
    UNIQUE (user_id, symbol, opened_at)
);

CREATE INDEX IF NOT EXISTS idx_positions_user ON portfolio_positions (user_id) WHERE closed_at IS NULL;

CREATE TABLE IF NOT EXISTS equity_snapshots (
    time            TIMESTAMPTZ NOT NULL,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    total_value_usd NUMERIC(28,8) NOT NULL,
    unrealized_pnl  NUMERIC(28,8) NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, time)
);

SELECT create_hypertable('equity_snapshots', 'time', if_not_exists => TRUE);

-- ============================================================
-- USER STATE: Alerts
-- ============================================================
CREATE TABLE IF NOT EXISTS alerts (
    id              BIGSERIAL PRIMARY KEY,
    user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type            alert_type NOT NULL,
    symbol          VARCHAR(20) NOT NULL REFERENCES assets(symbol),
    threshold       NUMERIC(28,10),
    status          alert_status NOT NULL DEFAULT 'ACTIVE',
    triggered_at    TIMESTAMPTZ,
    triggered_value NUMERIC(28,10),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_alerts_user_status  ON alerts (user_id, status);
CREATE INDEX IF NOT EXISTS idx_alerts_eval_pending ON alerts (status, type, symbol)
    WHERE status = 'ACTIVE';

CREATE TABLE IF NOT EXISTS alert_events (
    id          BIGSERIAL PRIMARY KEY,
    alert_id    BIGINT NOT NULL REFERENCES alerts(id) ON DELETE CASCADE,
    message     TEXT NOT NULL,
    payload     JSONB,
    notified_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- GOVERNANCE: Audit log (append-only)
-- ============================================================
CREATE TABLE IF NOT EXISTS audit_log (
    id          BIGSERIAL PRIMARY KEY,
    user_id     UUID REFERENCES users(id) ON DELETE SET NULL,
    action      audit_action NOT NULL,
    ip_address  INET,
    user_agent  TEXT,
    detail      JSONB NOT NULL DEFAULT '{}',
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_user_time  ON audit_log (user_id, occurred_at DESC);
CREATE INDEX IF NOT EXISTS idx_audit_action     ON audit_log (action, occurred_at DESC);

DROP TRIGGER IF EXISTS trg_audit_immutable ON audit_log;
CREATE TRIGGER trg_audit_immutable
    BEFORE UPDATE OR DELETE ON audit_log
    FOR EACH ROW EXECUTE FUNCTION block_table_mutation();  -- same append-only guard

-- ============================================================
-- OPERATIONS: Provider health tracking
-- ============================================================
CREATE TABLE IF NOT EXISTS provider_health (
    provider_name   VARCHAR(60) PRIMARY KEY,
    consecutive_failures INTEGER NOT NULL DEFAULT 0,
    circuit_state   VARCHAR(12) NOT NULL DEFAULT 'closed'
                    CHECK (circuit_state IN ('closed','open','half_open')),
    last_success_at TIMESTAMPTZ,
    last_failure_at TIMESTAMPTZ,
    last_error      TEXT,
    total_requests  BIGINT NOT NULL DEFAULT 0,
    total_failures  BIGINT NOT NULL DEFAULT 0,
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ============================================================
-- Housekeeping: updated_at touch triggers
-- ============================================================
CREATE OR REPLACE FUNCTION touch_updated_at()
RETURNS trigger AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_users_touch ON users;
CREATE TRIGGER trg_users_touch BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION touch_updated_at();

COMMIT;

-- ============================================================
-- Summary of design decisions:
--   * ohlcv/equity_snapshots are hypertables → auto partitioning,
--     compression after 7d, retention after 400d
--   * signals & audit_log are append-only (trigger-enforced)
--   * natural-key upserts keep ingestion idempotent
--   * sentiment label derived in-DB so it can never drift from score
--   * trgm indexes power fuzzy asset search cheaply
-- ============================================================
