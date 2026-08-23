# Architecture

Crypto Intelligence & AI Trading Decision Platform — System Design Document.

---

## 1. System Overview

The platform is a modular monolith gateway (FastAPI) backed by a timeseries database (PostgreSQL + TimescaleDB), a cache/broker tier (Redis), and an asynchronous processing tier (Celery workers + beat scheduler). The frontend is a Next.js application consuming the REST API.

```
┌────────────┐   ┌────────────┐   ┌──────────────────┐
│  Frontend  │──▶│ API Gateway │──▶│ Provider Layer    │
│  Next.js   │   │  FastAPI    │   │ (external APIs /  │
└────────────┘   └─────┬──────┘   │  mock providers)  │
                       │          └──────────────────┘
        ┌──────────────┼───────────────┐
        ▼              ▼               ▼
  ┌──────────┐  ┌──────────┐   ┌────────────┐
  │ Postgres │  │  Redis   │   │  Celery     │
  │ Timescale│  │ cache/   │◀──│ workers +   │
  │ :5432    │  │ broker   │   │ beat        │
  └──────────┘  └──────────┘   └────────────┘
```

Core responsibilities per service:

| Service | Responsibility |
|---|---|
| `web` | SSR dashboard, charts, alerts UI |
| `api` | Auth, validation, orchestration, caching, rate limiting |
| `postgres` | Durable storage: users, assets, OHLCV hypertable, signals, sentiment, audit log |
| `redis` | Response cache, Celery broker/backend, distributed locks, pub/sub for WS fanout |
| `worker` | Price ingestion, signal generation, ML scoring, sentiment jobs |
| `scheduler` | Cron-like triggers via Celery Beat |

## 2. Service Communication

### 2.1 Synchronous paths

- **Browser → web**: HTTPS. Next.js server components fetch from the API at render time; client components call the API directly.
- **web/api → api**: REST over HTTP. JSON payloads, JWT bearer auth.
- **api → postgres**: SQLAlchemy 2.0 async engine (`asyncpg`). Connection pooling with pre-ping; pool size tuned via env.
- **api → redis**: `redis-py` async client. Read-through cache pattern:
  ```
  GET key → hit? return : query DB → SET key TTL → return
  ```
- **api → external providers**: `httpx.AsyncClient` with timeouts, retries (exponential backoff + jitter), and circuit breakers.

### 2.2 Asynchronous paths

- **api → worker**: FastAPI handlers enqueue Celery tasks (`task.delay()`), returning `202 Accepted` + task id for long-running work.
- **scheduler → worker**: Beat publishes periodic tasks to the broker.
- **worker → api clients**: Workers write results to Postgres and publish events on Redis channels; the API's WebSocket layer fans out to subscribed sockets.

### 2.3 Failure isolation rules

1. The API never blocks on external providers longer than its circuit-breaker budget.
2. Cache reads are best-effort — Redis outage degrades latency, not availability.
3. Workers are idempotent; redelivery cannot double-insert (upsert semantics keyed by natural keys).
4. Postgres is the single source of truth; Redis is disposable state.

## 3. Data Flow

### 3.1 Price ingestion pipeline

```
Beat tick (60s)
   └─▶ task: ingest_prices
         ├─▶ provider.fetch_ohlcv(assets, timeframe=1m)
         ├─▶ normalize → canonical OHLCV schema
         ├─▶ upsert into ohlcv hypertable (ON CONFLICT DO UPDATE)
         ├─▶ invalidate redis keys: price:{symbol}, markets:list
         └─▶ publish event: price.updated.{symbol} → Redis channel
                └─▶ API WebSocket layer → connected browsers
```

### 3.2 Signal generation pipeline

```
Beat tick (5m)
   └─▶ task: generate_signals
         ├─▶ load last N candles from hypertable (continuous aggregates)
         ├─▶ feature engineering: RSI(14), MACD(12,26,9),
         │    Bollinger(20,2), EMA(9/21) cross, volume z-score,
         │    sentiment score join
         ├─▶ model.predict(features) → {action, confidence, attributions}
         ├─▶ persist to signals table (immutable append)
         └─▶ if confidence ≥ alert_threshold → publish signal.created
```

### 3.3 Sentiment pipeline

```
Beat tick (15m)
   └─▶ task: collect_sentiment
         ├─▶ news provider.fetch_headlines(symbols)
         ├─▶ dedupe (url hash) → NLP scoring (FinBERT or LLM fallback)
         ├─▶ aggregate per symbol per window → weighted mean
         └─▶ upsert into sentiment_snapshots
```

## 4. Event Architecture

Redis pub/sub is the in-memory event bus; Postgres is the durable event log where retention matters.

| Event | Channel | Producer | Consumers |
|---|---|---|---|
| Price updated | `events:price:{symbol}` | ingestion worker | WS layer, alert engine |
| Signal created | `events:signal:{symbol}` | signal worker | WS layer, notification service |
| Sentiment updated | `events:sentiment:{symbol}` | sentiment worker | WS layer |
| Alert triggered | `events:alert:{user}` | alert engine | WS layer, email/push adapters |

Design properties:

- **At-least-once delivery** on the bus; consumers must be idempotent.
- **Durable history** lives in tables (`signals`, `sentiment_snapshots`, `audit_log`) — the bus is ephemeral.
- **Fanout** is handled by one API process subscribing per channel and broadcasting internally; horizontal scale uses Redis Streams as a shared consumer group when socket count grows beyond a single node.

## 5. Provider Abstraction

All external data enters through a strategy-pattern interface so providers are swappable and testable:

```python
class MarketDataProvider(Protocol):
    async def get_price(self, symbol: str) -> PriceQuote: ...
    async def get_ohlcv(self, symbol: str, timeframe: str, limit: int) -> list[OHLCV]: ...

class NewsProvider(Protocol):
    async def get_headlines(self, symbols: list[str]) -> list[Headline]: ...
```

Implementations registered in a resolver:

```
ProviderRegistry
 ├── CoinGeckoProvider      (market data)   priority 1
 ├── BinanceProvider        (market data)   priority 2 (fallback)
 ├── MockMarketProvider     (market data)   demo mode / final fallback
 ├── CryptoPanicProvider    (news)          priority 1
 ├── MockNewsProvider       (news)          demo mode / fallback
 └── ...
```

Selection logic per request:

1. If `DEMO_MODE=true` → mock provider chain only (deterministic seeds, no network).
2. Else iterate providers by priority; first success wins.
3. Circuit breaker per provider (open after K consecutive failures, half-open probe after cooldown).
4. Every provider response is normalized to internal schemas before leaving the layer — no upstream shape leaks into business code.

Adding a provider = implementing the protocol + registering it + adding tests. No router changes.

## 6. ML Pipeline

```
raw candles ─▶ feature store view ─▶ train script ─▶ model registry
                                          │
                                          ▼
inference path: features ─▶ loaded model ─▶ action + confidence + SHAP-like attributions
```

Stages:

1. **Feature engineering** (`app/ml/features.py`)
   - Pure functions over candle frames: momentum, volatility, trend, volume, sentiment joins.
   - Deterministic and unit-tested; identical code path for training and inference (no training/serving skew).

2. **Training** (`scripts/train_model.py`, run offline or via scheduled job)
   - Walk-forward split (never random shuffle — temporal leakage guard).
   - Label: forward-return sign over horizon H, thresholded into BUY/HOLD/SELL.
   - Models: LightGBM primary, logistic regression baseline for sanity checks.
   - Metrics logged per fold: accuracy, F1 macro, precision@confidence≥0.7.

3. **Model registry**
   - Artifacts versioned under `models/` with metadata (features hash, train window, metrics).
   - Workers load the active version pinned by env/config; rollout = config flip.

4. **Inference**
   - Feature vector built with the exact same transformers → predict → calibrated confidence.
   - Attributions (feature importances per prediction) stored alongside the signal for explainability and audit.

5. **Monitoring**
   - Prediction distribution drift tracked daily; auto-alert when live accuracy vs. realized labels degrades below threshold.

## 7. Security Architecture

### Authentication & authorization
- Stateless JWT (HS256) access tokens, configurable expiry; refresh tokens rotated on use.
- Passwords hashed with bcrypt (cost factor configurable).
- Optional API-key scheme for machine clients, hashed at rest, scoped per environment.
- Route-level dependency guards: public routes, authenticated routes, admin routes.

### Transport & perimeter
- TLS terminated at the reverse proxy/load balancer in production; HSTS enforced there.
- CORS allow-list from `CORS_ORIGINS` — no wildcard origins in prod.
- Rate limiting per IP + per token in Redis sliding window (`RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW`).

### Input hardening
- Pydantic validation on every boundary; unknown fields rejected in strict models.
- ORM parameterized queries only — no string-built SQL anywhere.
- Request body size caps; upload endpoints (if enabled) validate content-type and magic bytes.

### Secrets management
- Secrets only via environment; `.env` git-ignored; `.env.example` contains placeholders only.
- Production requires explicit `SECRET_KEY` / `POSTGRES_PASSWORD` (compose fails fast if missing).
- Containers run as non-root users; read-only capability set; no secrets baked into images.

### Auditing
- Append-only `audit_log` table records auth events, admin actions, and trade-relevant signals with actor + timestamp.
- Logs structured (JSON), no PII or secrets in log lines.

### Threat model summary
| Threat | Mitigation |
|---|---|
| Credential stuffing | bcrypt + rate limits + lockout counters |
| Token theft | Short expiry, refresh rotation, HTTPS-only transport |
| SQL injection | ORM-only queries, validated params |
| Upstream provider compromise | Schema normalization, response validation at provider edge |
| Container escape surface | Non-root users, minimal base images, no privileged mode |

## 8. Scaling Strategy

### Vertical first, then horizontal per tier:

**API tier**
- Start: single container, 4 uvicorn workers.
- Scale: compose `--scale api=N` behind any TCP LB. Stateless — no sticky sessions required.
- Bottleneck signal: p95 latency > 300 ms while CPU < 60% → check DB pool exhaustion before adding replicas.

**Worker tier**
- Scale horizontally by concurrency (`-c N`) then by replica count.
- Queue routing separates fast tasks (price ingest) from slow ones (training) so head-of-line blocking can't starve latency-critical work.
- Idempotent tasks make retries safe; `acks_late` gives crash-safe redelivery.

**Database tier**
- TimescaleDB hypertables auto-partition `ohlcv`; compression on chunks older than 7 days (typical ~90% reduction).
- Continuous aggregates serve chart/resampling queries without touching raw chunks.
- Next step when needed: read replica for analytics queries; connection pooling via PgBouncer beyond ~200 client connections.

**Cache/bus tier**
- Redis single node comfortably serves this workload; move to Redis Sentinel (HA) or Cluster when persistence failover matters.
- Separate logical DBs: 0 cache, 1 broker, 2 results — allows independent eviction policies.

**Frontend tier**
- Fully stateless; static assets offloaded to CDN; ISR/streaming keeps TTFB low.

**Capacity envelope (reference hardware, 2 vCPU / 4 GB per service):**
- ~500 req/s API sustained with cache hit ratio ≥ 80%
- ~200 assets ingested per minute per worker process
- Signal generation for 200 assets in < 30 s per cycle

## 9. Key Design Decisions

| Decision | Rationale |
|---|---|
| Modular monolith API, not microservices | Single deployable reduces ops burden; module boundaries enforce separation; extract later if needed |
| TimescaleDB over plain PG partitioning | Native compression, continuous aggregates, time-bucket functions out of the box |
| Celery over asyncio background tasks | Durability, retries, scheduling, and horizontal scale for heavy jobs |
| Redis pub/sub for realtime, PG for durability | Ephemeral fanout cheap; audit needs persist anyway |
| Demo/mock providers as first-class citizens | Zero-friction onboarding, deterministic tests, CI runs without external dependencies |
| Strategy pattern for providers | Swappability, graceful degradation, trivial mocking |
