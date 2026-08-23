<div align="center">

# Crypto Intelligence & AI Trading Decision Platform

**AI-powered crypto market intelligence with real-time signals, sentiment analysis, and decision support.**

[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](.github/workflows/ci.yml)
[![CD](https://img.shields.io/badge/CD-main-blue)](.github/workflows/cd.yml)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-latest-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14-black?logo=next.js)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-TimescaleDB-336791?logo=postgresql&logoColor=white)](https://www.timescale.com/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?logo=redis&logoColor=white)](https://redis.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

</div>

---

A production-grade platform that aggregates cryptocurrency market data, on-chain metrics, and news sentiment, then applies ML models to generate **buy / sell / hold decisions** with confidence scores — all explainable, all auditable.

> **Demo Mode:** The entire system runs with zero API keys using deterministic mock providers. Drop in real keys whenever you're ready.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          CLIENTS                                     │
│              (Browser · Mobile · Bots · Dashboards)                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 │ HTTPS / WSS
                    ┌────────────▼─────────────┐
                    │   Next.js 14 Frontend    │
                    │   apps/web :3000         │
                    │   SSR · Charts · Alerts  │
                    └────────────┬─────────────┘
                                 │ REST
┌────────────────────────────────▼────────────────────────────────────┐
│                     FastAPI Gateway  apps/api :8000                  │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────────┐ │
│  │  Auth    │ │ Markets  │ │ Signals  │ │ Sentiment│ │ Portfolio │ │
│  │  Router  │ │  Router  │ │  Router  │ │  Router  │ │  Router   │ │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘ └─────┬─────┘ │
│       │            │            │            │             │        │
│  ┌────▼────────────▼────────────▼────────────▼─────────────▼─────┐ │
│  │           Provider Abstraction Layer (Strategy Pattern)        │ │
│  │   CoinGecko │ Binance │ CryptoPanic │ Etherscan │ Mock/Demo    │ │
│  └────────────────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  JWT Auth · Rate Limiting · CORS · Validation · Observability  │ │
│  └────────────────────────────────────────────────────────────────┘ │
└──────────────┬───────────────────────────────────────┬──────────────┘
               │                                       │
      ┌────────▼─────────┐                   ┌─────────▼──────────┐
      │   PostgreSQL     │                   │      Redis          │
      │  + TimescaleDB   │◄──── Celery ────►│  Broker / Cache     │
      │  Timeseries OHLCV│      Tasks        │  Pub/Sub · Locks    │
      │  :5432           │                   │  :6379              │
      └────────▲─────────┘                   └─────────┬──────────┘
               │                                       │
      ┌────────┴───────────────────────────────────────▼──────────┐
      │                 Background Processing                      │
      │  ┌─────────────────────┐   ┌────────────────────────────┐ │
      │  │  Celery Workers (-c2)│   │  Celery Beat (Scheduler)  │ │
      │  │  · price ingestion   │   │  · every 60s: prices      │ │
      │  │  · signal generation │   │  · every 15m: sentiment   │ │
      │  │  · ML scoring        │   │  · hourly: retrain eval   │ │
      │  └─────────────────────┘   └────────────────────────────┘ │
      └────────────────────────────────────────────────────────────┘

External Providers:  CoinGecko · Binance · CryptoPanic · Etherscan · OpenAI
```

## Features

### Market Data
- Real-time & historical OHLCV ingestion (TimescaleDB hypertables)
- Multi-provider fallback chain with automatic failover
- Live order book snapshots from Binance public streams
- Deterministic mock providers for full offline/demo operation

### Intelligence Layer
- **Signal Engine** — composite technical indicators (RSI, MACD, Bollinger, EMA crossovers)
- **Sentiment Analysis** — NLP over news headlines + social mentions, aggregated per asset
- **ML Decision Models** — gradient-boosted classifiers producing BUY/SELL/HOLD + confidence
- **Explainability** — every signal ships feature attributions, not black-box scores

### Platform
- Async FastAPI gateway with OpenAPI docs auto-generated
- JWT auth with refresh rotation; API-key auth for programmatic access
- Redis-backed rate limiting and response caching
- Celery task pipeline with scheduled ingestion via Beat
- WebSocket push for live prices and alert events

### Developer Experience
- One-command Docker startup, hot reload in dev mode
- Full test pyramid: unit → integration → e2e smoke
- CI: lint + typecheck + tests + security scan + docker build
- Seeded demo data for instant exploration

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| API | Python 3.12, FastAPI, Pydantic v2 | Async REST gateway |
| DB | PostgreSQL 16 + TimescaleDB | Relational + timeseries storage |
| Cache/Broker | Redis 7 | Caching, Celery broker, pub/sub |
| Workers | Celery | Async ingestion & ML jobs |
| Frontend | Next.js 14, React 18, TypeScript | Dashboard UI |
| Charts | TradingView Lightweight Charts | Price visualization |
| ML | scikit-learn, LightGBM, pandas | Signal models |
| LLM (optional) | OpenAI API | Narrative summaries |
| Infra | Docker Compose | Orchestration |
| CI/CD | GitHub Actions | Pipelines |
| QA | ruff, mypy, pytest, eslint | Quality gates |

## Quick Start

> Prerequisites: [Docker](https://docs.docker.com/get-docker/) 24+ and Docker Compose v2. That's it.

```bash
# 1. Clone
git clone https://github.com/your-org/crypto-intelligence-platform.git
cd crypto-intelligence-platform

# 2. Configure (demo mode works out of the box)
cp .env.example .env

# 3. Launch everything
docker compose up -d --build

# 4. Seed demo data
docker compose exec api python /app/scripts_seed.py || python scripts/seed.py
```

Open:
- **Dashboard** → http://localhost:3000
- **API Docs (Swagger)** → http://localhost:8000/docs
- **API Docs (ReDoc)** → http://localhost:8000/redoc
- **Health Check** → http://localhost:8000/health

Verify everything:

```bash
bash scripts/health-check.sh
```

## Docker Setup

```bash
# Development — hot reload for both API and web
docker compose -f docker-compose.yml -f docker-compose.dev.yml up

# Production — resource limits, restart policies, replicas
cp .env.example .env   # then set SECRET_KEY, POSTGRES_PASSWORD!
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Scale workers independently
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale worker=4

# Tail logs
docker compose logs -f api worker scheduler

# Rebuild after dependency changes
docker compose build --no-cache api web
```

Service map:

| Service | Port | Description |
|---|---|---|
| `web` | 3000 | Next.js dashboard |
| `api` | 8000 | FastAPI gateway |
| `postgres` | 5432 | TimescaleDB |
| `redis` | 6379 | Broker + cache |
| `worker` | — | Celery workers |
| `scheduler` | — | Celery beat |

## Development Setup (without Docker)

<details>
<summary><b>Backend</b></summary>

```bash
cd apps/api
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt

uvicorn app.main:app --reload --port 8000
celery -A app.workers.celery_app worker -l info
celery -A app.workers.celery_app beat -l info
```

</details>

<details>
<summary><b>Frontend</b></summary>

```bash
cd apps/web
npm install
npm run dev   # http://localhost:3000
npm run build && npm start
```

</details>

<details>
<summary><b>Quality gates</b></summary>

```bash
# Python
ruff check apps/api && ruff format --check apps/api
mypy apps/api
pytest apps/api/tests -v --cov

# TypeScript
cd apps/web && npm run lint && npx tsc --noEmit
```

</details>

## Environment Variables

Copy `.env.example` → `.env` and adjust. Key variables:

| Variable | Default | Required | Notes |
|---|---|---|---|
| `DATABASE_URL` | localhost pg | ✅ | asyncpg driver in URL |
| `REDIS_URL` | localhost | ✅ | db 0 = cache |
| `SECRET_KEY` | change-me | ✅ prod | Generate: `openssl rand -hex 32` |
| `DEMO_MODE` | `true` | — | Uses mock providers when true |
| `CORS_ORIGINS` | localhost:3000 | — | Comma-separated |
| `COINGECKO_API_KEY` | empty | optional | Free tier works without it |
| `OPENAI_API_KEY` | empty | optional | Enables narrative summaries |
| `CELERY_BROKER_URL` | redis db1 | ✅ | Separate from cache db |

Full reference with all variables: see [`.env.example`](.env.example).

## API Documentation

Interactive docs ship with the API itself:
- Swagger UI: **http://localhost:8000/docs**
- ReDoc: **http://localhost:8000/redoc**
- OpenAPI JSON: **http://localhost:8000/openapi.json**

Full endpoint reference with curl examples: **[API.md](API.md)**

Quick taste:

```bash
curl http://localhost:8000/health
curl "http://localhost:8000/api/v1/markets/bitcoin?days=7"
curl "http://localhost:8000/api/v1/signals/BTC"
curl "http://localhost:8000/api/v1/sentiment/ETH"
```

## Project Structure

```
crypto-intelligence-platform/
├── apps/
│   ├── api/                      # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py           # App entrypoint
│   │   │   ├── core/             # Config, security, logging
│   │   │   ├── routers/          # API endpoints
│   │   │   ├── services/         # Business logic
│   │   │   ├── providers/        # Data provider abstraction
│   │   │   ├── models/           # SQLAlchemy ORM models
│   │   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── workers/          # Celery tasks & beat schedule
│   │   │   └── ml/               # Feature engineering + models
│   │   ├── tests/                # pytest suites
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   └── web/                      # Next.js frontend
│       ├── src/
│       │   ├── app/              # App router pages
│       │   ├── components/       # UI components
│       │   ├── hooks/            # React hooks
│       │   └── lib/              # API client, utils
│       ├── package.json
│       └── Dockerfile
├── database/
│   ├── schemas/                  # Reference SQL schema
│   └── seeds/                    # Demo seed data
├── scripts/
│   ├── setup.sh                  # First-run setup
│   ├── seed.py                   # Demo data seeder
│   └── health-check.sh           # Service verification
├── .github/
│   ├── workflows/                # CI & CD pipelines
│   └── ISSUE_TEMPLATE/           # Bug & feature templates
├── docker-compose.yml            # Base services
├── docker-compose.dev.yml        # Dev overrides (hot reload)
├── docker-compose.prod.yml       # Prod overrides (limits)
├── .env.example                  # Env template
├── ARCHITECTURE.md               # Deep-dive design doc
├── DEPLOYMENT.md                 # Deployment guide
├── DATA_SOURCES.md               # Provider documentation
├── API.md                        # Endpoint reference
├── CONTRIBUTING.md               # Contribution guide
├── SECURITY.md                   # Security policy
└── LICENSE                       # MIT
```

## Contributing

Contributions welcome! Read [CONTRIBUTING.md](CONTRIBUTING.md) first. TL;DR:

1. Fork → branch (`feat/my-feature`)
2. Make changes, add tests
3. Run quality gates locally (`ruff`, `mypy`, `pytest`, `eslint`)
4. Open a PR against `main` — CI must pass

Found a security issue? Do **not** open a public issue — follow [SECURITY.md](SECURITY.md).

## License

Released under the [MIT License](LICENSE). See LICENSE for details.

---

<div align="center">
<i>This software is provided for educational and research purposes. Nothing here is financial advice.</i>
</div>
