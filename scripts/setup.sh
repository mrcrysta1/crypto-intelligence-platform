#!/usr/bin/env bash
# ============================================================
# Crypto Intelligence Platform - Initial Setup Script
#
# Verifies prerequisites, configures the environment, builds
# images, starts the stack, seeds demo data, and reports health.
#
# Usage:
#   bash scripts/setup.sh            # full setup (docker)
#   bash scripts/setup.sh --no-start # configure + build only
# ============================================================
set -euo pipefail

# ---------- Pretty output helpers ----------
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()      { echo -e "${GREEN}[ OK ]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
fail()    { echo -e "${RED}[FAIL]${NC} $*"; exit 1; }

NO_START=false
[[ "${1:-}" == "--no-start" ]] && NO_START=true

cd "$(dirname "$0")/.."
PROJECT_ROOT="$(pwd)"
info "Project root: ${PROJECT_ROOT}"

# ---------- 1. Prerequisite checks ----------
check_command() {
  if command -v "$1" >/dev/null 2>&1; then
    ok "$1 found: $(command -v "$1")"
  else
    fail "$1 is required but not installed. See https://docs.docker.com/get-docker/"
  fi
}

info "Checking prerequisites..."
check_command docker

if ! docker compose version >/dev/null 2>&1; then
  fail "Docker Compose v2 required (plugin 'docker compose'). Legacy 'docker-compose' v1 not supported."
fi
COMPOSE_VERSION="$(docker compose version --short 2>/dev/null || echo unknown)"
ok "Docker Compose version: ${COMPOSE_VERSION}"

if command -v python3 >/dev/null 2>&1; then
  ok "python3 found: $(python3 --version)"
else
  warn "python3 not found — only needed for local (non-Docker) development."
fi

if command -v node >/dev/null 2>&1; then
  ok "node found: $(node --version)"
else
  warn "node not found — only needed for local (non-Docker) development."
fi

# Verify docker daemon is actually running
if ! docker info >/dev/null 2>&1; then
  fail "Docker daemon is not running. Start Docker Desktop / systemd service and retry."
fi
ok "Docker daemon is running"

# ---------- 2. Environment configuration ----------
ENV_FILE="${PROJECT_ROOT}/.env"

generate_secret() {
  # Portable random hex: openssl preferred, python fallback, /dev/urandom last resort
  if command -v openssl >/dev/null 2>&1; then
    openssl rand -hex "${1:-32}"
  elif command -v python3 >/dev/null 2>&1; then
    python3 -c "import secrets; print(secrets.token_hex(${1:-32}))"
  else
    head -c "${1:-32}" /dev/urandom | od -An -tx1 | tr -d ' \n'
  fi
}

if [[ -f "${ENV_FILE}" ]]; then
  warn ".env already exists — keeping existing configuration."
  info "(Delete .env to regenerate a fresh one.)"
else
  info "Creating .env from template with generated secrets..."
  cp "${PROJECT_ROOT}/.env.example" "${ENV_FILE}"

  SECRET_KEY_VALUE="$(generate_secret 32)"
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "s|SECRET_KEY=change-me-to-a-random-64-char-string|SECRET_KEY=${SECRET_KEY_VALUE}|" "${ENV_FILE}"
  else
    sed -i "s|SECRET_KEY=change-me-to-a-random-64-char-string|SECRET_KEY=${SECRET_KEY_VALUE}|" "${ENV_FILE}"
  fi
  ok "Generated SECRET_KEY and wrote .env"
fi

set -a
# shellcheck disable=SC1091
source "${ENV_FILE}"
set +a

# ---------- 3. Build & start ----------
if [[ "${NO_START}" == true ]]; then
  info "--no-start flag set — building images only."
  docker compose build
  ok "Images built. Start later with:"
  info "  docker compose up -d"
  exit 0
fi

info "Building images (first run may take several minutes)..."
docker compose build

info "Starting services in background..."
docker compose up -d

info "Waiting for postgres & redis health..."
ATTEMPTS=0
MAX_ATTEMPTS=60
until docker compose ps --format json 2>/dev/null | grep -q '"Healthy"' || \
      [[ $(docker compose ps postgres redis 2>/dev/null | grep -c healthy || true) -ge 2 ]]; do
  ATTEMPTS=$((ATTEMPTS + 1))
  if [[ ${ATTEMPTS} -ge ${MAX_ATTEMPTS} ]]; then
    warn "Timed out waiting for infra health. Dumping recent logs:"
    docker compose logs --tail 30 postgres redis api || true
    fail "Infrastructure did not become healthy in time. Check logs above."
  fi
  printf '.'
  sleep 2
done
echo ""
ok "Postgres and Redis are healthy"

# ---------- 4. Database schema ----------
info "Ensuring TimescaleDB extension and initial schema..."
docker compose exec -T postgres psql -U crypto -d crypto_intelligence <<'SQL' || warn "Schema step skipped (may already be applied by app migrations)."
CREATE EXTENSION IF NOT EXISTS timescaledb;
SQL

info "Running database migrations (if alembic is wired)..."
docker compose exec -T api alembic upgrade head 2>/dev/null && ok "Migrations applied" \
  || warn "alembic unavailable or no migration configured yet — skipping."

# ---------- 5. Seed demo data ----------
info "Seeding demo data..."
if docker compose exec -T api python /app/scripts_seed.py >/dev/null 2>&1; then
  ok "Seeded via container entrypoint script"
elif [[ -f "${PROJECT_ROOT}/scripts/seed.py" ]] && command -v python3 >/dev/null 2>&1; then
  DATABASE_URL="${DATABASE_URL:-postgresql+asyncpg://crypto:crypto@localhost:5432/crypto_intelligence}" \
    python3 "${PROJECT_ROOT}/scripts/seed.py" && ok "Demo data seeded" || warn "Seeding failed — stack still usable in DEMO_MODE."
else
  warn "Could not run seeder automatically. Run manually: python scripts/seed.py"
fi

# ---------- 6. Final status ----------
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${GREEN}  Setup complete! 🚀${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""
echo -e "  Dashboard     : http://localhost:3000"
echo -e "  API           : http://localhost:8000"
echo -e "  Swagger UI    : http://localhost:8000/docs"
echo -e "  ReDoc         : http://localhost:8000/redoc"
echo -e "  Health check  : bash scripts/health-check.sh"
echo ""
echo -e "  Logs          : ${YELLOW}docker compose logs -f${NC}"
echo -e "  Stop          : ${YELLOW}docker compose down${NC}"
echo -e "  Reset data    : ${YELLOW}docker compose down -v${NC}  ${RED}(destroys DB!)${NC}"
echo ""
