# mem9-demo

Persistent agent memory on **TiDB Cloud Zero**, wrapped around upstream
[mem9-ai/mem9](https://github.com/mem9-ai/mem9). Spins up on a cold laptop
in under three minutes. Built for the Google Cloud Next 2026 booth; any
developer can use it to kick the tires on mem9.

## Just want memory in Claude Code?

You don't need this repo. Install the plugin and restart — it auto-provisions everything:

```bash
claude plugin marketplace add mem9-ai/mem9
claude plugin install mem9@mem9
# restart Claude Code — done, memory is live
```

mem9 connects to `api.mem9.ai`, which runs TiDB Cloud Zero under the hood.
No TiDB account, no DSN, no config needed.

**This repo** is the booth demo that makes the TiDB layer _visible_ — it runs
mnemo-server locally so you can watch Cloud Zero provision a database live.

---

## What you see (booth demo)

- **Screen 1 - Booth dashboard** (<http://localhost:7000>): live tenant
  metadata, 3 scripted queries, animated architecture diagram, fleet-scale
  tab.
- **Screen 2 - mem9 dashboard** (<http://localhost:3000>): upstream memory
  browser.
- **Screen 3 - Claude Code + mem9 plugin**: real agent talking to the same
  tenant (optional).

## Quick start (booth demo)

```bash
git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
./demo.sh
```

That's it. No config needed. The runner provisions a tenant via `api.mem9.ai`,
seeds 50 memories, and opens the booth dashboard.

> **Want the full self-hosted demo** (mnemo-server + TiDB running on your laptop)?
> Add a TiDB DSN to `.env` — the runner detects it and switches to Docker mode automatically:
> ```bash
> cp .env.example .env
> # edit .env: set MNEMO_DSN="user:pass@tcp(host:4000)/dbname?parseTime=true&tls=true"
> ./demo.sh
> ```

## Prerequisites (booth demo)

| Tool | Hosted path | Self-hosted path |
|---|---|---|
| Python 3.11+ | ✓ required | ✓ required |
| `git` | ✓ required | ✓ required |
| Chrome or Safari | ✓ required | ✓ required |
| Docker Desktop (running) | not needed | ✓ required |
| TiDB Cloud Serverless cluster | not needed | ✓ required |

Hosted path uses `api.mem9.ai` (which runs TiDB Cloud Zero internally).
Self-hosted path runs `mnemo-server` locally so you can see the TiDB layer
directly — useful when TiDB Cloud is the point of the demo.

## 10-step runbook

1. **Prereqs:** Python 3.11+, `git`, Chrome or Safari.
   _(Docker Desktop only needed for self-hosted TiDB path)_
2. **Clone:**
   ```bash
   git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
   ```
3. **(Self-hosted only) Create a TiDB Cloud Serverless cluster:** <https://tidbcloud.com> — copy the DSN.
4. **(Self-hosted only) Configure:**
   ```bash
   cp .env.example .env
   ```
   Open `.env` and replace `MNEMO_DSN` with your DSN. Everything else is pre-filled.
5. **Run:**
   ```bash
   ./demo.sh
   ```
   Hosted: provisions via `api.mem9.ai`, seeds 50 memories, opens dashboard (~30 s).
   Self-hosted: clones upstream mem9, builds Docker images, seeds memories (~90 s on good wifi).
6. **Open the tabs** the runner prints. Screen 1 should show a tenant
   ID, memory counter at 50, and three query pills.
7. **Rehearse** with [`talk_track.md`](talk_track.md). Queries are in
   [`queries.md`](queries.md).
8. **(Optional) Claude Code screen:**
   ```bash
   # one-time plugin install (if not already installed):
   claude plugin marketplace add mem9-ai/mem9
   claude plugin install mem9@mem9
   # restart Claude Code, then set the tenant:
   export MEM9_API_URL=http://localhost:8080
   export MEM9_TENANT_ID=<value from .env>
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

| Command | When to use |
|---|---|
| `./demo.sh` | Live run. No config → uses `api.mem9.ai`. `MNEMO_DSN` set → Docker + TiDB. |
| `./demo.sh --offline` | No network required; serves canned query results |
| `./demo.sh --replay` | Plays `recordings/demo.mp4` (record a session first) |
| `./demo.sh --reset` | Shuts down Docker (if running), clears tenant from `.env` |
| `./demo.sh --record` | Prints the macOS screen-recording hint |

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
