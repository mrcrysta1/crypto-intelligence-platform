# API Documentation

REST API reference for the Crypto Intelligence Platform.

- **Base URL:** `http://localhost:8000`
- **Interactive docs:** http://localhost:8000/docs (Swagger) · http://localhost:8000/redoc (ReDoc)
- **OpenAPI spec:** http://localhost:8000/openapi.json
- **Versioning:** all business routes are prefixed `/api/v1`

---

## Authentication

Most read endpoints are public. Write endpoints and user-scoped resources require a JWT bearer token.

### Obtain a token

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "demo@example.com", "password": "S3curePassw0rd!"}'

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=S3curePassw0rd!"
```

Response:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "expires_in": 86400
}
```

### Use the token

```bash
curl http://localhost:8000/api/v1/portfolio \
  -H "Authorization: Bearer <access_token>"
```

Tokens expire after `JWT_EXPIRATION_HOURS` (default 24). Refresh:

```bash
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

---

## Error Format

All errors share one envelope:

```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Asset 'xyzcoin' not found",
    "details": {},
    "request_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7"
  }
}
```

| HTTP | Code | Meaning |
|---|---|---|
| 400 | `BAD_REQUEST` | Malformed input |
| 401 | `UNAUTHORIZED` | Missing/expired token |
| 403 | `FORBIDDEN` | Insufficient permissions |
| 404 | `NOT_FOUND` | Resource doesn't exist |
| 422 | `VALIDATION_ERROR` | Schema validation failed (includes field details) |
| 429 | `RATE_LIMITED` | Rate limit exceeded (see `Retry-After` header) |
| 500 | `INTERNAL_ERROR` | Server fault (request_id for log correlation) |
| 503 | `PROVIDER_UNAVAILABLE` | All upstream providers failed |

---

## Health & System

### `GET /health`

Liveness probe. No auth.

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "ok",
  "version": "1.0.0",
  "environment": "development",
  "demo_mode": true
}
```

### `GET /ready`

Readiness — actively checks DB + Redis round-trips. Returns `503` when dependencies are unreachable.

```json
{
  "status": "ready",
  "checks": { "database": "ok", "redis": "ok" }
}
```

### `GET /metrics`

Prometheus-format metrics (when instrumentation enabled).

---

## Markets

### `GET /api/v1/markets`

List tracked assets with current market snapshot.

**Query params:**

| Param | Type | Default | Description |
|---|---|---|---|
| `limit` | int | 50 | Max results (1–250) |
| `offset` | int | 0 | Pagination offset |
| `sort` | string | `market_cap_desc` | Sort key |
| `search` | string | — | Filter by name/symbol |

```bash
curl "http://localhost:8000/api/v1/markets?limit=5"
```

```json
{
  "items": [
    {
      "symbol": "BTC",
      "name": "Bitcoin",
      "price": 67412.55,
      "change_24h_pct": 2.31,
      "market_cap": 1328900000000,
      "volume_24h": 34210000000,
      "updated_at": "2026-08-24T10:32:11Z"
    }
  ],
  "total": 200,
  "limit": 5,
  "offset": 0
}
```

### `GET /api/v1/markets/{symbol}`

Full detail for one asset.

```bash
curl http://localhost:8000/api/v1/markets/bitcoin
```

### `GET /api/v1/markets/{symbol}/history`

Historical OHLCV from the TimescaleDB hypertable.

**Query params:** `days` (default 30, max 365), `interval` (`1m`, `5m`, `15m`, `1h`, `4h`, `1d`)

```bash
curl "http://localhost:8000/api/v1/markets/BTC/history?days=7&interval=1h"
```

```json
{
  "symbol": "BTC",
  "interval": "1h",
  "candles": [
    {"ts": "2026-08-17T00:00:00Z", "open": 65120.1, "high": 65580.9,
     "low": 64901.2, "close": 65344.7, "volume": 2841.22}
  ]
}
```

### `GET /api/v1/markets/{symbol}/orderbook`

Top-of-book depth snapshot (Binance-backed; demo data in demo mode).

```bash
curl "http://localhost:8000/api/v1/markets/BTC/orderbook?depth=10"
```

---

## Signals

### `GET /api/v1/signals/{symbol}`

Latest AI decision signal with feature attributions.

```bash
curl http://localhost:8000/api/v1/signals/BTC
```

```json
{
  "symbol": "BTC",
  "action": "BUY",
  "confidence": 0.78,
  "generated_at": "2026-08-24T10:35:00Z",
  "model_version": "lgbm-v14",
  "horizon_hours": 24,
  "features": [
    {"name": "rsi_14",          "value": 38.2,  "contribution": -0.21},
    {"name": "macd_histogram",  "value": 41.7,  "contribution": 0.18},
    {"name": "ema_cross_score", "value": 0.73,  "contribution": 0.24},
    {"name": "sentiment_score", "value": 0.61,  "contribution": 0.15},
    {"name": "volume_zscore",   "value": 1.9,   "contribution": 0.09}
  ],
  "explanation": "EMA bullish cross with rising MACD momentum; RSI shows room to run before overbought."
}
```

### `GET /api/v1/signals`

Paginated signal history across assets.

**Query params:** `symbols=BTC,ETH`, `action=BUY`, `min_confidence=0.7`, `since=2026-08-20T00:00:00Z`, `limit`, `offset`

```bash
curl "http://localhost:8000/api/v1/signals?action=BUY&min_confidence=0.75&limit=10"
```

### `POST /api/v1/signals/{symbol}/refresh`

Force immediate re-computation (auth required). Enqueues the ML pipeline task and returns task id.

```bash
curl -X POST http://localhost:8000/api/v1/signals/ETH/refresh \
  -H "Authorization: Bearer $TOKEN"
```

```json
{ "task_id": "a3f8c2e1-...", "status": "queued" }
```

---

## Sentiment

### `GET /api/v1/sentiment/{symbol}`

Aggregated sentiment snapshot + recent scored headlines.

```bash
curl http://localhost:8000/api/v1/sentiment/BTC
```

```json
{
  "symbol": "BTC",
  "score": 0.62,
  "label": "bullish",
  "window_hours": 24,
  "sample_size": 47,
  "sources_breakdown": {"news": 31, "social": 16},
  "headlines": [
    {
      "title": "Spot ETF inflows hit new weekly record",
      "source": "CryptoPanic",
      "url": "https://...",
      "published_at": "2026-08-24T09:12:00Z",
      "score": 0.83
    }
  ],
  "trend": [0.31, 0.44, 0.58, 0.62]
}
```

### `GET /api/v1/sentiment/trending`

Assets ranked by absolute sentiment velocity.

```bash
curl "http://localhost:8000/api/v1/sentiment/trending?limit=10"
```

---

## Portfolio (auth required)

### `GET /api/v1/portfolio`

Current user's positions with live marks and P&L.

```bash
curl http://localhost:8000/api/v1/portfolio -H "Authorization: Bearer $TOKEN"
```

```json
{
  "positions": [
    {
      "symbol": "BTC",
      "quantity": 0.5,
      "avg_entry_price": 61800.00,
      "current_price": 67412.55,
      "unrealized_pnl": 2806.27,
      "unrealized_pnl_pct": 9.08
    }
  ],
  "total_value_usd": 33706.28,
  "total_unrealized_pnl": 2806.27
}
```

### `POST /api/v1/portfolio/positions`

Add or adjust a position.

```bash
curl -X POST http://localhost:8000/api/v1/portfolio/positions \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "ETH", "quantity": 2.5, "entry_price": 3120.50}'
```

### `DELETE /api/v1/portfolio/positions/{id}`

Remove a position.

### `GET /api/v1/portfolio/performance?days=30`

Equity curve + aggregate stats (Sharpe, max drawdown, win rate on signals followed).

---

## Alerts (auth required)

### `POST /api/v1/alerts`

Create an alert rule.

```bash
curl -X POST http://localhost:8000/api/v1/alerts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"type": "price_above", "symbol": "BTC", "threshold": 70000}'
```

Supported types: `price_above`, `price_below`, `pct_change_24h`, `signal_action`, `sentiment_threshold`.

### `GET /api/v1/alerts` · `DELETE /api/v1/alerts/{id}`

List and cancel rules. Triggered alerts appear in `GET /alerts/triggers` and push over WebSocket.

---

## WebSocket API

Live updates over `ws://localhost:8000/ws/stream`.

### Subscribe protocol

Client → server:

```json
{"action": "subscribe",   "channels": ["prices", "signals:BTC", "sentiment:ETH"]}
{"action": "unsubscribe", "channels": ["signals:BTC"]}
```

Server → client events:

```json
{"event": "price.updated",    "data": {"symbol": "BTC", "price": 67488.10}}
{"event": "signal.created",   "data": {"symbol": "ETH", "action": "BUY", "confidence": 0.71}}
{"event": "sentiment.update", "data": {"symbol": "SOL", "score": -0.24, "label": "bearish"}}
{"event": "alert.triggered",  "data": {"alert_id": 42, "message": "BTC crossed above $70,000"}}
```

Heartbeat: server sends `ping` every 30 s; clients should respond with `pong`. Idle connections without pong are reaped after 90 s.

Quick test:

```bash
npx wscat -c ws://localhost:8000/ws/stream
> {"action":"subscribe","channels":["prices"]}
```

---

## Rate Limiting

Redis sliding-window limiter applied per IP (and per token where authenticated).

| Setting | Env var | Default |
|---|---|---|
| Max requests | `RATE_LIMIT_REQUESTS` | 100 |
| Window seconds | `RATE_LIMIT_WINDOW` | 60 |

Responses include headers:

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1724500331
```

On breach: `429` with `Retry-After` header.

---

## Pagination Convention

List endpoints use limit/offset consistently:

```json
{ "items": [...], "total": 200, "limit": 50, "offset": 0 }
```

Max page size is endpoint-specific (usually 250).

---

## SDK Snippets

<details>
<summary><b>Python</b></summary>

```python
import httpx

BASE = "http://localhost:8000"

async with httpx.AsyncClient(base_url=BASE) as c:
    markets = (await c.get("/api/v1/markets", params={"limit": 10})).raise_for_status().json()
    signal  = (await c.get("/api/v1/signals/BTC")).raise_for_status().json()

if signal["action"] == "BUY" and signal["confidence"] >= 0.7:
    print(f"Strong BUY on BTC ({signal['confidence']:.0%})")
```
</details>

<details>
<summary><b>TypeScript</b></summary>

```typescript
const BASE = "http://localhost:8000";

export async function getSignal(symbol: string) {
  const res = await fetch(`${BASE}/api/v1/signals/${symbol}`);
  if (!res.ok) throw new Error(`Signal fetch failed: ${res.status}`);
  return res.json() as Promise<{
    symbol: string;
    action: "BUY" | "SELL" | "HOLD";
    confidence: number;
    generated_at: string;
  }>;
}
```
</details>

---

*This document mirrors the auto-generated OpenAPI schema. If they ever diverge, the live docs at `/docs` are canonical.*
