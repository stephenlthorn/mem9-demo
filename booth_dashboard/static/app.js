// booth_dashboard/static/app.js
// Safe DOM only: createElement + textContent. No unsafe property assignments.

const PATHS = { meta: "/meta", canned: "/canned", api: "/api", chat: "/chat" };
const QUERIES = { q1: "What does Sam think about TypeScript?",
                  q2: "Who does Sam report to?",
                  q3: "What slowed down the research pipeline recently?" };
const ANNOTATIONS = {
  q1: "Vector-only win. 'TypeScript' never appears in this memory - semantic similarity surfaces the Python preference anyway.",
  q2: "Baseline sanity. Both FTS and vector signals strong - recall works normally.",
  q3: "Hybrid beats either alone. FTS hits 'pipeline'; vector pulls 'latency regression'.",
};

let CANNED_CACHE = null;
let OFFLINE = new URLSearchParams(location.search).has("offline");

document.addEventListener("DOMContentLoaded", () => {
  bindTabs();
  bindQueryRail();
  bindFleetControls();
  bindChatControls();
  bootstrap();
});

async function bootstrap() {
  const [meta, canned] = await Promise.all([fetchMeta(), fetchCanned()]);
  CANNED_CACHE = canned;
  renderTopStrip(meta);
  pollMemoryCount();
  await loadFleetMeasurements();
}

async function fetchMeta() {
  try {
    const r = await fetch(PATHS.meta);
    if (!r.ok) throw new Error("meta " + r.status);
    return await r.json();
  } catch (e) {
    return { tenant_id: null, provision_ms: null };
  }
}

async function fetchCanned() {
  const r = await fetch(PATHS.canned);
  return await r.json();
}

function renderTopStrip(meta) {
  setText("tenant-value", meta.tenant_id ? shorten(meta.tenant_id) : "not provisioned");
  setText("provision-value", meta.provision_ms != null ? `${meta.provision_ms} ms` : "-");
}

function shorten(id) {
  if (id.length <= 10) return id;
  return id.slice(0, 6) + "..." + id.slice(-4);
}

function setText(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}

async function pollMemoryCount() {
  const el = document.getElementById("memories-value");
  if (!el) return;
  let stable = 0;
  let last = -1;
  async function tick() {
    try {
      const r = await fetch(PATHS.api + "/v1alpha2/mem9s/memories?limit=1&count=true");
      if (!r.ok) throw new Error("count " + r.status);
      const body = await r.json();
      const count = body.total ?? (body.hits ? body.hits.length : 0);
      el.textContent = String(count);
      if (count === last) stable += 1; else stable = 0;
      last = count;
      if (stable < 3) setTimeout(tick, 2000);
    } catch (e) {
      el.textContent = OFFLINE ? "50 (offline)" : "?";
    }
  }
  tick();
}

function bindTabs() {
  document.querySelectorAll(".tab").forEach((btn) => {
    btn.addEventListener("click", () => {
      const target = btn.dataset.tab;
      document.querySelectorAll(".tab").forEach((b) => b.classList.toggle("active", b === btn));
      document.querySelectorAll(".tab-panel").forEach((p) => {
        p.classList.toggle("active", p.dataset.tabPanel === target);
      });
    });
  });
}

function bindQueryRail() {
  document.querySelectorAll(".query").forEach((btn) => {
    btn.addEventListener("click", () => runQuery(btn.dataset.q, btn));
  });
}

async function runQuery(qKey, btn) {
  document.querySelectorAll(".query").forEach((b) => b.classList.toggle("active", b === btn));
  playDiagramAnimation(qKey);

  let payload = null;
  if (!OFFLINE) {
    try {
      const r = await fetch(
        PATHS.api + "/v1alpha2/mem9s/memories?q=" + encodeURIComponent(QUERIES[qKey]) + "&limit=3"
      );
      if (r.ok) payload = await r.json();
    } catch (e) { /* fall through to canned */ }
  }
  if (!payload && CANNED_CACHE) {
    payload = { hits: CANNED_CACHE[qKey].hits };
  }
  renderResults(qKey, payload || { hits: [] });
}

function renderResults(qKey, payload) {
  const host = document.getElementById("results");
  clearChildren(host);

  // Query header
  const qHeader = document.createElement("div");
  qHeader.className = "result-query";
  qHeader.textContent = `"${QUERIES[qKey]}"`;
  host.appendChild(qHeader);

  const meta = document.createElement("div");
  meta.className = "result-meta";
  meta.textContent = `Top ${payload.hits.length} memories retrieved`;
  host.appendChild(meta);

  // Score legend
  host.appendChild(buildScoreLegend());

  for (const hit of payload.hits) {
    host.appendChild(buildHitElement(hit));
  }

  // Annotation
  if (ANNOTATIONS[qKey]) {
    const noteWrap = document.createElement("div");
    noteWrap.className = "annotation";
    const noteLabel = document.createElement("div");
    noteLabel.className = "annotation-label";
    noteLabel.textContent = "Why this result is interesting";
    noteWrap.appendChild(noteLabel);
    const noteText = document.createElement("div");
    noteText.textContent = ANNOTATIONS[qKey];
    noteWrap.appendChild(noteText);
    host.appendChild(noteWrap);
  }
}

function buildScoreLegend() {
  const legend = document.createElement("div");
  legend.className = "score-legend";
  const items = [
    { cls: "v", label: "Vector — semantic similarity (meaning, not keywords)" },
    { cls: "f", label: "FTS — full-text search (exact keyword match)" },
    { cls: "h", label: "Hybrid — mem9 blends both signals" },
  ];
  for (const { cls, label } of items) {
    const item = document.createElement("div");
    item.className = "score-legend-item";
    const bar = document.createElement("span");
    bar.className = `score-legend-bar ${cls}`;
    const text = document.createElement("span");
    text.textContent = label;
    item.appendChild(bar);
    item.appendChild(text);
    legend.appendChild(item);
  }
  return legend;
}

function buildHitElement(hit) {
  const row = document.createElement("div");
  row.className = "hit";

  const content = document.createElement("div");
  content.className = "hit-content";
  content.textContent = hit.content;
  row.appendChild(content);

  const bars = document.createElement("div");
  bars.className = "score-bars";
  const s = hit.scores || { vector: 0, fts: 0, hybrid: 0 };
  bars.appendChild(buildScoreRow("vector", s.vector, ""));
  bars.appendChild(buildScoreRow("FTS", s.fts, "fts"));
  bars.appendChild(buildScoreRow("hybrid", s.hybrid, "hybrid"));
  row.appendChild(bars);

  return row;
}

function buildScoreRow(labelText, value, flavor) {
  const row = document.createElement("div");
  row.className = "score-row";

  const label = document.createElement("span");
  label.textContent = labelText;
  row.appendChild(label);

  const track = document.createElement("span");
  track.className = "bar-track";
  const fill = document.createElement("span");
  fill.className = "bar-fill" + (flavor ? " " + flavor : "");
  fill.style.width = clampPct(value) + "%";
  track.appendChild(fill);
  row.appendChild(track);

  const num = document.createElement("span");
  num.textContent = value != null ? value.toFixed(2) : "-";
  row.appendChild(num);

  return row;
}

function clampPct(v) {
  const x = Number(v);
  if (!isFinite(x)) return 0;
  return Math.max(0, Math.min(100, Math.round(x * 100)));
}

function clearChildren(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

// ----- Diagram animation -----

function playDiagramAnimation(qKey) {
  const svgHost = document.getElementById("architecture-svg");
  const doc = svgHost && svgHost.contentDocument;
  if (!doc || !window.anime) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  const targets = {
    packet: doc.getElementById("packet"),
    fanV: doc.getElementById("fan-vector"),
    fanF: doc.getElementById("fan-fts"),
    fanM: doc.getElementById("fan-meta"),
    merge: doc.getElementById("merge"),
    result: doc.getElementById("result-packet"),
  };
  for (const [k, v] of Object.entries(targets)) {
    if (!v) return;
  }
  const accent = { q1: "#4cc9f0", q2: "#2bd9a1", q3: "#f72585" }[qKey] || "#4cc9f0";

  const timeline = anime.timeline({ duration: 800, easing: "easeInOutQuad" });
  timeline
    .add({ targets: targets.packet, translateX: [0, 160], opacity: [1, 1], duration: 200 })
    .add({ targets: [targets.fanV, targets.fanF, targets.fanM],
           opacity: [0.2, 1], fill: accent, duration: 200 }, "-=60")
    .add({ targets: targets.merge, scale: [0.8, 1.2, 1], duration: 200 })
    .add({ targets: targets.result, translateX: [320, 480], opacity: [0, 1], duration: 200 });
}

// ----- Fleet tab -----

let FLEET_MEASUREMENTS = [];

async function loadFleetMeasurements() {
  try {
    const r = await fetch("/static/fleet_measurements.json");
    if (r.ok) {
      const data = await r.json();
      FLEET_MEASUREMENTS = data.measurements_ms || [];
      setText("fleet-measured-count", FLEET_MEASUREMENTS.length);
    }
  } catch (e) { /* file may not exist yet */ }
}

function bindFleetControls() {
  document.getElementById("spawn-100").addEventListener("click", () => spawnTiles(100));
  document.getElementById("spawn-10000").addEventListener("click", () => spawnTiles(10000));
  document.getElementById("spawn-10m").addEventListener("click", () => spawnTiles(10_000_000));
}

function spawnTiles(n) {
  const host = document.getElementById("fleet-grid");
  clearChildren(host);

  const VISIBLE_CAP = 2500;
  const shown = Math.min(n, VISIBLE_CAP);
  const frag = document.createDocumentFragment();
  for (let i = 0; i < shown; i++) {
    const tile = document.createElement("div");
    tile.className = "fleet-tile" + (i >= FLEET_MEASUREMENTS.length ? " sim" : "");
    const ms = pickTiming(i);
    tile.title = `${ms} ms`;
    frag.appendChild(tile);
  }
  host.appendChild(frag);

  const note = document.getElementById("fleet-note");
  if (note) {
    note.textContent =
      n > VISIBLE_CAP
        ? `Showing ${VISIBLE_CAP.toLocaleString()} of ${n.toLocaleString()} tiles ` +
          `(measured ${FLEET_MEASUREMENTS.length}; rest extrapolated).`
        : `Showing ${shown.toLocaleString()} tiles ` +
          `(measured ${FLEET_MEASUREMENTS.length}; rest extrapolated).`;
  }

  if (!matchMedia("(prefers-reduced-motion: reduce)").matches && window.anime) {
    anime({
      targets: host.children,
      opacity: [0, 0.9],
      duration: 600,
      delay: anime.stagger(0.6, { from: "first" }),
      easing: "easeOutQuad",
    });
  }
}

function pickTiming(i) {
  if (i < FLEET_MEASUREMENTS.length) return FLEET_MEASUREMENTS[i];
  if (!FLEET_MEASUREMENTS.length) return 900;
  const base = FLEET_MEASUREMENTS[i % FLEET_MEASUREMENTS.length];
  const jitter = Math.round((Math.random() - 0.5) * 120);
  return Math.max(200, base + jitter);
}

// ----- Ask the Agent (chat) -----

// Matches either the canned short-id style ([mem_XXX]) or a UUID-shaped
// memory id ([d5fe1787-efd0-414f-9359-ade34a45e1fd]). Real mem9 tenants
// return UUIDs; the canned fixture uses short ids.
const CITE_REGEX = /\[(mem_[A-Za-z0-9_\-]+|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\]/g;
const MODE_LABELS = {
  live: "Live - MiniMax answering with memories from TiDB",
  "retrieval-only": "Retrieval-only - LLM unavailable, showing memories",
  canned: "Offline - using pre-recorded demo turn",
  error: "Something went wrong - check console",
};

function bindChatControls() {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  if (!form || !input) return;

  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;
    input.value = "";
    sendChat(text);
  });

  document.querySelectorAll(".chat-suggestion").forEach((btn) => {
    btn.addEventListener("click", () => {
      const text = btn.textContent.trim();
      input.value = "";
      sendChat(text);
    });
  });
}

async function sendChat(userText) {
  const sendBtn = document.getElementById("chat-send");
  const empty = document.querySelector("#chat-messages .chat-empty");
  if (empty) empty.remove();

  appendBubble("user", userText);
  const thinkingEl = appendBubble("agent", "thinking...", { thinking: true });
  if (sendBtn) sendBtn.disabled = true;

  try {
    const r = await fetch(PATHS.chat, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ message: userText }),
    });
    const payload = await r.json();

    thinkingEl.remove();

    const mode = payload.mode || "error";
    renderMemoryPane(payload.memories || [], mode);
    setChatMode(mode, payload.error);

    const answer = payload.answer ||
      (mode === "retrieval-only"
        ? "(LLM unavailable - memories shown on the right are what would have been passed to the agent.)"
        : "(No answer returned.)");
    appendBubble("agent", answer, { mode });
  } catch (e) {
    thinkingEl.remove();
    appendBubble("agent", "Network error - check the console.", { mode: "error" });
    setChatMode("error", String(e));
  } finally {
    if (sendBtn) sendBtn.disabled = false;
  }
}

function appendBubble(role, text, opts = {}) {
  const host = document.getElementById("chat-messages");
  const bubble = document.createElement("div");
  bubble.className = "chat-bubble " + role;
  if (opts.thinking) bubble.classList.add("thinking");
  if (opts.mode) bubble.classList.add(opts.mode);

  if (role === "agent" && !opts.thinking) {
    appendTextWithCitations(bubble, text);
  } else {
    bubble.textContent = text;
  }

  host.appendChild(bubble);
  host.scrollTop = host.scrollHeight;
  return bubble;
}

/**
 * Split agent text on [mem_XYZ] citations and render each as a highlighted
 * span. Pure safe-DOM: only createElement + textContent, no raw HTML.
 * Uses String.matchAll for clarity.
 */
function appendTextWithCitations(container, text) {
  let cursor = 0;
  for (const match of text.matchAll(CITE_REGEX)) {
    const start = match.index;
    if (start > cursor) {
      container.appendChild(document.createTextNode(text.slice(cursor, start)));
    }
    const pill = document.createElement("span");
    pill.className = "mem-cite";
    pill.textContent = match[1];
    pill.dataset.memId = match[1];
    pill.addEventListener("click", () => highlightMemory(match[1]));
    pill.title = "Click to highlight the source memory";
    container.appendChild(pill);
    cursor = start + match[0].length;
  }
  if (cursor < text.length) {
    container.appendChild(document.createTextNode(text.slice(cursor)));
  }
}

function renderMemoryPane(memories, mode) {
  const host = document.getElementById("memory-pane-list");
  clearChildren(host);

  if (!memories.length) {
    const empty = document.createElement("div");
    empty.className = "memory-empty";
    empty.textContent = "No memories retrieved for this turn.";
    host.appendChild(empty);
    return;
  }

  for (const m of memories) {
    const card = document.createElement("div");
    card.className = "memory-card";
    card.dataset.memId = m.id || "";

    const idRow = document.createElement("div");
    idRow.className = "memory-card-id";
    idRow.textContent = `[${m.id || "?"}]`;
    card.appendChild(idRow);

    const body = document.createElement("div");
    body.className = "memory-card-body";
    body.textContent = m.content || "";
    card.appendChild(body);

    const s = m.scores;
    if (s && (s.vector != null || s.fts != null || s.hybrid != null)) {
      const scores = document.createElement("div");
      scores.className = "memory-card-scores";
      scores.appendChild(scoreSpan("v", s.vector));
      scores.appendChild(scoreSpan("f", s.fts));
      scores.appendChild(scoreSpan("h", s.hybrid));
      card.appendChild(scores);
    }

    host.appendChild(card);
  }
}

function scoreSpan(label, value) {
  const span = document.createElement("span");
  const strong = document.createElement("strong");
  strong.textContent = label + ":";
  span.appendChild(strong);
  span.appendChild(
    document.createTextNode(" " + (value != null ? Number(value).toFixed(2) : "-"))
  );
  return span;
}

function highlightMemory(memId) {
  document.querySelectorAll(".memory-card").forEach((card) => {
    card.classList.toggle("highlight", card.dataset.memId === memId);
  });
  const target = document.querySelector(`.memory-card[data-mem-id="${memId}"]`);
  if (target) target.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function setChatMode(mode, error) {
  const strip = document.getElementById("chat-mode-strip");
  if (!strip) return;
  strip.hidden = false;
  const modeClass = mode === "retrieval-only" ? "retrieval" : mode;
  strip.className = "chat-mode-strip " + modeClass;
  const text = strip.querySelector(".chat-mode-text");
  if (text) {
    text.textContent = MODE_LABELS[mode] || mode;
    if (error && mode !== "live") text.textContent += ` (${error})`;
  }
}
