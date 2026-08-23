# Data Sources

Complete reference for every data provider the platform integrates, including rate limits, coverage, and how the provider abstraction handles them.

---

## Table of Contents

- [Provider Architecture](#provider-architecture)
- [CoinGecko](#coingecko)
- [Binance Public API](#binance-public-api)
- [CryptoPanic](#cryptopanic)
- [Etherscan](#etherscan)
- [Alchemy](#alchemy)
- [OpenAI (Enrichment)](#openai-enrichment)
- [Demo / Mock Providers](#demo--mock-providers)
- [Future Providers (Roadmap)](#future-providers-roadmap)
- [Comparison Matrix](#comparison-matrix)

---

## Provider Architecture

All providers implement shared protocols and are resolved at runtime:

```
ProviderRegistry
├── MarketDataProvider protocol
│   ├── CoinGeckoProvider      (primary market data)
│   ├── BinanceProvider        (fallback + orderbook depth)
│   └── MockMarketProvider     (demo mode / final fallback)
├── NewsProvider protocol
│   ├── CryptoPanicProvider    (aggregated crypto news)
│   └── MockNewsProvider       (demo mode / fallback)
├── OnChainProvider protocol
│   ├── EtherscanProvider      (Ethereum gas/transactions)
│   └── AlchemyProvider        (enhanced chain data)
└── LLMProvider protocol
    └── OpenAIProvider         (narrative summaries — optional)
```

**Resolution rules:**

1. `DEMO_MODE=true` → only mock providers (deterministic, zero network).
2. Otherwise providers are tried in priority order; first success wins.
3. Per-provider circuit breaker: opens after 5 consecutive failures, half-open probe after 60 s cooldown.
4. All responses normalized to internal schemas before leaving the provider layer.
5. Missing API keys never crash the system — the resolver skips unconfigured providers.

---

## CoinGecko

| Property | Value |
|---|---|
| Role | Primary market data: prices, OHLCV, market caps, volumes |
| Env var | `COINGECKO_API_KEY` (optional) |
| Free tier | Yes — ~10–30 calls/min depending on endpoint |
| Paid tier | Demo/Paid plans raise limits substantially |
| Docs | https://www.coingecko.com/en/api |

### Endpoints used

| Endpoint | Purpose | Poll cadence |
|---|---|---|
| `/coins/markets` | Top-market snapshot (price, cap, 24h volume/change) | 60 s |
| `/coins/{id}/ohlc` | Historical candles | on demand |
| `/coins/{id}/market_chart` | Price/volume time series | on demand |
| `/global` | Total market cap, BTC dominance | 10 min |
| `/search/trending` | Trending coins widget | 15 min |

### Notes & limits

- Without an API key you share the free-tier pool; expect occasional `429`s during peak hours. The retry layer uses exponential backoff with jitter and honors `Retry-After`.
- Symbols vs. IDs: CoinGecko uses slugs (`bitcoin`, not `BTC`). The registry maintains a symbol→slug map seeded with top assets and extended via `/search`.
- Attribution required by their ToS when displaying data publicly.

---

## Binance Public API

| Property | Value |
|---|---|
| Role | Fallback market data, klines, order book depth, 24h stats |
| Env vars | `BINANCE_API_KEY`, `BINANCE_API_SECRET` (optional — public endpoints need none) |
| Free tier | Public market data is free without authentication |
| Rate limit | Weight-based: 6,000 weight/min per IP (public data) |
| Docs | https://developers.binance.com/docs/binance-spot-api-docs |

### Endpoints used

| Endpoint | Purpose | Poll cadence |
|---|---|---|
| `GET /api/v3/klines` | OHLCV candles (1m → 1M intervals) | 60 s ingest loop |
| `GET /api/v3/ticker/24hr` | Rolling 24h statistics | 60 s |
| `GET /api/v3/depth` | Order book snapshots (top N levels) | on demand |
| `GET /api/v3/trades` | Recent trade prints | on demand |
| WS `<symbol>@trade` streams | Live price push (planned) | continuous |

### Notes & limits

- Public endpoints require no key; keys are only needed if trading endpoints get enabled later. Keys are read from env, never logged.
- Symbol format: `BTCUSDT`. The registry maps internal symbols to pairs automatically.
- Response weights vary by query size (`limit` parameter); the client budgets requests to stay under ~80% of the weight ceiling.
- Geographic restrictions apply in some jurisdictions — the circuit breaker treats persistent `451`s as a permanent disable signal rather than a transient failure.

---

## CryptoPanic

| Property | Value |
|---|---|
| Role | Aggregated crypto news headlines + sentiment votes for NLP pipeline |
| Env var | `CRYPTOPANIC_API_KEY` (optional) |
| Free tier | Yes — limited request rate, standard filters |
| Rate limit | Free: modest per-hour allowance; paid tiers scale up |
| Docs | https://cryptopanic.com/developers/api/ |

### Endpoints used

| Endpoint | Purpose | Poll cadence |
|---|---|
| `GET /api/v1/posts/?auth_token=...&currencies=BTC,ETH` | Latest headlines filtered by asset | 15 min |
| `GET /api/v1/posts/?filter=hot` | High-engagement stories | 15 min |

### Notes & limits

- Each post includes community sentiment votes (positive/negative) which we blend with our own NLP score as a weak label.
- Deduplication is by URL hash before storage — aggregators repost heavily.
- Headlines are stored raw alongside scores so models can be re-run retroactively.

---

## Etherscan

| Property | Value |
|---|---|
| Role | Ethereum on-chain activity: gas prices, transaction counts, contract events |
| Env var | `ETHERSCAN_API_KEY` (optional) |
| Free tier | Yes — 5 calls/sec, 100k calls/day |
| Docs | https://docs.etherscan.io/ |

### Endpoints used

| Endpoint module | Purpose | Poll cadence |
|---|---|---|
| `gastracker` | Current safe/proposed/fast gas | 60 s |
| `stats` | ETH supply, price feed cross-check | 10 min |
| `account → txlist` | Address activity features (whale watch) | hourly |

### Notes & limits

- Free key is sufficient for all current usage patterns; the client enforces a strict 4 req/sec self-throttle to stay compliant.
- On-chain features currently feed the feature store for ETH-family assets; multi-chain support routes through the same `OnChainProvider` protocol.

---

## Alchemy

| Property | Value |
|---|---|
| Role | Enhanced on-chain data: NFT metrics, token transfers, webhooks (roadmap) |
| Env var | `ALCHEMY_API_KEY` (optional) |
| Free tier | Generous monthly compute-unit allowance |
| Docs | https://docs.alchemy.com/ |

### Status

Registered in the provider registry but **not yet active** in any pipeline. Planned usage:

- Token transfer volume per contract (on-chain momentum features)
- Webhook-based event ingestion instead of polling
- Multi-chain expansion beyond Ethereum mainnet

---

## OpenAI (Enrichment)

| Property | Value |
|---|---|
| Role | Narrative summaries of signals ("why is BTC flagged SELL today?") |
| Env var | `OPENAI_API_KEY` (optional) |
| Cost | Pay-per-token; summaries generated lazily and cached |
| Docs | https://platform.openai.com/docs/ |

### Behavior

- When configured, signal detail views include a plain-language explanation generated from structured feature attributions.
- **Never** used for decisions — the ML model output is deterministic; the LLM only verbalizes stored attributions.
- Cached aggressively (per signal id); failures degrade gracefully to template text.
- Prompt-injection guard: only numeric/enum feature values enter prompts, never raw scraped text.

---

## Demo / Mock Providers

| Property | Value |
|---|---|
| Role | Deterministic synthetic data for demo mode, tests, CI |
| Activation | `DEMO_MODE=true` or missing real providers |
| Network calls | **None** |

### Design

Mock providers generate realistic-but-synthetic series using seeded randomness (fixed seed → identical data across runs):

```
seed = stable_hash(symbol)
base_price = lookup_table[symbol]           # plausible anchor (e.g., BTC ≈ 65k)
series(t) = base × drift(t) × seasonal(t) × noise(seed, t)
```

Properties guaranteed by design:

- **Deterministic** — same inputs, byte-identical outputs (golden-file testable).
- **Plausible** — volatility regimes, trend segments, and volume correlations mimic real markets enough to exercise charts, indicators, and ML paths meaningfully.
- **Fast** — pure computation, microsecond latency.

### What demo mode covers

- Full OHLCV history for ~50 assets
- Synthetic headlines with pre-scored sentiment
- Signal generation end-to-end through the real ML path (trained on synthetic data)
- WebSocket events firing on schedule

Demo mode exists so that: onboarding requires zero setup, CI runs hermetically, and UI development never blocks on upstream API changes.

---

## Future Providers (Roadmap)

Candidates under evaluation, in rough priority:

| Provider | Type | Why |
|---|---|---|
| Coinbase Exchange API | Market data | Redundant second venue, regulated-market pricing |
| Kraken Public API | Market data | Additional fallback diversity |
| Messari | Fundamentals | Project metrics, TVL, developer activity |
| Santiment | Social + on-chain | Combined social dominance & network growth |
| LunarCrush | Social | Galaxy score, influencer activity |
| Glassnode | On-chain | Institutional-grade chain metrics (paid) |
| DefiLlama | DeFi | TVL series across chains (free) |
| The Graph | Indexing | Subgraph queries for protocol-level events |
| Twitter/X API | Social | Real-time mention velocity (expensive, gated) |
| Reddit API | Social | Subreddit activity for retail sentiment |
| FRED/Macro APIs | Macro | DXY, rates as exogenous features |
| Solana RPC clusters | On-chain | Multi-chain expansion |
| CoinAPI / Kaiko | Aggregator | Single-key multi-venue normalization (paid) |

Integration cost is intentionally low: implement one protocol class, register it, add tests. See [ARCHITECTURE.md §5](ARCHITECTURE.md#5-provider-abstraction).

---

## Comparison Matrix

| Provider | Data type | Auth needed | Free tier usable | Active in pipelines |
|---|---|---|---|---|
| CoinGecko | Prices/OHLCV/market | No (key optional) | ✅ | ✅ Primary |
| Binance | Klines/orderbook/stats | No (public) | ✅ | ✅ Fallback |
| CryptoPanic | News/sentiment votes | Yes (free key) | ✅ | ✅ Primary |
| Etherscan | ETH on-chain | Yes (free key) | ✅ | ✅ Primary |
| Alchemy | Rich on-chain | Yes (free key) | ✅ | 🔜 Registered |
| OpenAI | Narrative enrichment | Yes (paid) | ❌ | ⭕ Optional |
| Mock/Demo | Everything | No | ✅ | ✅ Always available |

## Adding a New Provider

1. Implement the relevant protocol in `apps/api/app/providers/<name>_provider.py`
2. Register it in the `ProviderRegistry` with priority
3. Add unit tests with mocked HTTP + a contract test against the protocol
4. Document env vars here and in `.env.example`
5. Update this file's matrix above

No changes to routers, services, or workers should be necessary — that's the point of the abstraction.
