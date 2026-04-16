# mem9-demo

Persistent agent memory on **TiDB Cloud Zero**, built on top of
[mem9-ai/mem9](https://github.com/mem9-ai/mem9). Built for the Google Cloud
Next 2026 booth — any developer can clone and run it in under two minutes.

---

## Just want memory in Claude Code?

You don't need this repo. Two commands and a restart:

```bash
claude plugin marketplace add mem9-ai/mem9
claude plugin install mem9@mem9
# restart Claude Code — memory is live
```

mem9 auto-provisions via `api.mem9.ai` (TiDB Cloud Zero under the hood).
No TiDB account, no DSN, no config.

**This repo** is a booth demo that makes the TiDB layer _visible_: it
provisions a tenant, seeds 50 memories about a fictional engineer, and lets
you run live semantic queries against them while the architecture diagram
animates in the background.

---

## Quick start

```bash
git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
./demo.sh
```

No config needed. The runner provisions a tenant via `api.mem9.ai`, seeds 50
memories, and opens the booth dashboard at <http://localhost:7000>.

> **Want the full self-hosted demo** (mnemo-server + TiDB running locally)?
> Set `MNEMO_DSN` in `.env` — the runner auto-detects it and switches to Docker mode:
> ```bash
> cp .env.example .env
> # edit .env: set MNEMO_DSN="user:pass@tcp(host:4000)/dbname?parseTime=true&tls=true"
> ./demo.sh
> ```

---

## Two run modes

| | Hosted | Self-hosted |
|---|---|---|
| **Backend** | `api.mem9.ai` | `mnemo-server` in Docker |
| **TiDB** | managed by mem9 | your TiDB Cloud Serverless cluster |
| **Setup** | none | `MNEMO_DSN` in `.env` |
| **Docker required** | no | yes |
| **What you see** | booth dashboard only | booth dashboard + mem9 dashboard |
| **Best for** | quick runs, no-wifi fallback | showing TiDB layer directly |

---

## Prerequisites

| Tool | Hosted | Self-hosted |
|---|---|---|
| Python 3.11+ | ✓ | ✓ |
| `git` | ✓ | ✓ |
| Chrome or Safari | ✓ | ✓ |
| Docker Desktop (running) | — | ✓ |
| TiDB Cloud Serverless cluster | — | ✓ |

For the self-hosted path, create a free Serverless cluster at
<https://tidbcloud.com>, copy the DSN from **Connect → General**, and paste it
into `MNEMO_DSN` in `.env`. Everything else is pre-configured.

---

## Runbook

### Hosted (default — no config)

```bash
git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
./demo.sh
```

1. Provisions a tenant via `api.mem9.ai` (~1 s)
2. Seeds 50 memories about Sam Chen
3. Starts the booth dashboard at <http://localhost:7000>

### Self-hosted (TiDB visible)

```bash
git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo
cp .env.example .env          # then set MNEMO_DSN
./demo.sh
```

1. Clones upstream `mem9-ai/mem9`
2. Builds Docker images for `mnemo-server` and `mem9-dashboard` (~90 s first run)
3. Provisions a tenant, seeds 50 memories
4. Opens two screens:
   - <http://localhost:7000> — booth dashboard
   - <http://localhost:3000> — mem9 upstream dashboard

### Optional: Claude Code as Screen 3

```bash
# one-time install (if not already done):
claude plugin marketplace add mem9-ai/mem9
claude plugin install mem9@mem9
# restart Claude Code, then point it at the running tenant:
export MEM9_TENANT_ID=<value from .env>
# for self-hosted, also:
export MEM9_API_URL=http://localhost:8080
```

Ask Claude: *"Who does Sam report to?"* — it answers from the seeded memories.

### Record a fallback

```bash
./demo.sh --record    # prints macOS screen-recording hint
# save as recordings/demo.mp4
./demo.sh --replay    # verify playback works
```

### On-booth tips

- Plug in power before the session starts
- Preload all tabs before the first visitor arrives
- Use phone hotspot — conference wifi is unreliable
- Rehearse with [`talk_track.md`](talk_track.md); queries are in [`queries.md`](queries.md)

---

## Modes

| Command | What it does |
|---|---|
| `./demo.sh` | Live run. No `MNEMO_DSN` → hosted via `api.mem9.ai`. DSN set → Docker + TiDB. |
| `./demo.sh --offline` | No network needed; serves canned query results from `booth_dashboard/canned.py` |
| `./demo.sh --replay` | Plays `recordings/demo.mp4` |
| `./demo.sh --reset` | Shuts down Docker (if running), clears tenant vars from `.env` |
| `./demo.sh --record` | Prints the macOS screen-recording instructions |

---

## Architecture

### Hosted path

```
Claude Code (mem9 plugin)
  └── api.mem9.ai
        └── TiDB Cloud Zero (per-tenant DB, auto-provisioned)

booth laptop
└── localhost:7000  (booth-dashboard: FastAPI + static HTML)
      └── /api/* → https://api.mem9.ai  (X-API-Key injected server-side)
```

### Self-hosted path

```
booth laptop
├── localhost:7000  (booth-dashboard: FastAPI + static HTML)
│     └── /api/* → mnemo-server:8080  (X-API-Key injected server-side)
├── localhost:3000  (mem9-dashboard: upstream Vite/React SPA)
└── localhost:8080  (mnemo-server: upstream Go binary)
      └── TiDB Cloud Serverless
            └── Cloud Zero: per-tenant DB auto-provisioned in <1 s

Claude Code (mem9 plugin, optional Screen 3)
  └── localhost:8080  (same mnemo-server, same tenant)
```

---

## What's in this repo

| Path | Description |
|---|---|
| `demo.sh` | Runner script — hosted and self-hosted paths |
| `seed_memories.py` | Provisions tenant, seeds 50 memories, writes tenant ID back to `.env` |
| `corpus.py` | 50-memory Sam Chen persona used for demo queries |
| `mem9_client.py` | Thin httpx wrapper around the mnemo-server REST API |
| `env_writer.py` | Idempotent `.env` writeback helper |
| `booth_dashboard/` | FastAPI app + static HTML/CSS/JS dashboard |
| `booth_dashboard/canned.py` | Offline fallback results for 3 scripted queries |
| `docker/` | Dockerfiles for `mnemo-server` (Go) and `mem9-dashboard` (Vite) |
| `docker-compose.yml` | Self-hosted stack definition |
| `queries.md` | Operator cue card — 3 scripted queries + fallback ladder |
| `talk_track.md` | 2-minute booth script with objection handling |

---

## Non-goals

This repo is a booth wrapper, not a memory product. All heavy lifting is
upstream in `mem9-ai/mem9`. See
[`docs/superpowers/specs/2026-04-16-mem9-demo-design.md`](docs/superpowers/specs/2026-04-16-mem9-demo-design.md)
for the full design.

---

## License

Apache-2.0, matching upstream. See [LICENSE](LICENSE).
