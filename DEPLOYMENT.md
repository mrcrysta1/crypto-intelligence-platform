# Deployment Guide

Complete guide for deploying the Crypto Intelligence & AI Trading Decision Platform across environments.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [1. Local Development](#1-local-development)
- [2. Docker Deployment (Single Host)](#2-docker-deployment-single-host)
- [3. Cloud Deployment (Generic)](#3-cloud-deployment-generic)
- [Database Migrations](#database-migrations)
- [Zero-Downtime Updates](#zero-downtime-updates)
- [Backup & Recovery](#backup--recovery)
- [Monitoring & Observability](#monitoring--observability)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

| Requirement | Minimum | Notes |
|---|---|---|
| Docker Engine | 24.0 | Compose v2 built in |
| CPU | 2 vCPU | 4+ recommended for prod |
| RAM | 4 GB | 8 GB recommended for prod |
| Disk | 20 GB | Timeseries grows over time; enable compression |
| OS | Any Docker-capable | Linux recommended for prod |

Generate production secrets before any non-demo deployment:

```bash
openssl rand -hex 32   # → SECRET_KEY
openssl rand -hex 24   # → POSTGRES_PASSWORD
```

---

## 1. Local Development

### 1.1 Full stack with hot reload

```bash
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

What you get:

| URL | Service |
|---|---|
| http://localhost:3000 | Next.js dashboard (fast refresh) |
| http://localhost:8000/docs | Swagger UI |
| http://localhost:8000/redoc | ReDoc |
| http://localhost:8080 | Adminer (DB UI) — `profiles: ["debug"]` |
| http://localhost:5540 | Redis Insight — `profiles: ["debug"]` |

Debug tools are opt-in:

```bash
docker compose -f docker-compose.yml -f docker-compose.dev.yml \
  --profile debug up adminer redis-insight
```

### 1.2 Backend-only workflow (no Docker)

```bash
# Infra only
docker compose up -d postgres redis

cd apps/api
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt

uvicorn app.main:app --reload --port 8000          # terminal 1
celery -A app.workers.celery_app worker -l info    # terminal 2
celery -A app.workers.celery_app beat -l info      # terminal 3
```

### 1.3 Seed demo data

```bash
docker compose exec api python scripts_seed.py 2>/dev/null || python scripts/seed.py
# or against a running stack:
python scripts/seed.py
```

### 1.4 Verify health

```bash
bash scripts/health-check.sh
```

---

## 2. Docker Deployment (Single Host)

Suitable for VPS / dedicated box deployments (DigitalOcean, Hetzner, EC2, etc.).

### 2.1 Prepare environment

```bash
git clone https://github.com/your-org/crypto-intelligence-platform.git
cd crypto-intelligence-platform

cat > .env <<EOF
DATABASE_URL=postgresql+asyncpg://crypto:$(openssl rand -hex 24)@postgres:5432/crypto_intelligence
REDIS_URL=redis://redis:6379/0
SECRET_KEY=$(openssl rand -hex 32)
POSTGRES_PASSWORD=$(openssl rand -hex 24)
DEMO_MODE=false
LOG_LEVEL=WARNING
CORS_ORIGINS=https://your-domain.com
NEXT_PUBLIC_API_URL=https://api.your-domain.com
EOF
chmod 600 .env
```

### 2.2 Launch production stack

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml pull || true
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

The prod overlay adds:
- Restart policies (`always` for data services, `on-failure` for apps)
- CPU/memory limits and reservations per service
- JSON log rotation (size-capped)
- API scaled to 2 replicas, workers to 2 replicas
- Redis persistence (AOF) + memory ceiling with LRU eviction
- Postgres tuning for larger buffers/connection counts

### 2.3 Reverse proxy + TLS (Caddy example)

```caddyfile
your-domain.com {
    reverse_proxy web:3000
}

api.your-domain.com {
    reverse_proxy api:8000
}
```

```bash
# Attach proxy to compose network
docker network create caddy_net 2>/dev/null || true
docker run -d --name caddy --network caddy_net \
  -p 80:80 -p 443:443 \
  -v $PWD/Caddyfile:/etc/caddy/Caddyfile \
  -v caddy_data:/data \
  caddy:2-alpine
```

Nginx/Traefik work equally well — terminate TLS, forward to `web:3000` and `api:8000`.

### 2.4 Scale on demand

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --scale worker=4 --scale api=3
```

> Note: `scheduler` must stay at exactly **one** replica (Beat is not multi-instance safe).

### 2.5 Security hardening checklist

- [ ] Remove host port bindings for `postgres` and `redis` in prod (or firewall them):
  ```yaml
  # In your own override file:
  postgres:
    ports: []   # internal network only
  redis:
    ports: []
  ```
- [ ] `DEMO_MODE=false` confirmed
- [ ] TLS enforced, HSTS enabled at proxy
- [ ] Firewall: only 80/443 (and SSH) exposed
- [ ] Automated unattended-upgrades for the host OS
- [ ] Log shipping configured

---

## 3. Cloud Deployment (Generic)

The stack is cloud-agnostic. Reference mapping for common providers:

### 3.1 Managed service mapping

| Component | AWS | GCP | Azure | Generic alternative |
|---|---|---|---|---|
| Container hosting | ECS Fargate / App Runner | Cloud Run | Container Apps | Any Kubernetes |
| PostgreSQL (+Timescale) | RDS PG16 + manual TS extension | Cloud SQL | Azure DB for PG | Timescale Cloud |
| Redis | ElastiCache | Memorystore | Azure Cache | Upstash |
| Registry | ECR | Artifact Registry | ACR | GHCR / Docker Hub |
| Secrets | Secrets Manager | Secret Manager | Key Vault | SOPS / Doppler |
| CDN/WAF | CloudFront + WAF | Cloud CDN + Armor | Front Door | Cloudflare |

### 3.2 Build & push images (CI-built)

```bash
export REGISTRY=ghcr.io/your-org
export TAG=v1.0.0

docker build -f apps/api/Dockerfile --target runtime -t $REGISTRY/crypto-api:$TAG .
docker build -f apps/web/Dockerfile --target production \
  --build-arg NEXT_PUBLIC_API_URL=https://api.your-domain.com \
  -t $REGISTRY/crypto-web:$TAG .

echo "$REGISTRY_TOKEN" | docker login ghcr.io -u your-org --password-stdin
docker push $REGISTRY/crypto-api:$TAG
docker push $REGISTRY/crypto-web:$TAG
```

(The CD pipeline in `.github/workflows/cd.yml` automates this on every tag.)

### 3.3 Kubernetes sketch (any provider)

```yaml
# Example deployment shape — adapt labels/probes to your cluster conventions
apiVersion: apps/v1
kind: Deployment
metadata:
  name: crypto-api
spec:
  replicas: 3
  selector: {matchLabels: {app: crypto-api}}
  template:
    metadata:
      labels: {app: crypto-api}
    spec:
      containers:
        - name: api
          image: ghcr.io/your-org/crypto-api:v1.0.0
          ports: [{containerPort: 8000}]
          envFrom:
            - secretRef: {name: crypto-secrets}
            - configMapRef: {name: crypto-config}
          readinessProbe:
            httpGet: {path: /health, port: 8000}
            initialDelaySeconds: 10
          livenessProbe:
            httpGet: {path: /health, port: 8000}
            initialDelaySeconds: 20
          resources:
            requests: {cpu: 250m, memory: 256Mi}
            limits: {cpu: "1500m", memory: 1Gi}
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: crypto-api
spec:
  scaleTargetRef: {apiVersion: apps/v1, kind: Deployment, name: crypto-api}
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource: {name: cpu, target: {type: Utilization, averageUtilization: 70}}
```

Celery on K8s:

- `worker` → Deployment (HPA on queue depth via KEDA optional)
- `beat` → **Deployment with `replicas: 1`** (use leader election or a StatefulSet if you need HA beat)

### 3.4 Serverless notes

- The FastAPI app is stateless and containerized — deploys cleanly to Cloud Run / App Runner.
- Celery requires long-running processes: keep workers on always-on compute (don't serverless them).
- WebSocket support: verify your platform supports it before relying on live-push features; otherwise the frontend gracefully falls back to polling.

---

## Database Migrations

Alembic manages schema evolution:

```bash
cd apps/api

# Generate migration after model changes
alembic revision --autogenerate -m "add alerts table"

# Apply (local / docker exec into api container)
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

In Docker:

```bash
docker compose exec api alembic upgrade head
```

**Rules:**
- Never edit an applied migration.
- Every migration must have a tested downgrade path.
- Breaking migrations ship in two phases when zero-downtime matters (expand → contract).

## Zero-Downtime Updates

```bash
# 1. Migrate DB (expand phase — backward compatible)
docker compose exec api alembic upgrade head

# 2. Rolling restart of stateless tiers
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --no-deps --build api worker web

# 3. Verify health between steps
bash scripts/health-check.sh

# 4. Contract-phase migration if needed (after all old instances drained)
docker compose exec api alembic upgrade <contract-revision>
```

## Backup & Recovery

```bash
# Nightly logical backup (cron this)
docker compose exec postgres pg_dump -U crypto -Fc crypto_intelligence > backup_$(date +%F).dump

# Restore
cat backup_2026-08-24.dump | docker compose exec -T postgres pg_restore -U crypto -d crypto_intelligence --clean --if-exists

# Volume snapshot alternative (faster, point-in-time needs WAL archiving)
docker run --rm -v crypto-intelligence-platform_pgdata:/data -v $PWD/backups:/backup alpine \
  tar czf /backup/pgdata_$(date +%F).tar.gz -C /data .
```

Retention recommendation: daily backups ×14, weekly ×8, monthly ×12. Test restores quarterly.

## Monitoring & Observability

Built-in:

- `GET /health` — liveness (all critical deps checked)
- `GET /ready` — readiness (DB + Redis round-trips)
- Structured JSON logs on stdout — ship with any log collector

Suggested stack additions:

| Concern | Tool suggestion |
|---|---|
| Metrics scrape | Prometheus → `/metrics` (enable prometheus-fastapi-instrumentator) |
| Dashboards | Grafana (API latency, queue depth, cache hit ratio, DB connections) |
| Errors | Sentry SDK (`sentry_sdk.init` behind env flag) |
| Uptime | External synthetic checks on `/health` from ≥2 regions |

Key alert thresholds:

| Metric | Warning | Critical |
|---|---|---|
| API p95 latency | > 500 ms | > 2000 ms |
| Error rate | > 1% | > 5% |
| Celery queue depth | > 100 | > 1000 |
| DB connections | > 75% pool | > 90% pool |
| Disk (pgdata volume) | > 75% | > 90% |

## Troubleshooting

<details>
<summary><b>Services won't start / dependency loops</b></summary>

```bash
docker compose ps                 # check states
docker compose logs postgres redis | tail -50
docker compose down && docker compose up -d --force-recreate
```
</details>

<details>
<summary><b>API can't reach database</b></summary>

```bash
docker compose exec api python -c "
from sqlalchemy import create_engine, text
e = create_engine('$DATABASE_URL'.replace('+asyncpg',''))
print(e.connect().execute(text('SELECT 1')).scalar())
"
# Common cause: .env has localhost URLs but you're inside compose networking.
# Compose files set correct URLs automatically — don't override DATABASE_URL manually.
```
</details>

<details>
<summary><b>Port conflicts (3000/5432/6379/8000 busy)</b></summary>

Either stop the conflicting local service or remap in an override file:

```yaml
services:
  api:
    ports: ["8001:8000"]
```
</details>

<details>
<summary><b>Celery worker not picking up tasks</b></summary>

```bash
docker compose logs worker | grep -i error
docker compose exec redis redis-cli -n 1 llen celery     # queue depth
# After code changes, workers must restart (reload covers most cases):
docker compose restart worker scheduler
```
</details>

<details>
<summary><b>Frontend shows API connection errors</b></summary>

- Browser-side calls need a browser-reachable URL: set `NEXT_PUBLIC_API_URL=http://localhost:8000` locally.
- `http://api:8000` only resolves *inside* the Docker network (used for SSR fetches).
- Check CORS_ORIGINS includes your exact frontend origin (scheme + host + port).
</details>

<details>
<summary><b>TimescaleDB hypertable errors</b></summary>

Ensure the extension exists and schema was applied:

```bash
docker compose exec postgres psql -U crypto -d crypto_intelligence \
  -c "CREATE EXTENSION IF NOT EXISTS timescaledb;" \
  -f /dev/stdin < database/schemas/initial_schema.sql
```
</details>
