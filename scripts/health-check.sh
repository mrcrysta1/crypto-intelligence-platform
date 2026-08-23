#!/usr/bin/env bash
# ============================================================
# Crypto Intelligence Platform - Health Check Script
#
# Verifies every service in the stack:
#   containers → postgres → redis → API → web → workers
#
# Usage:
#   bash scripts/health-check.sh            # full check
#   bash scripts/health-check.sh --quiet    # exit code only
#   bash scripts/health-check.sh --json     # machine-readable
# ============================================================
set -u

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
PASS=0; FAIL=0; WARN_COUNT=0
QUIET=false; JSON=false
RESULTS=""

for arg in "$@"; do
  [[ "${arg}" == "--quiet" ]] && QUIET=true
  [[ "${arg}" == "--json" ]]  && JSON=true
done

cd "$(dirname "$0")/.." || exit 1

record() { # status, name, detail
  local status="$1" name="$2" detail="${3:-}"
  case "${status}" in
    PASS) PASS=$((PASS + 1)); [[ "${QUIET}" == false && "${JSON}" == false ]] && echo -e "  ${GREEN}[PASS]${NC} ${name} ${detail:+— ${detail}}" ;;
    FAIL) FAIL=$((FAIL + 1)); [[ "${QUIET}" == false && "${JSON}" == false ]] && echo -e "  ${RED}[FAIL]${NC} ${name} ${detail:+— ${detail}}" ;;
    WARN) WARN_COUNT=$((WARN_COUNT + 1)); [[ "${QUIET}" == false && "${JSON}" == false ]] && echo -e "  ${YELLOW}[WARN]${NC} ${name} ${detail:+— ${detail}}" ;;
  esac
  RESULTS+="{\"check\":\"${name}\",\"status\":\"${status}\",\"detail\":\"${detail}\"},"
}

section() {
  if [[ "${QUIET}" == false && "${JSON}" == false ]]; then
    echo ""
    echo -e "${BLUE}== $* ==${NC}"
  fi
}

command_exists() { command -v "$1" >/dev/null 2>&1; }

# ------------------------------------------------------------
# Docker Compose availability
# ------------------------------------------------------------
if command_exists docker && docker compose version >/dev/null 2>&1; then
  COMPOSE="docker compose"
else
  COMPOSE=""
fi

# ------------------------------------------------------------
# 1. Container states
# ------------------------------------------------------------
section "Containers"

if [[ -n "${COMPOSE}" ]]; then
  for svc in postgres redis api worker scheduler web; do
    STATE=$(${COMPOSE} ps --format json "${svc}" 2>/dev/null | grep -o '"State":"[^"]*"' | head -1 | cut -d'"' -f4)
    HEALTH=$(${COMPOSE} ps --format json "${svc}" 2>/dev/null | grep -o '"Health":"[^"]*"' | head -1 | cut -d'"' -f4)
    if [[ "${STATE}" == "running" ]]; then
      if [[ -n "${HEALTH}" && "${HEALTH}" != "healthy" && "${HEALTH}" != "none" && "${HEALTH}" != "null" ]]; then
        record WARN "${svc}" "state=${STATE}, health=${HEALTH}"
      else
        record PASS "${svc}" "running${HEALTH:+, health=${HEALTH}}"
      fi
    else
      record FAIL "${svc}" "not running (state=${STATE:-absent})"
    fi
  done
else
  record WARN "docker-compose" "unavailable — falling back to endpoint checks only"
fi

# ------------------------------------------------------------
# 2. PostgreSQL
# ------------------------------------------------------------
section "PostgreSQL"

if [[ -n "${COMPOSE}" ]] && ${COMPOSE} exec -T postgres pg_isready -U crypto >/dev/null 2>&1; then
  record PASS "postgres:pg_isready" "accepting connections"
else
  record FAIL "postgres:pg_isready" "not accepting connections"
fi

DB_SIZE=$(${COMPOSE} exec -T postgres psql -U crypto -d crypto_intelligence -tAc \
  "SELECT pg_size_pretty(pg_database_size('crypto_intelligence'));" 2>/dev/null)
[[ -n "${DB_SIZE}" ]] \
  && record PASS "postgres:database_size" "${DB_SIZE//[$'\t\r\n']/}" \
  && ASSET_COUNT=$(${COMPOSE} exec -T postgres psql -U crypto -d crypto_intelligence -tAc \
       "SELECT COUNT(*) FROM assets;" 2>/dev/null | tr -d '[:space:]') \
  || ASSET_COUNT=""
if [[ -n "${ASSET_COUNT}" ]]; then
  record PASS "postgres:assets_table" "${ASSET_COUNT} assets"
else
  record WARN "postgres:assets_table" "table missing or empty (run scripts/seed.py)"
fi

EXT=$(${COMPOSE} exec -T postgres psql -U crypto -d crypto_intelligence -tAc \
  "SELECT extname FROM pg_extension WHERE extname='timescaledb';" 2>/dev/null | tr -d '[:space:]')
[[ "${EXT}" == "timescaledb" ]] \
  && record PASS "postgres:timescale_extension" "enabled" \
  || record WARN "postgres:timescale_extension" "extension not found"

# ------------------------------------------------------------
# 3. Redis
# ------------------------------------------------------------
section "Redis"

PING=$(${COMPOSE} exec -T redis redis-cli ping 2>/dev/null | tr -d '[:space:]')
[[ "${PING}" == "PONG" ]] \
  && record PASS "redis:ping" "PONG" \
  || record FAIL "redis:ping" "no response"

BROKER_QLEN=$(${COMPOSE} exec -T redis redis-cli -n 1 llen celery 2>/dev/null | tr -d '[:space:]')
if [[ "${BROKER_QLEN}" =~ ^[0-9]+$ ]]; then
  if [[ ${BROKER_QLEN} -gt 500 ]]; then
    record WARN "redis:celery_queue" "backlog=${BROKER_QLEN} tasks (workers may be stalled)"
  else
    record PASS "redis:celery_queue" "backlog=${BROKER_QLEN} tasks"
  fi
else
  record WARN "redis:celery_queue" "could not read queue depth"
fi

REDIS_MEM=$(${COMPOSE} exec -T redis redis-cli info memory 2>/dev/null | grep used_memory_human | cut -d: -f2 | tr -d '[:space:]')
[[ -n "${REDIS_MEM}" ]] && record PASS "redis:memory_usage" "${REDIS_MEM}"

# ------------------------------------------------------------
# 4. API endpoints
# ------------------------------------------------------------
section "API (http://localhost:8000)"

API_HEALTH=$(curl -sf -m 10 http://localhost:8000/health 2>/dev/null)
if [[ $? -eq 0 && "${API_HEALTH}" == *'"ok"'* || -n "${API_HEALTH}" ]]; then
  record PASS "api:/health" "responding"
else
  record FAIL "api:/health" "no healthy response"
fi

API_READY=$(curl -sf -m 10 http://localhost:8000/ready 2>/dev/null)
if [[ -n "${API_READY}" ]]; then
  DB_OK=$(echo "${API_READY}" | grep -c '"database":"ok"')
  RD_OK=$(echo "${API_READY}" | grep -c '"redis":"ok"')
  [[ ${DB_OK} -ge 1 ]] && record PASS "api:/ready database" "connected" \
                       || record FAIL "api:/ready database" "connection failed"
  [[ ${RD_OK} -ge 1 ]] && record PASS "api:/ready redis" "connected" \
                       || record FAIL "api:/ready redis" "connection failed"
fi

DOCS_CODE=$(curl -s -o /dev/null -w '%{http_code}' -m 10 http://localhost:8000/docs 2>/dev/null)
[[ "${DOCS_CODE}" == "200" ]] \
  && record PASS "api:/docs" "swagger reachable" \
  || record FAIL "api:/docs" "HTTP ${DOCS_CODE}"

MARKETS_CODE=$(curl -s -o /dev/null -w '%{http_code}' -m 15 "http://localhost:8000/api/v1/markets?limit=1" 2>/dev/null)
case "${MARKETS_CODE}" in
  200) record PASS "api:/markets" "returns data" ;;
  404|501) record WARN "api:/markets" "endpoint not implemented yet (HTTP ${MARKETS_CODE})" ;;
  *) record FAIL "api:/markets" "HTTP ${MARKETS_CODE}" ;;
esac

# ------------------------------------------------------------
# 5. Celery workers
# ------------------------------------------------------------
section "Celery Workers"

WORKER_PING=$(${COMPOSE} exec -T api celery -A app.workers.celery_app inspect ping -d '*' --timeout 8 2>/dev/null | grep -c "pong\|OK")
if [[ ${WORKER_PING:-0} -ge 1 ]]; then
  record PASS "celery:worker_ping" "${WORKER_PING} worker(s) responded"
else
  record WARN "celery:worker_ping" "no workers responded (may still be booting)"
fi

BEAT_RUNNING=$(${COMPOSE} ps scheduler 2>/dev/null | grep -c Up)
[[ ${BEAT_RUNNING:-0} -ge 1 ]] \
  && record PASS "celery:beat_scheduler" "container up" \
  || record WARN "celery:beat_scheduler" "scheduler not detected"

# ------------------------------------------------------------
# 6. Frontend
# ------------------------------------------------------------
section "Frontend (http://localhost:3000)"

WEB_CODE=$(curl -s -o /dev/null -w '%{http_code}' -m 15 http://localhost:3000 2>/dev/null)
case "${WEB_CODE}" in
  200) record PASS "web:homepage" "HTTP 200" ;;
  000) record FAIL "web:homepage" "connection refused — is the web service running?" ;;
  *) record FAIL "web:homepage" "HTTP ${WEB_CODE}" ;;
esac

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
TOTAL=$((PASS + FAIL))
HEALTHY=$(( FAIL == 0 ))

if [[ "${JSON}" == true ]]; then
  echo "{\"pass\": ${PASS}, \"fail\": ${FAIL}, \"warn\": ${WARN_COUNT}, \"healthy\": ${HEALTHY}, \"results\": [${RESULTS%,}]}"
elif [[ "${QUIET}" == false ]]; then
  echo ""
  echo -e "${BLUE}============================================${NC}"
  printf "  Checks passed : %s\n  Checks failed : %s\n  Warnings      : %s\n" \
    "${GREEN}${PASS}${NC}" "${RED}${FAIL}${NC}" "${YELLOW}${WARN_COUNT}${NC}"
  if [[ ${HEALTHY} -eq 1 ]]; then
    echo -e "  Overall       : ${GREEN}ALL SYSTEMS OPERATIONAL${NC}"
  else
    echo -e "  Overall       : ${RED}DEGRADED — inspect failures above${NC}"
    echo ""
    echo -e "  Tip: docker compose logs <service>   # inspect a failing service"
    echo -e "  Tip: bash scripts/setup.sh           # full re-setup"
  fi
  echo -e "${BLUE}============================================${NC}"
fi

exit ${FAIL}
