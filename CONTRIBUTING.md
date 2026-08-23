# Contributing to Crypto Intelligence Platform

First off, thank you for considering contributing! This project thrives on community involvement. This document explains how to set up, what conventions we follow, and how to get your changes merged.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Project Layout Reference](#project-layout-reference)

## Code of Conduct

Be respectful, constructive, and professional. Harassment, trolling, and personal attacks are not tolerated. Maintainainers reserve the right to remove comments, issues, PRs, or participants that violate this standard.

## Getting Started

### Prerequisites

- Docker 24+ with Compose v2 (recommended path), **or**
  - Python 3.12+ for backend work
  - Node.js 20+ for frontend work
- Git
- Make or bash-compatible shell for helper scripts

### Initial Setup

The fastest route — one command:

```bash
git clone https://github.com/your-org/crypto-intelligence-platform.git
cd crypto-intelligence-platform
bash scripts/setup.sh
```

Or manually:

```bash
cp .env.example .env
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d --build
docker compose logs -f   # wait for "Application startup complete"
```

Verify: `bash scripts/health-check.sh` should report all services green.

## Development Workflow

1. **Find or create an issue** — check existing issues first; comment that you're picking it up.
2. **Fork & branch** from `main`:
   ```bash
   git checkout -b feat/short-descriptive-name
   # or fix/, docs/, refactor/, test/, chore/
   ```
3. **Develop** following the standards below.
4. **Test locally**:
   ```bash
   docker compose -f docker-compose.yml -f docker-compose.dev.yml up
   ```
5. **Run quality gates** (all must pass):
   ```bash
   # Backend
   cd apps/api
   ruff check . && ruff format --check .
   mypy app
   pytest tests -v --cov=app --cov-report=term-missing

   # Frontend
   cd apps/web
   npm run lint
   npx tsc --noEmit
   npm test --if-present
   ```
6. **Commit** using the convention below.
7. **Push and open a PR** against `main`.

### Hot Reload

Dev compose mounts source directories:

- Backend: `apps/api` → edits auto-reload uvicorn and Celery (`--reload` flags active).
- Frontend: `apps/web` → Next.js fast refresh works out of the box.

## Coding Standards

### Python (Backend)

- **Formatter/Linter:** ruff (line length 100). Run `ruff format` before committing.
- **Typing:** full type annotations required; `mypy` runs in strict-ish mode in CI. No bare `Any` without justification.
- **Style:**
  - Async-first: use `async def` handlers and async clients in routers/services.
  - Dependency injection via FastAPI `Depends`, no module-level singletons for request-scoped state.
  - Pydantic schemas at boundaries; ORM models never leak into responses.
  - Providers implement the provider protocols in `app/providers/base.py`.
  - Docstrings on public functions/classes; no commented-out code.
- **Naming:** `snake_case` functions/variables, `PascalCase` classes, `UPPER_SNAKE` constants.

### TypeScript (Frontend)

- **Linter:** eslint (next/core-web-vitals config).
- **Types:** `strict: true`; avoid `any`; prefer discriminated unions over enums.
- **Components:** functional components + hooks only. Server components by default in App Router; add `"use client"` deliberately.
- **API access:** through typed client helpers in `src/lib/`, never raw fetch scattered across components.

### General

- No secrets in code, tests, or fixtures — use env vars / mock providers.
- Deterministic tests: no reliance on wall-clock time or external networks (mock providers exist precisely for this).
- Keep diffs focused: one logical change per PR.

## Testing Requirements

| Change type | Required tests |
|---|---|
| Bug fix | Regression test reproducing the bug |
| New endpoint | Unit test for service logic + integration test hitting the router |
| New provider | Contract test against the protocol + mocked HTTP tests |
| ML change | Feature parity test + metric report in PR description |
| Frontend feature | Component/render test where applicable |

Run everything locally before pushing:

```bash
pytest apps/api/tests -v
```

CI will refuse to merge if any gate fails: lint, types, unit tests, integration tests, security scan, docker build.

## Commit Message Convention

We follow Conventional Commits:

```
<type>(<scope>): <short summary in imperative mood>

[optional body explaining why]

[optional footer: BREAKING CHANGE:, Closes #123]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`

Examples:

```
feat(signals): add Bollinger band squeeze detector
fix(api): handle CoinGecko rate-limit 429 with backoff
docs(architecture): expand ML pipeline section
refactor(providers): extract shared retry decorator
```

## Pull Request Process

1. Fill out the PR template completely.
2. Title follows the commit convention.
3. Link related issues (`Closes #42`).
4. Ensure CI is green — maintainers won't review red PRs.
5. Screenshots/GIFs for UI changes.
6. At least **one maintainer approval** required; two for changes touching:
   - auth/security code
   - database migrations
   - provider abstraction contracts
7. Squash-and-merge is the default merge strategy.

PRs may go stale after 30 days of inactivity; a friendly bot will flag them.

## Issue Guidelines

Use the templates:

- 🐛 [Bug report](.github/ISSUE_TEMPLATE/bug_report.md) — include repro steps, environment, logs.
- 💡 [Feature request](.github/ISSUE_TEMPLATE/feature_request.md) — describe the problem first, then your proposed solution.

For security vulnerabilities, do **not** file an issue — see [SECURITY.md](SECURITY.md).

## Project Layout Reference

Where things live (so your PR lands in the right place):

```
apps/api/app/
├── routers/       → new API endpoints here
├── services/      → business logic (routers stay thin)
├── providers/     → data provider implementations
├── models/        → SQLAlchemy models
├── schemas/       → Pydantic request/response schemas
├── workers/       → Celery tasks & beat schedule
├── ml/            → features, training, inference
└── core/          → config, security, logging infra

apps/web/src/
├── app/           → routes/pages (App Router)
├── components/    → UI components
├── hooks/         → reusable React hooks
└── lib/           → API client, utilities
```

## Recognition

All contributors are credited in release notes. Meaningful contributions may earn you commit access over time.

Thanks for contributing! 🚀
