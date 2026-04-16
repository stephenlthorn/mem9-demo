# mem9-demo — Design Spec

**Date:** 2026-04-16
**Owner:** @stephenlthorn
**Event:** Google Cloud Next 2026 (on-booth demo, laptop-resident)
**Status:** Draft, awaiting user review

---

## 1. Goal

Ship a public GitHub repo (`stephenlthorn/mem9-demo`) that lets a booth
operator run a persistent-agent-memory demo on a cold laptop in under three
minutes. The demo must:

1. Prove that a single SQL engine (TiDB Cloud Starter, via `mem9`) does
   vector + full-text + metadata retrieval in one query.
2. Visually reinforce the "ease of getting started + scale when it matters"
   narrative, with a booth-tuned HTML dashboard that runs beside mem9's
   own dashboard and (optionally) a Claude Code agent session.
3. Survive flaky conference wifi via a recorded-MP4 fallback.

This is **not** a new memory product. It is a narrative wrapper around
upstream [mem9-ai/mem9](https://github.com/mem9-ai/mem9).

---

## 2. Context (Phase 0 findings)

The original build plan assumed `pingcap/mem9`. Phase 0 research
corrected that:

- The repo lives at **`mem9-ai/mem9`**, Apache-2.0, 968 stars. TiDB-aligned
  but not inside the `pingcap` GitHub org. The README badge reads *"Powered
  by TiDB Cloud Starter."*
- **Backend:** Go (`server/cmd/mnemo-server`). **Plugins:** TypeScript for
  Claude Code, OpenCode, OpenClaw. **Dashboard:** Next.js app under
  `dashboard/app/`.
- **TiDB is the default backend** (`MNEMO_DB_BACKEND=tidb`); Postgres and
  `db9` are also supported.
- **Tenancy is first-class.** `POST /v1alpha1/mem9s` provisions a tenant
  and returns an ID used as an API key. With `MNEMO_TIDB_ZERO_ENABLED=true`
  (default), mnemo-server auto-provisions a dedicated TiDB database per
  tenant in under a second. This is the demo's opening hook.
- **Full-text search is off by default** (`MNEMO_FTS_ENABLED=false`). The
  demo enables it; the TiDB Cloud Starter cluster must support TiDB FTS.
- **Embeddings** can be server-side via TiDB's `EMBED_TEXT()`
  (`MNEMO_EMBED_AUTO_MODEL=...`) — no OpenAI key required. The demo uses
  this path.
- **Brand split:** internal naming is `mnemos` / `mnemo-server` / `MNEMO_*`
  env vars. Product/API naming is `mem9`. We adopt mem9 in all user-facing
  copy and keep `MNEMO_*` only in `.env.example` / `docker-compose.yml`.

**Implication for the plan:** no structural change. The repo-shape
assumption (runbook with mem9 pulled at setup) still holds. The FTS flag
and the EMBED_TEXT choice become explicit config defaults in the demo.

---

## 3. Decisions on record

All five approvals complete during brainstorming:

| # | Question | Decision |
|---|---|---|
| 1 | Repo relationship to mem9 | **Runbook-only.** Clone mem9 at setup time. No vendoring, no submodule. |
| 2 | Persona | Generic: **Sam Chen**, staff engineer at *Lumos AI*, a Series B AI startup building the *Lantern* research agent. Tuned for GCN exec + tech mix. |
| 3 | TiDB Cloud cluster | **TiDB Cloud Zero auto-provisioning.** mnemo-server provisions a dedicated TiDB database per tenant in <1s. Lead with "ease of starting," pivot to scale. |
| 4 | Network fallback | **Cloud-primary + MP4 fallback.** `demo.sh --replay` plays a recorded run when wifi dies. |
| 5 | Where is the agent? | **A + B.** Primary: booth dashboard shows deterministic memory retrieval (no LLM). Secondary: Claude Code on the laptop, with the mem9 plugin installed against the same tenant, as a swivel-to demo. No in-repo LLM code. |

---

## 4. Architecture

### 4.1 Three-screen booth topology

Every screen points at the **same tenant ID** (captured once by the seeder
and written to `.env`).

| Screen | Source | Purpose in the pitch |
|---|---|---|
| **1. Booth dashboard** | `booth_dashboard/` in this repo | Main stage. Pitch-tuned HTML. Tenant provisioning time, live memory count, 3 query cards with hybrid-score breakdowns, scale strip. |
| **2. mem9 dashboard** | `dashboard/app/` in upstream mem9 repo | "Proof" beat. Generic memory browser. Shows the raw corpus + source attribution. |
| **3. Claude Code** | mem9 Claude plugin (`/plugin install mem9@mem9`) | "Where's the agent?" swivel beat. Real agent loop against the same tenant. |

### 4.2 Runtime components

```
┌─────────────────────── booth laptop ─────────────────────────┐
│                                                              │
│  Browser tab 1: booth_dashboard (localhost:7000)             │
│     │                                                        │
│     │ HTTP (server.py proxies to sidestep CORS)              │
│     ▼                                                        │
│  ┌────────────────────────────────────────────────────┐      │
│  │ docker-compose (services in this repo's compose)   │      │
│  │                                                    │      │
│  │   mnemo-server   :8080   (built from ./mem9)       │      │
│  │   mem9-dashboard :3000   (built from ./mem9)       │      │
│  │   booth-dashboard:7000   (FastAPI from this repo)  │      │
│  └────────────────────────────────────────────────────┘      │
│     │                                                        │
│     │ MNEMO_DSN (TiDB Cloud Starter control DB)              │
│     ▼                                                        │
└──┼───────────────────────────────────────────────────────────┘
   │
   ▼
┌──────────────── TiDB Cloud (Serverless) ─────────────────────┐
│                                                              │
│  Control DB (mnemo-server state, tenant registry)            │
│  + Cloud Zero auto-provisions a dedicated tenant DB per      │
│    POST /v1alpha1/mem9s call (millisecond copy-on-write)     │
└──────────────────────────────────────────────────────────────┘
```

**Key flows:**

- **Tenant provisioning:** `seed_memories.py` → `POST /v1alpha1/mem9s` →
  mnemo-server calls TiDB Cloud Zero API → dedicated DB exists, returns
  `{id}`. Captured and written to `.env` as `MEM9_TENANT_ID`.
- **Memory write:** seeder → `POST /v1alpha2/mem9s/memories` with
  `X-API-Key: <tenant-id>` → mnemo-server inserts into tenant DB with
  `EMBED_TEXT()` generating the vector column server-side.
- **Memory search:** booth dashboard (and Claude Code plugin) →
  `GET /v1alpha2/mem9s/memories?q=...` → single hybrid SQL query in the
  tenant DB → results with vector/FTS/hybrid scores returned.

---

## 5. Repo layout

```
mem9-demo/
├── README.md                 # 10-step cold-laptop runbook
├── LICENSE                   # Apache-2.0 (match mem9 upstream)
├── .env.example              # config template — NO secrets committed
├── .gitignore                # .env, mem9/, recordings/, booth_dashboard/__pycache__
├── docker-compose.yml        # mnemo-server + mem9-dashboard + booth-dashboard
├── demo.sh                   # one-command runner (live + --replay fallback)
├── seed_memories.py          # ~50 memories via mem9 REST API
├── queries.md                # 3 scripted queries + expected results (operator cue card)
├── talk_track.md             # 2-minute GCN pitch with stage directions + variant stings
├── recordings/               # .gitignored; demo.mp4 fallback lives here
│   └── README.md             # how to record a fresh fallback
├── booth_dashboard/
│   ├── server.py             # FastAPI: serves static, proxies /api/* → mnemo-server
│   ├── requirements.txt
│   ├── Dockerfile
│   └── static/
│       ├── index.html
│       ├── app.js            # vanilla JS, no build step
│       ├── style.css
│       ├── diagrams/
│       │   ├── architecture.svg   # per-query unified-engine diagram (Option B hero)
│       │   └── fleet.svg          # tenant-fleet grid for the "scale" tab (Option C)
│       └── vendor/
│           └── anime.min.js       # ~20KB animation lib, checked in (no CDN runtime dep)
└── docs/
    └── superpowers/
        └── specs/
            └── 2026-04-16-mem9-demo-design.md    # this file
```

`mem9/` is cloned into the repo root by `demo.sh` on first run and is
gitignored.

---

## 6. Components in detail

### 6.1 `.env.example`

```bash
# --- TiDB Cloud (control DB for mnemo-server) ---
# Create a Starter cluster at https://tidbcloud.com, paste DSN below.
MNEMO_DSN="user:pass@tcp(host:4000)/mnemos?parseTime=true&tls=true"

# --- mem9 server knobs the demo requires ---
MNEMO_DB_BACKEND=tidb
MNEMO_FTS_ENABLED=true
MNEMO_TIDB_ZERO_ENABLED=true
MNEMO_EMBED_AUTO_MODEL=tidb/text-embedding-v1   # confirm exact model name during impl
MNEMO_EMBED_AUTO_DIMS=1024

# --- mnemo-server URLs (host vs. container network) ---
# Seeder (host-side Python) hits mnemo-server via published port.
MEM9_API_URL_HOST=http://localhost:8080
# Booth dashboard (inside docker-compose network) hits via service name.
MEM9_API_URL_CONTAINER=http://mnemo-server:8080
BOOTH_DASHBOARD_PORT=7000

# --- set by seeder; do not commit ---
# MEM9_TENANT_ID=

# --- mem9 pin (overridden by demo.sh if set) ---
MEM9_GIT_REF=main    # we may pin to a commit SHA before the event
```

### 6.2 `docker-compose.yml`

Three services. Builds mnemo-server and mem9-dashboard from the local
`./mem9/` clone; builds booth-dashboard from `./booth_dashboard/`.

**Open implementation question:** does mem9 ship a ready-made
`docker-compose.yml`? If yes, we extend it; if no, we write Dockerfiles
that wrap `go build ./cmd/mnemo-server` and `pnpm build && pnpm start` for
the dashboard. Resolved during implementation step 2.

### 6.3 `demo.sh`

Bash, posix-friendly. Modes:

- `demo.sh` — live mode (default).
  1. Check `.env` exists and required keys set.
  2. If `./mem9/` missing, `git clone https://github.com/mem9-ai/mem9 mem9` at `MEM9_GIT_REF`.
  3. `docker compose up -d --build`.
  4. Wait for health: `curl -sf localhost:8080/healthz`, `localhost:3000`, `localhost:7000/healthz`.
  5. Run seeder (Python venv in `.venv/`, install requirements, invoke).
  6. Open `http://localhost:7000` in the default browser.
  7. Print the 3 scripted queries and URLs to screens 2 and 3.
- `demo.sh --replay` — opens `recordings/demo.mp4` via `open`.
- `demo.sh --reset` — kills compose stack, drops tenant via `DELETE /v1alpha2/mem9s/...`, clears `MEM9_TENANT_ID`.
- `demo.sh --record` — hints the operator how to capture a fresh MP4 (e.g. `cmd+shift+5`); does not automate recording.

### 6.4 `seed_memories.py`

Python 3.11+. Dependencies: `httpx`, `python-dotenv`. No `pytidb`
dependency — we talk only to mem9's REST API, not TiDB directly.

Flow:

1. Load `.env`.
2. If `MEM9_TENANT_ID` unset, `POST /v1alpha1/mem9s` with `utm_source=gcn-booth`, capture ID, append to `.env`.
3. Read 50 memory records from an in-file list (see §7).
4. `POST /v1alpha2/mem9s/memories` for each, with progress bar.
5. Pretty-print a summary: tenant ID, provisioning time, memory count, dashboard URLs, 3 scripted queries.

### 6.5 `booth_dashboard/`

- **`server.py`** — FastAPI. Endpoints:
  - `GET /` → serves `static/index.html`.
  - `GET /healthz` → for demo.sh to poll.
  - `ANY /api/{path:path}` → proxies to `MEM9_API_URL_CONTAINER` with the tenant's `X-API-Key` header added server-side (so the API key never hits the browser). Allows querying mem9 without CORS config on the upstream server.
  - `GET /meta` → returns `{tenant_id, provisioned_at, region, memory_count}` by reading `.env` and hitting mnemo-server's metadata endpoints.

- **`static/index.html` + `app.js` + `style.css`** — single page, vanilla JS, no build step. `anime.js` vendored locally (~20KB) for diagram animation. Two tabs in the centerpiece: **Query Flow** (default) and **Fleet**.

  **Layout:**
  ```
  ┌──────────────────────────────────────────────────────────────┐
  │ mem9 on TiDB Cloud Zero — live                               │
  ├────────────────────┬────────────────────┬────────────────────┤
  │ tenant: mnm_a8f…   │ memories: 50       │ provisioned: 847ms │
  │ region: us-west-2  │ one TiDB DB — vec  │ (live-measured)    │
  │                    │ + FTS + SQL        │                    │
  ├────────────────────┴────────────────────┴────────────────────┤
  │ [ Query Flow ]  [ Fleet ]              ← tab switcher        │
  ├────────┬─────────────────────────────────────────────────────┤
  │ Query  │                                                     │
  │ rail:  │         ┌────────────────────────────┐              │
  │        │         │   ARCHITECTURE DIAGRAM     │              │
  │ [Q1]◀──┼─────────┼──  animated on click  ──   │              │
  │ [Q2]   │         │                            │              │
  │ [Q3]   │         └────────────────────────────┘              │
  │        │                                                     │
  │        │  result panel (below diagram, populates on click)   │
  │        │  top 3 memories · vec | FTS | hybrid score bars     │
  │        │  operator annotation line                           │
  ├────────┴─────────────────────────────────────────────────────┤
  │ Manus 10M+ DBs · Pinterest 1.3M QPS · Flipkart 700→1 · …     │
  └──────────────────────────────────────────────────────────────┘
  ```

  - **Top strip** — tenant metadata (unchanged semantics; re-arranged into 3 tiles).
  - **Query rail (left)** — the 3 scripted queries as pill-buttons. Clicking one drives the diagram animation and populates the result panel.
  - **Centerpiece (tabs)** — detailed in §6.6.
  - **Result panel** — below the diagram. Top 3 retrieved memories with `vector | FTS | hybrid` score bars and the operator annotation copied from `queries.md`.
  - **Scale strip (bottom)** — static scale proof points, always visible.
  - Memory count auto-polls every 2s during seeding, stops once stable.

### 6.6 Architecture diagram (Option B hero + Option C tab)

The centerpiece is the pitch's hero asset. Two tabs:

#### 6.6.1 "Query Flow" tab — animated unified engine

Static SVG (`diagrams/architecture.svg`) showing:

```
  Agent                mnemo-server              TiDB (tenant DB)
 ┌──────┐   HTTP      ┌──────────────┐   SQL    ┌──────────────────┐
 │ Claude│  ────────▶ │ mnemo-server │ ───────▶ │  ┌─vector col──┐ │
 │ Code  │            │   (Go)       │          │  ├─FTS index───┤ │
 │ /dash │            │              │          │  ├─metadata────┤ │
 └──────┘             └──────────────┘          │  └─one query───┘ │
                                                └──────────────────┘

  Ghosted alternative strip below, greyed out:
  [ Pinecone ] ⇄ sync ⇄ [ Postgres ] ⇄ sync ⇄ [ Elastic ]
  3 systems · ETL glue · sync lag · partial-update bugs
```

**Animation sequence (click a query card, ~800ms total):**

1. `t=0ms` — Agent node pulses. A "packet" circle emits.
2. `t=0–200ms` — Packet travels along Agent → mnemo-server arrow.
3. `t=200–300ms` — mnemo-server node pulses. Label flickers showing the actual HTTP request path (`GET /v1alpha2/mem9s/memories?q=…`).
4. `t=300–500ms` — Packet travels mnemo-server → TiDB. Splits into 3 sub-packets on entry: one to vector column, one to FTS index, one to metadata — all simultaneous. This is the money shot: "one SQL query, three retrieval paths, zero ETL."
5. `t=500–700ms` — TiDB sub-components each emit a score glow. A small `σ` merge glyph in the middle shows hybrid scoring.
6. `t=700–800ms` — Single result packet returns. Result panel below animates in with the top 3 memories + score bars.

Throughout: the ghosted alternative strip below stays visible and greyed. Caption: *"Without TiDB, this same query needs sync glue between three systems."*

Each query has its own animation tint: Q1 emphasizes the vector sub-packet (annotates *"FTS misses — vector wins"*); Q2 emphasizes FTS; Q3 emphasizes the merge glyph (hybrid scoring explicitly labelled).

**Timing contract:** total animation ≤ 800ms. Longer drags the pitch.

#### 6.6.2 "Fleet" tab — Option C, per-agent elasticity

Grid of tenant-DB tiles. Seeded from **real** provisioning timings captured during the seed step (see below).

**How it stays honest:**

- During `seed_memories.py`, after the primary tenant is created, the seeder optionally fires 4 additional `POST /v1alpha1/mem9s` calls (opt-in via `SEED_FLEET_TENANTS=4`), measures each, and records the timings to `booth_dashboard/static/fleet_measurements.json`. Tenants are immediately deleted after timing is captured.
- The Fleet tab renders those 5 real timings as real tiles with their measured `Xms` labels.
- A "Simulate Manus-scale" button multiplies the grid visually to 100 / 10,000 / 10M tiles, each using a jittered value drawn from the measured distribution. Clearly labelled *"extrapolated from 5 measured provisions"* — the operator calls this out in the pitch.

**Fleet animation:** clicking "spawn 100" → tiles appear in a cascade over ~1.5s, each flashing the measured-ish timing. Terminal state: a dense grid with a single "one TiDB cluster underneath" band at the bottom.

**Narration:** *"Each tile is a real dedicated database, provisioned in under a second. Manus runs ten million of these."*

#### 6.6.3 Implementation

- **SVG artwork:** hand-authored, kept simple (boxes, arrows, labels). Stored as two static files. Nodes have stable `id`s that `app.js` references.
- **Animation:** `anime.js` (vendored in `static/vendor/`). No CDN runtime dependency — works offline, supporting the wifi-fallback requirement.
- **Data binding:** each query card defines its animation parameters and score payload in a JSON block loaded at page start. Keeps the animation logic data-driven, not hardcoded per query.
- **Accessibility:** `prefers-reduced-motion` honored — replaces the animation with an instant state swap so the demo still works but without motion.
- **Failure mode:** if the query API call fails (wifi dies mid-pitch), the diagram still plays with canned results baked into the JSON payload. The operator can run `demo.sh --offline` to force this mode pre-emptively. This is a second layer of fallback below the MP4 replay.

### 6.7 `seed_memories` corpus

See §7 for the full 50-record corpus draft. Stored as a Python list literal
at the top of `seed_memories.py` for trivial edit access.

### 6.8 Fleet-timing capture (seeder addition)

When `SEED_FLEET_TENANTS` (default: 4) is set, the seeder — after the
primary tenant is provisioned — performs that many extra
`POST /v1alpha1/mem9s` calls, times each, writes results to
`booth_dashboard/static/fleet_measurements.json`, and deletes those
throwaway tenants via `DELETE /v1alpha1/mem9s/:id` before returning.
The Fleet tab in the booth dashboard reads the JSON file on load.

---

## 7. Seed corpus (Sam Chen, Lumos AI)

~50 memories in 5 buckets. All dates absolute. Corpus is cross-referential:
pipeline-latency event (#15) and pipeline-latency project (#47) share a
p99 budget; the TypeScript/Python preference (#6) is what query 1 hits.

### 7.1 Facts (10)

1. Sam Chen, staff software engineer at Lumos AI, Series B.
2. Stack: Python 3.12, FastAPI, Postgres (migrating to TiDB), Pinecone (decommissioning).
3. Ten years backend experience; last five on ML platform work.
4. Works remotely from Oakland, CA.
5. GitHub handle: `sam-c`.
6. **Prefers Python for anything ML-related; dynamically typed languages keep iteration fast.**  ← query 1 target
7. Daily-driver machine: 16" MacBook Pro M3 Max, 64 GB RAM.
8. Uses Claude Code as his primary coding agent.
9. Writes Rust occasionally when Python can't hit latency targets.
10. On-call rotation every fourth week.

### 7.2 Events (15, dated)

11. Shipped the vector search feature for the research agent on 2026-03-02.
12. Led Q1 planning offsite in Tahoe, 2026-01-14 → 2026-01-16.
13. Authored RFC to migrate from Pinecone to TiDB hybrid search on 2026-02-18.
14. Presented "Agent Memory at Scale" at Lumos all-hands on 2026-03-27.
15. **Debugged a latency regression in the research pipeline on 2026-04-02 — traced to a missing vector index.**  ← query 3 target
16. Hosted interview loop for senior infra hire on 2026-04-08.
17. Closed sev-2 incident about stale embeddings on 2026-03-15.
18. Open-sourced a small embedding-cache utility, `ember-cache`, on 2026-01-29.
19. Attending Google Cloud Next 2026 the week of 2026-04-13.
20. Kicked off internal "memory-as-a-service" project on 2026-02-05.
21. Finished a Python performance audit on 2026-03-10 — shaved 40% off embedding latency.
22. Mentored two new grads through first 90 days; second rotation ended 2026-02-20.
23. Rolled out on-call playbook v2 on 2026-03-30.
24. Published retrospective on Q4 incident trilogy on 2026-01-08.
25. Built the first Lantern prototype the weekend of 2025-11-14.

### 7.3 Relational (8)

26. **Reports to Priya Menon, Director of Platform at Lumos AI.**  ← query 2 target
27. Pairs most often with Jordan Vega, senior ML engineer on the same team.
28. Skip-level: Ana Ruiz, VP Engineering.
29. Shares a project boundary with Daniel Park on the data platform team.
30. Recruiter contact: Noa Weiss, Lumos AI People Ops.
31. Closest external peer: Miguel Torres, staff engineer at a friendly company; weekly ML-infra DMs.
32. Internal mentor: Helen Osei, former principal engineer, now an advisor.
33. Direct report starting Q2 2026: Jess Choi, new grad.

### 7.4 Preferences (10)

34. Hates when agents end responses with a summary — prefers the diff to speak for itself.
35. Prefers concise bullet lists over prose in status updates.
36. Schedules deep work in the morning; meetings after 1 PM.
37. Reviews design docs in Markdown, not Google Docs.
38. Does not want agents to ask clarifying questions when the instruction is obvious.
39. PRs should stay under 400 lines of diff when possible.
40. Likes test-driven development but considers 100% coverage a smell.
41. Drinks tea, not coffee.
42. Keeps Slack closed during focus blocks; teammates should page via PagerDuty if urgent.
43. Reads *The Morning Paper* over breakfast.

### 7.5 Projects (7)

44. Lantern (the research agent) serves 800 Lumos employees as of 2026-04-10.
45. Memory-as-a-service project: unify four scattered memory stores by end of Q2 2026.
46. Evaluating mem9 as Lantern's memory backend — leaning toward adopting.
47. **Pipeline latency work continues; p99 is 840 ms, target sub-500 ms by 2026-05-15.**  ← query 3 target
48. Owns TiDB migration RFC; target: decommission Pinecone by 2026-06-30.
49. Drafting a hybrid-search-vs-Pinecone benchmark; target publish 2026-04-30.
50. Lantern's next major feature: multi-hop retrieval, design phase, landing 2026-06-15.

---

## 8. The 3 queries

Each query card in the booth dashboard and each row in `queries.md`
renders: query text · expected top-3 memories · annotation for the
operator to read aloud.

| # | Query | Expected top hit | Why it's there |
|---|---|---|---|
| 1 | "What does Sam think about TypeScript?" | #6 (Python preference) | **Vector-only win.** Query word ("TypeScript") absent from memory; semantic similarity still surfaces it. FTS returns nothing. Keyword-only stacks fail here. |
| 2 | "Who does Sam report to?" | #26 (reports to Priya) | **Baseline sanity.** Both signals strong. Shows relational + keyword recall still work. |
| 3 | "What slowed down the research pipeline recently?" | #15 (latency regression) + #47 (ongoing p99 work) | **Hybrid beats either alone.** FTS hits "pipeline"; vector pulls "latency regression" semantically. Combined: both right hits, no noise. |

`queries.md` also records, for the operator:

- Exact phrases to narrate.
- Expected hybrid score ranges (for "this is the number you should see on
  the bar" — fails safely if numbers drift).
- A fourth "bonus" query for audiences that linger: *"What's Sam
  drinking?"* → #41 (tea). Trivial, but charming.

---

## 9. Talk track (summary; full version in `talk_track.md`)

Five beats, 2 minutes total, Google Cloud Next–flavored:

1. **Hook (0:00–0:15)** — "Every agent you saw at this conference forgets
   you. Here's what fixes it, and why the storage choice decides whether
   your agent scales to one user or ten million."
2. **Live demo (0:15–0:50)** — run seeder on screen 1 (counter ticks).
   Click query 1; the **architecture diagram animates** — agent → mnemo-server →
   TiDB fans into vector + FTS + metadata simultaneously → merges → returns.
   Land the TypeScript→Python punchline from the result panel. Click query 3;
   same diagram, emphasize the hybrid merge glyph. Point at the ghosted
   "Pinecone + Postgres + Elastic" strip below: *"that's the same query
   without TiDB."*
3. **Scale wall (0:50–1:20)** — flip centerpiece to the **Fleet tab**.
   Narrate *"each of these dots provisioned in under a second — I just
   measured five of them."* Click "Simulate Manus-scale"; grid cascades to
   10M. Reference proof points: Pinterest 1.3M QPS, Flipkart 700→1,
   Dify.AI 500K containers → 1.
4. **Unified engine + ACID (1:20–1:40)** — swivel to screen 2 (mem9
   dashboard, raw memories); one engine vs. Pinecone+Elastic+Postgres;
   multi-row agent transactions need distributed ACID. If a technical
   visitor is present, swivel to screen 3 (Claude Code).
5. **Close (1:40–2:00)** — "$0 idle, 30-day free trial, no credit card.
   Scan the QR code, you'll have your own in 15 seconds."

`talk_track.md` also ships:

- Three variant stings (3–5 seconds each) for walk-bys.
- Five common objections with crisp responses (AlloyDB/pgvector,
  Vertex Vector Search, Pinecone, self-hosting OSS vector DBs, "we
  already use Postgres").
- A stage-direction-free cue-card version for rehearsal.

---

## 10. README runbook (preview)

The 10-step README, top-to-bottom:

1. Prereqs (Docker Desktop, Python 3.11+, `git`, a browser).
2. `git clone https://github.com/stephenlthorn/mem9-demo && cd mem9-demo`.
3. Create a TiDB Cloud Starter cluster (with link).
4. `cp .env.example .env` and fill in `MNEMO_DSN`.
5. `./demo.sh` — watch the seeder populate screens 1 and 2.
6. Open the three screens in the intended browser-tab order.
7. Rehearse with `talk_track.md`.
8. (Optional) Install the mem9 Claude Code plugin for screen 3.
9. Record a fresh `recordings/demo.mp4` so `--replay` works offline.
10. On-booth tips: preload tabs, plug in power, test with phone hotspot.

---

## 11. Non-goals

- ❌ Writing a new memory product. We use upstream mem9 verbatim.
- ❌ Customizing mem9's dashboard. We place a booth dashboard beside it.
- ❌ Embedding fine-tuning. We use TiDB `EMBED_TEXT()` at defaults.
- ❌ Building a custom agent. Claude Code with the mem9 plugin plays that role if needed.
- ❌ An in-dashboard chat LLM loop. LLM latency is a booth-demo risk we explicitly refuse.
- ❌ pytidb direct queries. We talk to mem9's REST API only; the "SQL under the hood" beat is delivered visually via the mem9 dashboard + optional TiDB Cloud SQL editor screenshot in `docs/`.

---

## 12. Open implementation questions (to resolve during build)

These do not block spec approval; they are flagged for the
writing-plans step.

1. Does mem9 ship a `docker-compose.yml` we can extend, or do we author
   Dockerfiles from scratch against its source? (Inspect `./mem9/`
   on first clone.)
2. Exact TiDB `EMBED_TEXT()` model name to pin in `.env.example`.
   (README of mem9 references the flag; actual model ID requires reading
   mem9's embedding README or running it once.)
3. Does mnemo-server expose tenant metadata (provisioning timestamp,
   region, underlying cluster ID) via an API endpoint? If not, the
   booth dashboard's "provisioned in 847ms" card falls back to the
   wall-clock measurement captured by the seeder.
4. Mem9 FTS requirement: confirm TiDB Cloud Starter supports TiDB's
   native FTS (the mem9 README hedges: *"Only set this on clusters that
   support TiDB FTS"*). If Starter does not, either switch on a tier that
   does, or drop to vector-only and restructure query 3.
5. Claude Code plugin install instructions assume `/plugin install
   mem9@mem9`. Verify the marketplace flow end-to-end on the booth
   laptop before the event.
6. Architecture SVG artwork source: hand-authored vs. Excalidraw export.
   Hand-authored gives us stable node `id`s for animation targeting;
   Excalidraw is faster to iterate. Decide during the first implementation
   pass; the animation code is identical either way since it targets
   SVG `id`s.
7. `DELETE /v1alpha1/mem9s/:id` behavior in seeder's fleet-timing capture:
   confirm mnemo-server actually deletes the underlying TiDB Cloud Zero
   database (not just tombstones the tenant row). We don't want 4 orphan
   DBs accumulating per booth run.
8. Animation library choice: `anime.js` (preferred, ~20KB, simple API).
   Fallback if it doesn't cover a case: GSAP free tier. Vendored either
   way — no CDN dependency at booth time.

---

## 13. Success criteria

- Cold `git clone` → working demo in **≤ 10 minutes** including cluster
  provisioning.
- `./demo.sh` → tenant provisioned + 50 memories seeded + all three
  screens healthy in **≤ 90 seconds** on conference wifi (target; MP4
  fallback if wifi is hostile).
- Each of the 3 scripted queries reliably returns the expected top hit
  across ≥ 10 cold runs.
- Booth dashboard legible from 3 meters. Scale-strip numbers readable
  without squinting.
- **Query Flow animation total duration ≤ 800ms per query**; Fleet "spawn
  100" cascade ≤ 1.5s. Feels snappy, not sluggish.
- Architecture diagram plays correctly **with no network** (offline mode
  baked into the JSON payload).
- `talk_track.md` deliverable in a single 2-minute take without flipping
  windows out of order.
- Repo is public, Apache-2.0, with zero secrets in history.
