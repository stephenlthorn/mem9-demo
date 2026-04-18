# Booth Dashboard UI Narrative Redesign

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Transform the booth dashboard from a technical demo into a persuasive narrative experience that communicates TiDB's AI-era positioning — with customer proof, clear pain points, and business outcomes on every screen.

**Architecture:** All changes are static frontend only (`index.html`, `style.css`, `app.js`). The Python backend (`server.py`, `llm_client.py`, etc.) is untouched. All 33 existing tests must continue to pass. A new `tests/test_index_html_structure.py` file grows task-by-task to verify HTML structure.

**Tech Stack:** Vanilla HTML/CSS/JS, FastAPI static file serving, pytest for structural verification.

---

## File Map

| File | What changes |
|---|---|
| `booth_dashboard/static/index.html` | New hero, customer strip, new panels in lifecycle tab, new "Why TiDB" tab, redesigned fleet tab, closing strip |
| `booth_dashboard/static/style.css` | CSS for every new component; modify `.hero-headline` rule |
| `booth_dashboard/static/app.js` | Remove fleet tile-spawn functions; remove fleet controls bind |
| `tests/test_index_html_structure.py` | Created in Task 1, extended in Tasks 2–7 |

**Do not touch:** `booth_dashboard/server.py`, `booth_dashboard/llm_client.py`, `booth_dashboard/canned.py`, any file in `tests/` except `test_index_html_structure.py`.

---

## Context — The Narrative We're Building

The demo tells this story, tab by tab:

1. **Hook (hero):** "The memory wall kills agents." → TiDB is the solution.
2. **Live Recall:** Watch hybrid search work live. (mostly unchanged)
3. **Ask the Agent:** Chat with a mem9-backed agent. (mostly unchanged)
4. **Memory Duties:** Three ways memory fails → five duties that prevent it → Why TiDB makes all five possible.
5. **One Cluster:** Before (4 systems) vs. After (1 TiDB). (mostly unchanged)
6. **Cross-Session Proof:** Real incident, real learning. (mostly unchanged)
7. **Why TiDB:** Four AI pain points + TiDB solutions + Four AI patterns (NEW TAB).
8. **Scale:** Scale ladder (1 → 10M) + three customer proof tiles.
9. **Footer:** "Stop prompting. Start maintaining."

---

## Task 1: Hero Overhaul + Customer Proof Strip

**What this does:** Replaces the generic hero tagline with a narrative hook ("the memory wall"), the TiDB AI-era positioning tagline, and a horizontal customer proof strip (Manus, Pinterest, DeepSeek, Plaud, Kimi, Dify.AI, Flipkart).

**Files:**
- Modify: `booth_dashboard/static/index.html` (hero section, lines 12–21; insert proof strip after `</header>` before `.stat-strip`)
- Modify: `booth_dashboard/static/style.css` (replace `.hero-headline` rule ~line 33; add new hero classes after line 43)
- Create: `tests/test_index_html_structure.py`

---

- [ ] **Step 1: Write the failing test**

Create `tests/test_index_html_structure.py` with this content:

```python
"""Structural tests for booth_dashboard/static/index.html.

Each task in the UI redesign plan appends a test function here.
Run from the repo root: pytest tests/test_index_html_structure.py -v
"""
from pathlib import Path

HTML = Path("booth_dashboard/static/index.html").read_text()


def test_hero_has_positioning_tagline():
    """Task 1: Hero should contain the TiDB AI-era positioning tagline."""
    assert "Unified Data Foundation" in HTML


def test_hero_has_memory_wall_hook():
    """Task 1: Hero should contain the memory wall narrative hook."""
    assert "memory wall" in HTML.lower()


def test_customer_proof_strip_exists():
    """Task 1: Customer proof strip class should be present."""
    assert "customer-proof-strip" in HTML


def test_all_customers_present():
    """Task 1: All customer names must appear in the HTML."""
    for name in ["Manus", "Pinterest", "DeepSeek", "Plaud", "Kimi", "Dify"]:
        assert name in HTML, f"Missing customer: {name}"
```

- [ ] **Step 2: Run test to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py -v
```

Expected: 4 FAIL (assertions not yet satisfied).

- [ ] **Step 3: Replace the hero section in `index.html`**

Open `booth_dashboard/static/index.html`. Replace the entire `<header class="hero">...</header>` block (lines 12–21) with:

```html
  <!-- ── Hero ── -->
  <header class="hero">
    <div class="hero-eyebrow">mem9 · Persistent Agent Memory on TiDB Cloud Zero</div>
    <div class="hero-headline">TiDB — Unified Data Foundation for the AI Era</div>
    <div class="hero-tagline">
      One set of data simultaneously supports transactions, analytics,
      vector retrieval, RAG, and long-term memory for Agents.
    </div>
    <div class="hero-hook">
      <span class="hook-bang">⚠</span>
      <div class="hook-body">
        <strong>The memory wall.</strong>
        Without persistent memory, agents repeat the same mistakes, cite stale facts,
        and hallucinate coherence from session to session. Every run is day one.
        The tabs below show how TiDB solves it — once, at the infrastructure layer.
      </div>
    </div>
  </header>
```

- [ ] **Step 4: Insert the customer proof strip after `</header>` and before `<!-- ── Stat strip ── -->`**

```html
  <!-- ── Customer proof strip ── -->
  <div class="customer-proof-strip">
    <div class="proof-label">Running agent memory at scale:</div>
    <div class="proof-items">
      <div class="proof-item">
        <div class="proof-name">Manus</div>
        <div class="proof-stat">10M+ agent DBs · 80% cost reduction</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">Pinterest</div>
        <div class="proof-stat">1.3M QPS · 6 systems → 1</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">DeepSeek</div>
        <div class="proof-stat">AI agent infrastructure on TiDB</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">Plaud</div>
        <div class="proof-stat">AI agents on TiDB</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">Kimi</div>
        <div class="proof-stat">AI agents on TiDB</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">Dify.AI</div>
        <div class="proof-stat">500K containers → 1 cluster · 90% ops cut</div>
      </div>
      <div class="proof-divider"></div>
      <div class="proof-item">
        <div class="proof-name">Flipkart</div>
        <div class="proof-stat">700+ MySQL → 1 · 1M QPS · P95 &lt; 5ms</div>
      </div>
    </div>
  </div>
```

- [ ] **Step 5: Update CSS for the hero and add customer proof strip styles**

In `booth_dashboard/static/style.css`, find the `.hero-headline` rule (around line 33) and replace it:

Old:
```css
.hero-headline {
  font-size: 20px;
  font-weight: 700;
  color: var(--accent);
  margin-bottom: 6px;
}
```

New:
```css
.hero-eyebrow {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--muted);
  margin-bottom: 8px;
}
.hero-headline {
  font-size: 26px;
  font-weight: 800;
  color: var(--fg);
  margin-bottom: 6px;
  line-height: 1.2;
}
.hero-tagline {
  font-size: 15px;
  color: var(--ok);
  font-weight: 500;
  margin-bottom: 14px;
  max-width: 780px;
  line-height: 1.5;
}
.hero-hook {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: rgba(247, 37, 133, 0.08);
  border: 1px solid rgba(247, 37, 133, 0.25);
  border-left: 3px solid var(--accent-2);
  border-radius: 0 8px 8px 0;
  padding: 12px 14px;
  max-width: 780px;
}
.hook-bang {
  font-size: 18px;
  line-height: 1.4;
  flex-shrink: 0;
}
.hook-body {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
}
.hook-body strong { color: var(--fg); }
```

Then, after the `.hero-sub strong` rule (currently line 43), append:

```css
/* ── Customer proof strip ── */
.customer-proof-strip {
  background: var(--panel);
  border-bottom: 1px solid var(--border);
  padding: 10px 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  overflow-x: auto;
  white-space: nowrap;
}
.proof-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  flex-shrink: 0;
}
.proof-items {
  display: flex;
  align-items: center;
  gap: 16px;
}
.proof-item {
  display: flex;
  flex-direction: column;
  gap: 1px;
}
.proof-name {
  font-size: 13px;
  font-weight: 700;
  color: var(--fg);
}
.proof-stat {
  font-size: 11px;
  color: var(--muted);
}
.proof-divider {
  width: 1px;
  height: 28px;
  background: var(--border);
  flex-shrink: 0;
}
```

- [ ] **Step 6: Run tests to verify they pass**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 6 PASS (4 new + 2 existing no-innerHTML tests).

- [ ] **Step 7: Run the full suite to confirm nothing is broken**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 33+ PASS, 0 FAIL.

- [ ] **Step 8: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: hero overhaul with narrative hook, TiDB positioning tagline, and customer proof strip"
```

---

## Task 2: Lifecycle Tab — Three Failure Modes Panel

**What this does:** Adds a "three ways agent memory fails" panel *before* the 5 memory duties in the lifecycle tab. Sets up the problem → solution narrative arc. Three cards: Token Debt, Context Amnesia, Memory Decay.

**Files:**
- Modify: `booth_dashboard/static/index.html` (lifecycle tab, after `.panel-hero`, before `.duty-grid`)
- Modify: `booth_dashboard/static/style.css` (append failure modes styles)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test to `tests/test_index_html_structure.py`**

Open `tests/test_index_html_structure.py` and append:

```python

def test_lifecycle_tab_has_failure_modes():
    """Task 2: Lifecycle tab should have the three failure modes panel."""
    assert "failure-modes-section" in HTML
    assert "Token Debt" in HTML
    assert "Context Amnesia" in HTML
    assert "Memory Decay" in HTML
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_lifecycle_tab_has_failure_modes -v
```

Expected: FAIL.

- [ ] **Step 3: Add the failure modes HTML to the lifecycle tab in `index.html`**

Find the lifecycle tab section. It starts with:
```html
    <!-- ── Tab 2: 5 Memory Duties ── -->
    <section class="tab-panel" data-tab-panel="lifecycle">
      <div class="panel-hero">
```

After the closing `</div>` of `.panel-hero` (which ends with `</div>` right before `<div class="duty-grid">`), insert:

```html

      <!-- ── Three Failure Modes ── -->
      <div class="failure-modes-section">
        <div class="failure-modes-heading">Three ways agent memory fails in production:</div>
        <div class="failure-modes-grid">
          <div class="failure-mode-card">
            <div class="failure-icon">💸</div>
            <div class="failure-name">Token Debt</div>
            <div class="failure-desc">
              Stuffing all memories into every prompt burns your context window.
              At scale you are paying to remind the agent what it already knew,
              every single message.
            </div>
            <div class="failure-signal">Signal: context window keeps hitting limits</div>
          </div>
          <div class="failure-mode-card">
            <div class="failure-icon">🫥</div>
            <div class="failure-name">Context Amnesia</div>
            <div class="failure-desc">
              Session ends. Agent forgets everything. The next user gets the same
              wrong diagnosis the agent gave the last three users.
              Cross-session learning simply does not exist.
            </div>
            <div class="failure-signal">Signal: agents repeat the same mistakes</div>
          </div>
          <div class="failure-mode-card">
            <div class="failure-icon">📉</div>
            <div class="failure-name">Memory Decay</div>
            <div class="failure-desc">
              Old facts do not expire. Contradicted conclusions sit beside newer truths.
              The agent confidently cites a diagnosis it corrected six months ago.
            </div>
            <div class="failure-signal">Signal: agents hallucinate coherence from stale data</div>
          </div>
        </div>
      </div>
      <div class="failure-to-solution-bridge">
        ↓ The five maintenance duties below run continuously inside TiDB to prevent all three.
      </div>

```

- [ ] **Step 4: Append CSS to `style.css`**

Append after the last rule in `style.css` (before the `@media` queries, after line ~919):

```css
/* ── Failure Modes panel (lifecycle tab) ── */
.failure-modes-section {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 12px;
}
.failure-modes-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.failure-modes-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.failure-mode-card {
  background: var(--panel-2);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-top: 3px solid var(--accent-2);
}
.failure-icon { font-size: 26px; }
.failure-name {
  font-size: 15px;
  font-weight: 700;
  color: var(--fg);
}
.failure-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.55;
  flex: 1;
}
.failure-signal {
  font-size: 11px;
  color: var(--accent-2);
  font-style: italic;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}
.failure-to-solution-bridge {
  text-align: center;
  font-size: 13px;
  color: var(--muted);
  padding: 8px;
  margin-bottom: 12px;
  font-style: italic;
}
@media (max-width: 900px) {
  .failure-modes-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 5: Run tests**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 5 PASS.

- [ ] **Step 6: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 34+ PASS, 0 FAIL.

- [ ] **Step 7: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: add three failure modes panel to lifecycle tab"
```

---

## Task 3: Lifecycle Tab — "Why TiDB Makes This Possible" Strip

**What this does:** Adds a 4-card strip *after* the duty grid and panel-footer in the lifecycle tab, explaining the four TiDB capabilities that make all five memory duties possible: Unified HTAP+Vector, SQL+Vector in one query, MCP integration, Zero-ETL reasoning.

**Files:**
- Modify: `booth_dashboard/static/index.html` (lifecycle tab, after `.panel-footer`)
- Modify: `booth_dashboard/static/style.css` (append why-tidb styles)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test**

Open `tests/test_index_html_structure.py` and append:

```python

def test_lifecycle_tab_has_why_tidb_strip():
    """Task 3: Lifecycle tab should have the Why TiDB 4-card strip."""
    assert "why-tidb-strip" in HTML
    assert "Unified HTAP" in HTML
    assert "VEC_COSINE_DISTANCE" in HTML
    assert "MCP integration" in HTML
    assert "Zero-ETL" in HTML
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_lifecycle_tab_has_why_tidb_strip -v
```

Expected: FAIL.

- [ ] **Step 3: Add the Why TiDB strip HTML in `index.html`**

Find the lifecycle tab's closing `</section>` tag. It follows:
```html
      <div class="panel-footer ok">
        All five duties run inside a <strong>single TiDB cluster</strong>.
        No external schedulers. No sync jobs. No Kafka, Redis, or Airflow.
      </div>
    </section>
```

Insert the why-tidb strip immediately before `</section>`:

```html

      <!-- ── Why TiDB strip ── -->
      <div class="why-tidb-strip">
        <div class="why-tidb-heading">Why TiDB makes all five duties possible:</div>
        <div class="why-tidb-grid">
          <div class="why-tidb-card">
            <div class="why-tidb-icon">⚡</div>
            <div class="why-tidb-title">Unified HTAP + Vector</div>
            <div class="why-tidb-desc">
              SQL, analytics, and semantic search in one engine.
              No ETL pipeline to maintain. No sync lag between systems.
            </div>
          </div>
          <div class="why-tidb-card">
            <div class="why-tidb-icon">🔗</div>
            <div class="why-tidb-title">Vector + SQL in one query</div>
            <div class="why-tidb-desc">
              JOIN embeddings against transactions in a single statement.
              <code>VEC_COSINE_DISTANCE()</code> is a SQL function.
            </div>
          </div>
          <div class="why-tidb-card">
            <div class="why-tidb-icon">🔌</div>
            <div class="why-tidb-title">MCP integration</div>
            <div class="why-tidb-desc">
              Agents provision and query TiDB directly from Claude, Cursor,
              and GitHub Copilot via the Model Context Protocol.
            </div>
          </div>
          <div class="why-tidb-card">
            <div class="why-tidb-icon">📡</div>
            <div class="why-tidb-title">Zero-ETL real-time reasoning</div>
            <div class="why-tidb-desc">
              Write to one place. Reason across everything instantly.
              No batch jobs, no Kafka topics, no Airflow DAGs.
            </div>
          </div>
        </div>
      </div>

```

- [ ] **Step 4: Append CSS to `style.css`**

Append before the `@media` queries:

```css
/* ── Why TiDB strip (lifecycle tab) ── */
.why-tidb-strip {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-top: 14px;
  border: 1px solid rgba(43, 217, 161, 0.35);
}
.why-tidb-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--ok);
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.why-tidb-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}
.why-tidb-card {
  background: var(--panel-2);
  border-radius: var(--radius);
  padding: 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 6px;
  border-top: 3px solid var(--ok);
}
.why-tidb-icon { font-size: 22px; }
.why-tidb-title {
  font-size: 14px;
  font-weight: 700;
  color: var(--fg);
}
.why-tidb-desc {
  font-size: 12.5px;
  color: var(--muted);
  line-height: 1.55;
}
.why-tidb-desc code {
  color: var(--ok);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11.5px;
  background: var(--panel-3);
  padding: 1px 4px;
  border-radius: 3px;
}
@media (max-width: 1100px) {
  .why-tidb-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 700px) {
  .why-tidb-grid { grid-template-columns: 1fr; }
}
```

- [ ] **Step 5: Run tests**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 6 PASS.

- [ ] **Step 6: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 35+ PASS, 0 FAIL.

- [ ] **Step 7: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: add Why TiDB 4-card capability strip to lifecycle tab"
```

---

## Task 4: New "Why TiDB" Tab — Pain Points, Solutions, and AI Scenarios

**What this does:** Adds a new "⚡ Why TiDB" tab (between Cross-Session Proof and Scale) with two sections: (1) four AI infrastructure pain points with TiDB solutions, (2) four AI patterns that become possible.

**Files:**
- Modify: `booth_dashboard/static/index.html` (add tab button + full panel; placed after `proof` tab button and before `fleet` tab button)
- Modify: `booth_dashboard/static/style.css` (append pain points + scenarios styles)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test**

Open `tests/test_index_html_structure.py` and append:

```python

def test_why_tidb_tab_exists():
    """Task 4: New Why TiDB tab should contain pain points and AI scenarios."""
    assert 'data-tab="whytidb"' in HTML
    assert 'data-tab-panel="whytidb"' in HTML
    assert "Memory fragmentation" in HTML
    assert "Vector + SQL" in HTML
    assert "Multi-tenant isolation" in HTML
    assert "Schema migrations" in HTML
    assert "Agent Long-Term Memory" in HTML
    assert "RAG Unified Storage" in HTML
    assert "AI SaaS Multi-Tenancy" in HTML
    assert "Real-time Feature Library" in HTML
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_why_tidb_tab_exists -v
```

Expected: FAIL.

- [ ] **Step 3: Add the tab button in `index.html`**

Find the tab bar `<nav class="tabs">`. It currently contains buttons ending with `data-tab="fleet"`. Add a new button *before* the fleet button:

Find:
```html
    <button class="tab" data-tab="fleet">🌐 Scale: 10M Agents</button>
```

Insert before it:
```html
    <button class="tab" data-tab="whytidb">⚡ Why TiDB</button>
```

- [ ] **Step 4: Add the full tab panel HTML in `index.html`**

Find the fleet tab section which starts with:
```html
    <!-- ── Tab 5: Fleet (10M Agents) ── -->
    <section class="tab-panel" data-tab-panel="fleet">
```

Insert the entire new panel immediately before that section:

```html
    <!-- ── Tab: Why TiDB ── -->
    <section class="tab-panel" data-tab-panel="whytidb">
      <div class="panel-hero">
        <div class="panel-title">TiDB for AI — built for all five memory duties</div>
        <div class="panel-sub">
          Every AI team hits the same four infrastructure walls. Here is why TiDB is the
          only database that tears them down — and the four patterns that become possible
          once it does.
        </div>
      </div>

      <!-- ── Four AI Pain Points ── -->
      <div class="pain-section">
        <div class="pain-section-heading">The four walls AI teams hit</div>
        <div class="pain-grid">

          <div class="pain-card">
            <div class="pain-header">
              <div class="pain-number">01</div>
              <div class="pain-title">Memory fragmentation</div>
            </div>
            <div class="pain-problem">
              Agent memory scattered across a vector DB, a KV cache, an OLTP database,
              and an analytics warehouse. Every write hits four systems.
              Sync lag means the agent sees yesterday's facts today.
            </div>
            <div class="pain-solution">
              <div class="solution-label">TiDB solution</div>
              <div class="solution-text">
                One unified engine. SQL + Vector + FTS + JSON + analytics in a single cluster.
                Zero sync code, zero lag, one consistency model.
              </div>
            </div>
          </div>

          <div class="pain-card">
            <div class="pain-header">
              <div class="pain-number">02</div>
              <div class="pain-title">Vector + SQL can't join</div>
            </div>
            <div class="pain-problem">
              Semantic search lives in Pinecone. Structured data lives in Postgres.
              You can't JOIN embeddings against transactions — so agents can't correlate
              what they remember with what actually happened.
            </div>
            <div class="pain-solution">
              <div class="solution-label">TiDB solution</div>
              <div class="solution-text">
                <code>VEC_COSINE_DISTANCE()</code> is a SQL function.
                Join embeddings against any table in a single statement.
              </div>
            </div>
          </div>

          <div class="pain-card">
            <div class="pain-header">
              <div class="pain-number">03</div>
              <div class="pain-title">Multi-tenant isolation is expensive</div>
            </div>
            <div class="pain-problem">
              Separate databases per agent: ops nightmare and idle capacity everywhere.
              Shared tables: cross-tenant leakage risk. Neither scales past a few
              hundred agents without someone writing a lot of plumbing.
            </div>
            <div class="pain-solution">
              <div class="solution-label">TiDB solution</div>
              <div class="solution-text">
                Data Branching — millisecond copy-on-write isolation, per agent, pay-per-RU.
                Manus runs 10M+ agent databases this way.
              </div>
            </div>
          </div>

          <div class="pain-card">
            <div class="pain-header">
              <div class="pain-number">04</div>
              <div class="pain-title">Schema migrations block production</div>
            </div>
            <div class="pain-problem">
              Adding a confidence column to the memories table means a maintenance window.
              ALTER TABLE locks the entire dataset for hours while your agents sit idle
              and your on-call engineer watches a progress bar.
            </div>
            <div class="pain-solution">
              <div class="solution-label">TiDB solution</div>
              <div class="solution-text">
                Online DDL — add columns, change indexes, alter schemas without blocking
                a single query in production.
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- ── Four AI Scenarios ── -->
      <div class="scenarios-section">
        <div class="scenarios-heading">Four patterns that become possible</div>
        <div class="scenarios-grid">

          <div class="scenario-card">
            <div class="scenario-tag">Pattern 1</div>
            <div class="scenario-title">Agent Long-Term Memory</div>
            <div class="scenario-desc">
              Persistent memory across sessions. Hybrid search (vector + BM25) for
              precise recall. Confidence decay ensures stale facts expire automatically.
              Write control prevents hallucination persistence.
            </div>
            <div class="scenario-customers">
              <div class="scenario-customer-label">Used by:</div>
              <div class="scenario-customer-list">Manus · DeepSeek · Plaud · Kimi</div>
            </div>
            <div class="scenario-outcome">10M+ agent databases · 80% infrastructure cost reduction</div>
          </div>

          <div class="scenario-card">
            <div class="scenario-tag">Pattern 2</div>
            <div class="scenario-title">RAG Unified Storage</div>
            <div class="scenario-desc">
              Documents and embeddings in the same table.
              BM25 + vector search in one query. No external vector database to
              sync, scale, or pay for separately.
            </div>
            <div class="scenario-customers">
              <div class="scenario-customer-label">Used by:</div>
              <div class="scenario-customer-list">Dify.AI · Pinterest</div>
            </div>
            <div class="scenario-outcome">500K containers → 1 cluster · 90% ops overhead eliminated</div>
          </div>

          <div class="scenario-card">
            <div class="scenario-tag">Pattern 3</div>
            <div class="scenario-title">AI SaaS Multi-Tenancy</div>
            <div class="scenario-desc">
              Database branching gives each customer their own isolated environment
              in milliseconds. Pay-per-RU means idle tenants cost nothing.
              Full ACID isolation with zero cross-tenant leakage.
            </div>
            <div class="scenario-customers">
              <div class="scenario-customer-label">Used by:</div>
              <div class="scenario-customer-list">Manus · Dify.AI</div>
            </div>
            <div class="scenario-outcome">Millisecond isolation · zero cross-tenant leakage · scale-to-zero cost</div>
          </div>

          <div class="scenario-card">
            <div class="scenario-tag">Pattern 4</div>
            <div class="scenario-title">Real-time Feature Library</div>
            <div class="scenario-desc">
              Streaming telemetry + vector similarity + SQL aggregation in one query.
              Agents reason over real-time data without a separate feature store
              or batch pipeline.
            </div>
            <div class="scenario-customers">
              <div class="scenario-customer-label">Used by:</div>
              <div class="scenario-customer-list">Flipkart · Pinterest</div>
            </div>
            <div class="scenario-outcome">1.3M QPS · &lt;5ms P95 · 6 systems → 1</div>
          </div>

        </div>
      </div>
    </section>

```

- [ ] **Step 5: Append CSS to `style.css`**

Append before the `@media` queries:

```css
/* ── Why TiDB tab — pain points ── */
.pain-section {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 12px;
}
.pain-section-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.pain-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.pain-card {
  background: var(--panel-2);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border: 1px solid var(--border);
}
.pain-header {
  display: flex;
  gap: 10px;
  align-items: center;
}
.pain-number {
  font-size: 24px;
  font-weight: 800;
  color: var(--accent-2);
  line-height: 1;
  font-variant-numeric: tabular-nums;
}
.pain-title {
  font-size: 15px;
  font-weight: 700;
  color: var(--fg);
}
.pain-problem {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
}
.pain-solution {
  background: var(--panel-3);
  border-left: 3px solid var(--ok);
  border-radius: 0 6px 6px 0;
  padding: 8px 12px;
  margin-top: auto;
}
.solution-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--ok);
  font-weight: 700;
  margin-bottom: 4px;
}
.solution-text {
  font-size: 12.5px;
  color: var(--fg);
  line-height: 1.5;
}
.solution-text code {
  color: var(--ok);
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11.5px;
  background: var(--panel-2);
  padding: 1px 4px;
  border-radius: 3px;
}

/* ── Why TiDB tab — AI scenarios ── */
.scenarios-section {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 12px;
}
.scenarios-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.scenarios-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}
.scenario-card {
  background: var(--panel-2);
  border-radius: var(--radius);
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border: 1px solid var(--border);
  border-top: 3px solid var(--accent);
}
.scenario-tag {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  font-weight: 700;
}
.scenario-title {
  font-size: 16px;
  font-weight: 700;
  color: var(--fg);
}
.scenario-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
  flex: 1;
}
.scenario-customers {
  display: flex;
  gap: 6px;
  align-items: center;
  padding-top: 8px;
  border-top: 1px solid var(--border);
}
.scenario-customer-label {
  font-size: 10px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--muted);
  flex-shrink: 0;
}
.scenario-customer-list {
  font-size: 12px;
  color: var(--fg);
  font-weight: 600;
}
.scenario-outcome {
  font-size: 11.5px;
  color: var(--ok);
  font-style: italic;
}
@media (max-width: 900px) {
  .pain-grid       { grid-template-columns: 1fr; }
  .scenarios-grid  { grid-template-columns: 1fr; }
}
```

- [ ] **Step 6: Run tests**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 7 PASS.

- [ ] **Step 7: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 36+ PASS, 0 FAIL.

- [ ] **Step 8: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: add Why TiDB tab with four AI pain points and scenario patterns"
```

---

## Task 5: Fleet Tab Redesign — Scale Ladder + Proof Tiles

**What this does:** Replaces the confusing tiny-tiles visualization with: (a) three large customer proof stat tiles (Manus/Pinterest/Dify), (b) a clean scale ladder (1 → 100 → 10K → 1M → 10M+), (c) a context stats row. Removes the tile-spawn JavaScript (it's dead code once the HTML is replaced). The existing fleet HTML in `index.html` is replaced entirely.

**Files:**
- Modify: `booth_dashboard/static/index.html` (replace entire fleet tab panel)
- Modify: `booth_dashboard/static/style.css` (append scale ladder + proof tile styles)
- Modify: `booth_dashboard/static/app.js` (remove `bindFleetControls`, `spawnTiles`, `pickTiming`, `loadFleetMeasurements`; remove their calls from `bootstrap` and `DOMContentLoaded`)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test**

Open `tests/test_index_html_structure.py` and append:

```python

def test_fleet_tab_has_scale_ladder():
    """Task 5: Fleet tab should have scale ladder and proof tiles, not tile grid."""
    assert "scale-ladder" in HTML
    assert "scale-proof-tiles" in HTML
    assert "10M+" in HTML
    # Old tile grid buttons should be gone
    assert "spawn-100" not in HTML
    assert "spawn-10000" not in HTML
    assert "fleet-grid" not in HTML
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_fleet_tab_has_scale_ladder -v
```

Expected: FAIL.

- [ ] **Step 3: Replace the fleet tab HTML in `index.html`**

Find the entire fleet tab section:
```html
    <!-- ── Tab 5: Fleet (10M Agents) ── -->
    <section class="tab-panel" data-tab-panel="fleet">
      ...
    </section>
```

Replace the entire section (from the opening comment through `</section>`) with:

```html
    <!-- ── Tab: Scale ── -->
    <section class="tab-panel" data-tab-panel="fleet">
      <div class="panel-hero">
        <div class="panel-title">One cluster. Unlimited agents.</div>
        <div class="panel-sub">
          TiDB Cloud Zero provisions a fully isolated database for every agent in milliseconds
          using copy-on-write branching — not spinning up new clusters. Manus runs 10M+ this way.
          Each agent is isolated. None of them share a table. All of them share one TiDB cluster.
        </div>
      </div>

      <!-- ── Three customer proof stat tiles ── -->
      <div class="scale-proof-tiles">
        <div class="scale-proof-tile manus-tile">
          <div class="spt-customer">Manus</div>
          <div class="spt-stat">10M+</div>
          <div class="spt-unit">agent databases</div>
          <div class="spt-detail">80% infrastructure cost reduction · 100% provisioned by AI agents · migrated in 2 weeks</div>
        </div>
        <div class="scale-proof-tile pinterest-tile">
          <div class="spt-customer">Pinterest</div>
          <div class="spt-stat">1.3M</div>
          <div class="spt-unit">queries per second</div>
          <div class="spt-detail">6 systems → 1 TiDB cluster · 80% cost reduction · 3–5× p99 improvement</div>
        </div>
        <div class="scale-proof-tile dify-tile">
          <div class="spt-customer">Dify.AI</div>
          <div class="spt-stat">500K</div>
          <div class="spt-unit">containers → 1 cluster</div>
          <div class="spt-detail">90% operations overhead eliminated · same performance, fraction of the cost</div>
        </div>
      </div>

      <!-- ── Scale Ladder ── -->
      <div class="scale-ladder-section">
        <div class="scale-ladder-heading">From one agent to ten million — same cluster, same provisioning time</div>
        <div class="scale-ladder">

          <div class="scale-rung">
            <div class="rung-count">1</div>
            <div class="rung-body">
              <div class="rung-track"><div class="rung-fill" style="width:3%"></div></div>
              <div class="rung-label">One agent. One isolated database. Provisioned in milliseconds from cold.</div>
              <div class="rung-tech">TiDB Cloud Zero · copy-on-write branch · ~900ms median</div>
            </div>
          </div>

          <div class="scale-rung">
            <div class="rung-count">100</div>
            <div class="rung-body">
              <div class="rung-track"><div class="rung-fill" style="width:8%"></div></div>
              <div class="rung-label">A team of agents. Each isolated. Zero shared state between any of them.</div>
              <div class="rung-tech">Pay-per-RU · idle agents cost nothing · scale to zero</div>
            </div>
          </div>

          <div class="scale-rung">
            <div class="rung-count">10K</div>
            <div class="rung-body">
              <div class="rung-track"><div class="rung-fill" style="width:22%"></div></div>
              <div class="rung-label">Product launch. Every user gets their own agent memory store.</div>
              <div class="rung-tech">Resource groups · no noisy neighbors · per-tenant RU caps</div>
            </div>
          </div>

          <div class="scale-rung">
            <div class="rung-count">1M</div>
            <div class="rung-body">
              <div class="rung-track"><div class="rung-fill" style="width:55%"></div></div>
              <div class="rung-label">SaaS scale. Dify.AI runs this with 90% less ops overhead than before TiDB.</div>
              <div class="rung-tech">Horizontal scale · TiDB X elastic compute/storage · HTAP on the same cluster</div>
            </div>
          </div>

          <div class="scale-rung highlight-rung">
            <div class="rung-count">10M+</div>
            <div class="rung-body">
              <div class="rung-track"><div class="rung-fill" style="width:100%"></div></div>
              <div class="rung-label">Manus scale. 10M+ databases. Billions of events per day. One cluster.</div>
              <div class="rung-tech">One TiDB cluster · 2-week migration · 80% cost reduction · 100% agent-provisioned</div>
            </div>
          </div>

        </div>
      </div>

      <!-- ── Context stats row ── -->
      <div class="fleet-context-strip">
        <div class="fleet-context-item">
          <div class="fci-stat">~900ms</div>
          <div class="fci-label">median provision time</div>
        </div>
        <div class="fleet-context-item">
          <div class="fci-stat">0</div>
          <div class="fci-label">shared tables · zero cross-tenant leakage</div>
        </div>
        <div class="fleet-context-item">
          <div class="fci-stat">$0</div>
          <div class="fci-label">cost when idle · pay-per-RU serverless</div>
        </div>
        <div class="fleet-context-item">
          <div class="fci-stat">ACID</div>
          <div class="fci-label">everywhere · no eventual consistency</div>
        </div>
      </div>

      <div class="fleet-band">
        All agents share <strong>one TiDB cluster</strong> underneath —
        full isolation, zero shared state, pay for what you use.
      </div>

      <div class="fleet-scale-refs">
        <div class="scale-ref">Manus: 10M+ agent DBs</div>
        <div class="scale-ref">Pinterest: 1.3M QPS</div>
        <div class="scale-ref">Flipkart: 700+ MySQL → 1</div>
        <div class="scale-ref">Dify.AI: 500K → 1 cluster</div>
        <div class="scale-ref">DeepSeek: AI agents on TiDB</div>
        <div class="scale-ref">Plaud: AI agents on TiDB</div>
        <div class="scale-ref">Kimi: AI agents on TiDB</div>
      </div>
    </section>
```

- [ ] **Step 4: Remove fleet tile functions from `app.js`**

Open `booth_dashboard/static/app.js`.

(a) In `document.addEventListener("DOMContentLoaded", ...)` remove the `bindFleetControls();` call and remove the `await loadFleetMeasurements();` call from `bootstrap()`.

The `DOMContentLoaded` handler should become:
```js
document.addEventListener("DOMContentLoaded", () => {
  bindTabs();
  bindQueryRail();
  bindChatControls();
  bootstrap();
});
```

The `bootstrap()` function should become:
```js
async function bootstrap() {
  const [meta, canned] = await Promise.all([fetchMeta(), fetchCanned()]);
  CANNED_CACHE = canned;
  renderTopStrip(meta);
  pollMemoryCount();
}
```

(b) Remove the entire `// ----- Fleet tab -----` section (lines roughly 265–328), which contains:
- `let FLEET_MEASUREMENTS = [];`
- `async function loadFleetMeasurements() { ... }`
- `function bindFleetControls() { ... }`
- `function spawnTiles(n) { ... }`
- `function pickTiming(i) { ... }`

- [ ] **Step 5: Append CSS to `style.css`**

Append before the `@media` queries:

```css
/* ── Scale Proof Tiles (fleet tab) ── */
.scale-proof-tiles {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-bottom: 14px;
}
.scale-proof-tile {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  border-top: 4px solid var(--accent);
}
.manus-tile    { border-top-color: var(--ok);      }
.pinterest-tile { border-top-color: var(--accent);  }
.dify-tile     { border-top-color: var(--warn);    }
.spt-customer {
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--muted);
  margin-bottom: 4px;
}
.spt-stat {
  font-size: 44px;
  font-weight: 800;
  line-height: 1;
}
.manus-tile    .spt-stat { color: var(--ok);     }
.pinterest-tile .spt-stat { color: var(--accent); }
.dify-tile     .spt-stat { color: var(--warn);   }
.spt-unit {
  font-size: 14px;
  color: var(--muted);
  margin-bottom: 6px;
}
.spt-detail {
  font-size: 11.5px;
  color: var(--muted);
  font-style: italic;
  border-top: 1px solid var(--border);
  padding-top: 8px;
  line-height: 1.5;
}

/* ── Scale Ladder ── */
.scale-ladder-section {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 20px 24px;
  margin-bottom: 14px;
}
.scale-ladder-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--fg);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.scale-ladder {
  display: flex;
  flex-direction: column;
  gap: 0;
}
.scale-rung {
  display: grid;
  grid-template-columns: 72px 1fr;
  gap: 14px;
  align-items: start;
  padding: 12px 0;
  border-bottom: 1px solid var(--border);
}
.scale-rung:last-child { border-bottom: none; }
.highlight-rung {
  background: rgba(43, 217, 161, 0.06);
  border-radius: 8px;
  padding: 12px 10px;
  border: 1px solid rgba(43, 217, 161, 0.25) !important;
  margin: 4px 0;
}
.rung-count {
  font-size: 16px;
  font-weight: 800;
  color: var(--muted);
  font-variant-numeric: tabular-nums;
  text-align: right;
  padding-top: 2px;
}
.highlight-rung .rung-count { color: var(--ok); font-size: 20px; }
.rung-body {
  display: flex;
  flex-direction: column;
  gap: 5px;
}
.rung-track {
  height: 8px;
  background: var(--panel-3);
  border-radius: 4px;
  overflow: hidden;
}
.rung-fill {
  height: 100%;
  background: var(--accent);
  border-radius: 4px;
}
.highlight-rung .rung-fill { background: var(--ok); }
.rung-label {
  font-size: 13px;
  color: var(--fg);
  line-height: 1.4;
}
.rung-tech {
  font-size: 11px;
  color: var(--muted);
  font-style: italic;
}

/* ── Fleet context strip ── */
.fleet-context-strip {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 10px;
}
.fleet-context-item {
  background: var(--panel);
  border-radius: var(--radius);
  padding: 14px 16px;
  text-align: center;
  border: 1px solid var(--border);
}
.fci-stat {
  font-size: 22px;
  font-weight: 800;
  color: var(--ok);
  margin-bottom: 4px;
}
.fci-label {
  font-size: 11.5px;
  color: var(--muted);
  line-height: 1.4;
}
@media (max-width: 900px) {
  .scale-proof-tiles     { grid-template-columns: 1fr; }
  .fleet-context-strip   { grid-template-columns: repeat(2, 1fr); }
}
```

- [ ] **Step 6: Run tests (including no-innerHTML on modified app.js)**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 8 PASS.

- [ ] **Step 7: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 37+ PASS, 0 FAIL.

- [ ] **Step 8: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css booth_dashboard/static/app.js tests/test_index_html_structure.py && git commit -m "feat: redesign fleet tab with scale ladder and customer proof tiles; remove tile-spawn JS"
```

---

## Task 6: Business Outcome Footer Strips on Every Tab

**What this does:** Adds a `.tab-outcome-strip` at the bottom of each of the six existing tab panels (queryflow, chat, lifecycle, unified, proof, whytidb). Each strip has 2 short outcome bullets with dollar/scale evidence. The fleet (scale) tab already has a `fleet-band` — skip it to avoid clutter.

**Files:**
- Modify: `booth_dashboard/static/index.html` (6 outcome strips, one per tab panel, each before `</section>`)
- Modify: `booth_dashboard/static/style.css` (append outcome strip styles)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test**

Open `tests/test_index_html_structure.py` and append:

```python

def test_tabs_have_outcome_strips():
    """Task 6: Each tab panel should have at least one tab-outcome-strip."""
    import re
    strips = re.findall(r'tab-outcome-strip', HTML)
    # Expect at least 5 (one per tab: queryflow, chat, lifecycle, unified, proof, whytidb)
    assert len(strips) >= 5, f"Expected at least 5 outcome strips, found {len(strips)}"
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_tabs_have_outcome_strips -v
```

Expected: FAIL.

- [ ] **Step 3: Add outcome strips to each tab in `index.html`**

For each tab panel listed below, find its closing `</section>` and insert the outcome strip HTML immediately before it.

**Tab: queryflow (Live Recall)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">💡</span>
          <span class="outcome-text">Hybrid search eliminates the need for a separate vector database — one TiDB table replaces three systems</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">⚡</span>
          <span class="outcome-text">Three search engines, one SQL query, one ranked result — no orchestration layer required</span>
        </div>
      </div>
```

**Tab: chat (Ask the Agent)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">🎯</span>
          <span class="outcome-text">Agents answer with cited, verifiable memories — hallucinations become auditable</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">🔍</span>
          <span class="outcome-text">Context plane assembled pre-agent — zero prompt engineering, zero context stuffing</span>
        </div>
      </div>
```

**Tab: lifecycle (5 Memory Duties)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">🏗️</span>
          <span class="outcome-text">All five duties run in one TiDB cluster — no Airflow, no Redis, no Kafka, no sync jobs</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">📊</span>
          <span class="outcome-text">Manus: 10M+ agent databases · 80% infrastructure cost reduction · 100% agent-provisioned</span>
        </div>
      </div>
```

**Tab: unified (One Cluster)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">🔒</span>
          <span class="outcome-text">ACID everywhere — one consistency model replaces four, eliminating an entire class of sync bugs</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">📉</span>
          <span class="outcome-text">Flipkart: 700+ MySQL clusters → 1 TiDB · 1M QPS · P95 under 5ms · massive ops reduction</span>
        </div>
      </div>
```

**Tab: proof (Cross-Session Proof)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">🧠</span>
          <span class="outcome-text">Stateless model. Stateful platform. DeepSeek, Plaud, and Kimi build agent memory this way.</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">🔄</span>
          <span class="outcome-text">Cross-session learning without sharing model weights — any agent, any language, any framework</span>
        </div>
      </div>
```

**Tab: whytidb (Why TiDB)**

```html
      <div class="tab-outcome-strip">
        <div class="outcome-item">
          <span class="outcome-icon">🚀</span>
          <span class="outcome-text">The only database where SQL JOINs embeddings against transactions in a single statement</span>
        </div>
        <div class="outcome-divider"></div>
        <div class="outcome-item">
          <span class="outcome-icon">✅</span>
          <span class="outcome-text">Online DDL, Data Branching, HTAP — in production today, not on the roadmap</span>
        </div>
      </div>
```

- [ ] **Step 4: Append CSS to `style.css`**

Append before the `@media` queries:

```css
/* ── Business outcome footer strips ── */
.tab-outcome-strip {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 18px;
  background: linear-gradient(135deg, var(--panel-3) 0%, var(--panel-2) 100%);
  border-radius: var(--radius);
  border-left: 4px solid var(--ok);
  margin-top: 14px;
  flex-wrap: wrap;
}
.outcome-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--fg);
  line-height: 1.4;
  flex: 1;
  min-width: 240px;
}
.outcome-icon { font-size: 16px; flex-shrink: 0; }
.outcome-divider {
  width: 1px;
  height: 32px;
  background: var(--border);
  flex-shrink: 0;
}
@media (max-width: 700px) {
  .outcome-divider { display: none; }
  .outcome-item { min-width: 100%; }
}
```

- [ ] **Step 5: Run tests**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 9 PASS.

- [ ] **Step 6: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 38+ PASS, 0 FAIL.

- [ ] **Step 7: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: add business outcome footer strips to all tab panels"
```

---

## Task 7: Closing CTA Strip — "Stop Prompting. Start Maintaining."

**What this does:** Adds a bold closing strip at the very bottom of the page (inside `<body>`, after `</main>`, before `</body>`). Contains the narrative payoff line, a one-paragraph summary, and two CTA links.

**Files:**
- Modify: `booth_dashboard/static/index.html` (add `<footer class="closing-strip">` before `</body>`)
- Modify: `booth_dashboard/static/style.css` (append closing strip styles)
- Modify: `tests/test_index_html_structure.py` (append test function)

---

- [ ] **Step 1: Append the failing test**

Open `tests/test_index_html_structure.py` and append:

```python

def test_closing_strip_exists():
    """Task 7: Closing strip with the payoff line should be present."""
    assert "closing-strip" in HTML
    assert "Stop prompting" in HTML
    assert "Start maintaining" in HTML
```

- [ ] **Step 2: Run to verify it fails**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py::test_closing_strip_exists -v
```

Expected: FAIL.

- [ ] **Step 3: Add the closing strip to `index.html`**

Find the line `</body>` near the bottom of `index.html`. Insert immediately before it:

```html

  <!-- ── Closing CTA strip ── -->
  <footer class="closing-strip">
    <div class="closing-tagline">Stop prompting. Start maintaining.</div>
    <div class="closing-sub">
      Memory is not a feature you bolt on. It is infrastructure you maintain —
      write, dedup, reconcile, decay, compact. TiDB runs all five duties in one cluster,
      from one agent to ten million, with ACID guarantees at every step.
    </div>
    <div class="closing-summary">
      TiDB = Unified Data Foundation for the AI Era
    </div>
    <div class="closing-cta-row">
      <a class="closing-cta-primary" href="https://mem9.ai" target="_blank" rel="noopener">Try mem9 free</a>
      <a class="closing-cta-secondary" href="https://docs.pingcap.com/ai" target="_blank" rel="noopener">TiDB AI docs</a>
    </div>
  </footer>

```

- [ ] **Step 4: Append CSS to `style.css`**

Append before the `@media` queries:

```css
/* ── Closing CTA strip ── */
.closing-strip {
  background: linear-gradient(135deg, #0d1b35 0%, #0b1220 100%);
  border-top: 1px solid var(--border);
  padding: 36px 24px 28px;
  text-align: center;
}
.closing-tagline {
  font-size: 30px;
  font-weight: 800;
  color: var(--fg);
  margin-bottom: 12px;
  letter-spacing: -0.02em;
  line-height: 1.1;
}
.closing-sub {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.7;
  max-width: 620px;
  margin: 0 auto 10px;
}
.closing-summary {
  font-size: 13px;
  color: var(--ok);
  font-weight: 600;
  letter-spacing: 0.04em;
  margin-bottom: 20px;
}
.closing-cta-row {
  display: flex;
  gap: 12px;
  justify-content: center;
}
.closing-cta-primary {
  background: var(--ok);
  color: #0b1220;
  text-decoration: none;
  padding: 12px 28px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 14px;
  transition: filter 0.15s;
}
.closing-cta-primary:hover { filter: brightness(1.1); }
.closing-cta-secondary {
  background: var(--panel-2);
  color: var(--fg);
  text-decoration: none;
  padding: 12px 28px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 14px;
  border: 1px solid var(--border);
  transition: border-color 0.15s;
}
.closing-cta-secondary:hover { border-color: var(--accent); }
@media (max-width: 600px) {
  .closing-tagline { font-size: 22px; }
  .closing-cta-row { flex-direction: column; align-items: center; }
}
```

- [ ] **Step 5: Run tests**

```bash
cd /Users/stephen/mem9-demo && pytest tests/test_index_html_structure.py tests/test_no_innerhtml.py -v
```

Expected: 10 PASS.

- [ ] **Step 6: Run full suite**

```bash
cd /Users/stephen/mem9-demo && pytest -x -q
```

Expected: 39+ PASS, 0 FAIL.

- [ ] **Step 7: Commit**

```bash
cd /Users/stephen/mem9-demo && git add booth_dashboard/static/index.html booth_dashboard/static/style.css tests/test_index_html_structure.py && git commit -m "feat: add closing CTA strip — Stop prompting. Start maintaining."
```

---

## Self-Review Checklist

- [ ] **Spec coverage:** All P0 (hero, outcome strips), P1 (failure modes, fleet redesign), P2 (Why TiDB strip, closing strip) requirements have corresponding tasks. The new "Why TiDB" tab covers pain points, comparison, and AI scenarios. Customer examples (DeepSeek, Plaud, Kimi) appear in Tasks 1, 4, 5, 6.
- [ ] **No placeholders:** Every step contains actual HTML/CSS/JS. No TBDs.
- [ ] **Type consistency:** CSS class names used in `index.html` HTML match what's defined in `style.css` CSS in the same task. Names checked: `scale-proof-tile`, `spt-stat`, `spt-unit`, `spt-detail`, `rung-fill`, `rung-track`, `rung-body`, `rung-count`, `fleet-context-strip`, `fci-stat`, `fci-label` — all consistent.
- [ ] **innerHTML check:** No task introduces `innerHTML` anywhere. All DOM content is written as `textContent` in app.js or as literal HTML in index.html (which is safe).
- [ ] **Task independence:** Each task can be executed by a fresh subagent who reads only their task. Each task specifies exact file paths, what to find, and what to replace. No task assumes knowledge from a sibling task.
