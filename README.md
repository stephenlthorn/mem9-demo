# mem9-demo

Persistent agent memory on **TiDB Cloud Zero**, wrapped around upstream
[mem9-ai/mem9](https://github.com/mem9-ai/mem9). Spins up on a cold laptop
in under three minutes. Built for the Google Cloud Next 2026 booth; any
developer can use it to kick the tires on mem9.

## What you see

- **Screen 1 - Booth dashboard** (<http://localhost:7000>): live tenant
  metadata, 3 scripted queries, animated architecture diagram, fleet-scale
  tab.
- **Screen 2 - mem9 dashboard** (<http://localhost:3000>): upstream memory
  browser.
- **Screen 3 - Claude Code + mem9 plugin**: real agent talking to the same
  tenant (optional).

## 10-step runbook

1. **Prereqs:** Docker Desktop, Python 3.11+, `git`, Chrome or Safari.
2. **Clone:**
   ```bash
   git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
   ```
3. **Create a TiDB Cloud Starter cluster:** <https://tidbcloud.com> - copy the DSN.
4. **Configure:**
   ```bash
   cp .env.example .env
   # edit .env: paste MNEMO_DSN
   ```
5. **Run:**
   ```bash
   ./demo.sh
   ```
   First run downloads upstream mem9, builds three Docker images, seeds
   50 memories. ~90 seconds on good wifi.
6. **Open the tabs** the runner prints. Screen 1 should show a tenant
   ID, memory counter at 50, and three query pills.
7. **Rehearse** with [`talk_track.md`](talk_track.md). Queries are in
   [`queries.md`](queries.md).
8. **(Optional) Claude Code screen:**
   ```bash
   # in Claude Code:
   /plugin install mem9@mem9
   # set MEM9_TENANT_ID to the value from .env
   ```
   Ask it: *"Who does Sam report to?"* It should answer from memory.
9. **Record a fallback:**
   ```bash
   ./demo.sh --record   # prints macOS recording hint
   # save the capture as recordings/demo.mp4
   ./demo.sh --replay   # verify playback
   ```
10. **On-booth tips:** plug in power; preload all three tabs before a
    visitor arrives; test with phone hotspot (conference wifi lies).

## Modes

- `./demo.sh` - live.
- `./demo.sh --offline` - frontend only, canned queries. Wifi-safe.
- `./demo.sh --replay` - plays `recordings/demo.mp4`.
- `./demo.sh --reset` - tears down compose, clears tenant from .env.

## Architecture

```
booth laptop
├── Screen 1: localhost:7000  (booth-dashboard: FastAPI + static HTML)
│   └── /api/* → mnemo-server:8080 (X-API-Key injected server-side)
├── Screen 2: localhost:3000  (mem9-dashboard: upstream Vite/React)
└── Screen 3: Claude Code + mem9 plugin (optional, same tenant)

TiDB Cloud (Serverless)
└── Per-tenant DB via Cloud Zero auto-provisioning (<1s per tenant)
```

## Non-goals

This repo is a booth wrapper, not a memory product. All heavy lifting is
upstream in mem9-ai/mem9. See
[`docs/superpowers/specs/2026-04-16-mem9-demo-design.md`](docs/superpowers/specs/2026-04-16-mem9-demo-design.md)
for the full design.

## License

Apache-2.0, matching upstream. See [LICENSE](LICENSE).
