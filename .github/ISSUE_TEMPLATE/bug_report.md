---
name: Bug Report
about: Report a problem with the platform
title: "[BUG] "
labels: ["bug", "triage"]
assignees: []
---

## Description

<!-- A clear, concise description of the bug. What happened vs. what did you expect? -->

## Steps to Reproduce

1. Go to '...'
2. Run '...'
3. Observe error

**Minimal repro (if possible):**

```bash
# commands / code snippet that reliably triggers the bug
```

## Expected Behavior

<!-- What should have happened? -->

## Actual Behavior

<!-- What actually happened? Include full error messages. -->

## Environment

| Component | Value |
|---|---|
| Deployment | Docker Compose / local venv |
| OS | <!-- e.g. Ubuntu 24.04, Windows 11, macOS 15 --> |
| Docker version | `docker --version` output |
| Commit/Tag | `git rev-parse --short HEAD` or release tag |
| DEMO_MODE | true / false |

## Logs

<details>
<summary>Service logs</summary>

```bash
# Paste relevant output from:
docker compose logs api worker scheduler web --tail 100

# Or for a single service:
docker compose logs <service> --tail 100
```

```
[paste logs here — redact any secrets!]
```

</details>

## Screenshots

<!-- If UI-related. Drag & drop images here. -->

## Additional Context

<!-- Frequency (always/sometimes), recent changes that might relate, anything else useful. -->

## Checklist

- [ ] I searched existing issues for duplicates
- [ ] I'm running the latest code on `main` (or noted my exact tag)
- [ ] Logs are included and contain no secrets/API keys
