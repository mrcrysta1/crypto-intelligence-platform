# Security Policy

## Supported Versions

We release security patches for the following versions:

| Version | Supported |
| --- | --- |
| latest on `main` | ✅ |
| tagged releases within last 90 days | ✅ |
| older releases | ❌ (upgrade) |

## Reporting a Vulnerability

**Do NOT open a public GitHub issue for security vulnerabilities.**

Instead, report privately:

1. **Preferred:** Use GitHub's [private vulnerability reporting](../../security/advisories/new) on this repository.
2. **Alternative:** Email `security@your-domain.com` with:
   - Description of the vulnerability
   - Affected component(s) and version/commit hash
   - Step-by-step reproduction or proof-of-concept
   - Potential impact assessment
   - Any suggested remediation

You will receive an acknowledgment within **48 hours**, and a status update at least every **7 days** until resolution.

Please allow up to **90 days** for coordinated disclosure before any public release. We ask that you:

- Give us reasonable time to fix the issue before public disclosure.
- Do not access, modify, or exfiltrate data that isn't yours.
- Do not run denial-of-service tests against hosted instances.
- Do not test against third-party provider APIs through our platform.

## Security Architecture Overview

Full details live in [ARCHITECTURE.md §7](ARCHITECTURE.md#7-security-architecture). Summary:

### Authentication & Authorization
- JWT (HS256) bearer tokens with configurable expiry (`JWT_EXPIRATION_HOURS`)
- bcrypt password hashing
- Route-level auth dependency guards; admin-scoped endpoints isolated
- Optional hashed API keys for machine clients

### Input Validation
- Pydantic v2 validation at every API boundary
- SQLAlchemy parameterized queries exclusively (ORM-only; no raw string SQL)
- Strict models rejecting unknown fields where appropriate

### Rate Limiting & Abuse Prevention
- Redis-backed sliding window per IP and per token
- Configurable via `RATE_LIMIT_REQUESTS` / `RATE_LIMIT_WINDOW`

### Transport
- TLS terminated at reverse proxy in production deployments
- CORS restricted to explicit allow-list (`CORS_ORIGINS`) — never wildcard in prod

### Container Hardening
- Multi-stage builds; production images run as non-root users
- Minimal base images (slim/alpine); no package managers in runtime layers where avoidable
- Healthchecks on every long-running service
- Compose fails fast if required secrets (`SECRET_KEY`, `POSTGRES_PASSWORD`) are missing in prod profile

### Secrets Management
- Secrets supplied via environment variables only
- `.env` is git-ignored; `.env.example` contains placeholder values exclusively
- CI secret scanning runs on every push (see `.github/workflows/ci.yml`)

### Data Protection
- Append-only audit log for auth events and admin actions
- Structured JSON logging without PII or credentials
- Demo mode uses deterministic synthetic data only — no real user data required

### Dependencies
- Pinned dependencies in lockfiles
- Automated scanning: pip-audit (Python), npm audit (Node), Trivy (container images)
- Dependabot-style updates recommended weekly

## Security Controls Checklist for Operators

When deploying this platform, ensure:

- [ ] `SECRET_KEY` set to a cryptographically random value (`openssl rand -hex 32`)
- [ ] Default database credentials changed from `crypto/crypto`
- [ ] `DEMO_MODE=false` in production (disables mock providers)
- [ ] `CORS_ORIGINS` lists only your actual frontend origins
- [ ] TLS enforced end-to-end; HTTP redirected to HTTPS
- [ ] Database not exposed publicly (remove `5432:5432` port mapping or firewall it)
- [ ] Redis not exposed publicly (same as above)
- [ ] Regular image rebuilds to pick up base-image security patches
- [ ] Log aggregation and alerting configured
- [ ] Backups of PostgreSQL tested for restore

## Disclosure Policy

1. Report received → triaged within 48h, severity assigned (CVSS-based).
2. Fix developed privately on a security branch.
3. Patched release published; advisory drafted.
4. Public disclosure coordinated with reporter credit (unless anonymity requested).

Severity handling targets:

| Severity | Fix Target |
|---|---|
| Critical | 7 days |
| High | 30 days |
| Medium | 60 days |
| Low | 90 days / next minor |

## Contact

- Security reports: GitHub private advisories or `security@your-domain.com`
- General questions: regular GitHub issues (non-sensitive topics only)

Thank you for helping keep Crypto Intelligence Platform secure.
