"""50-memory Sam Chen persona corpus for mem9 booth demo."""
from __future__ import annotations

MEMORIES: list[dict] = [
    # ── Facts (10) ──────────────────────────────────────────────────────────
    {
        "content": "GitHub handle is sam-c; most public repos are data-pipeline tooling and Rust experiments.",
        "tags": ["fact", "identity"],
    },
    {
        "content": "Staff Engineer at Lumos AI, focused on the ML platform team.",
        "tags": ["fact", "role"],
    },
    {
        "content": "Works on a MacBook M3 Max with 64 GB RAM; rarely uses an external monitor.",
        "tags": ["fact", "hardware"],
    },
    {
        "content": "Uses Claude Code as the primary AI coding assistant; has it aliased to 'cc' in zsh.",
        "tags": ["fact", "tools"],
    },
    {
        "content": "Based in Oakland, CA; commutes to the SF office two days a week.",
        "tags": ["fact", "location"],
    },
    # index 5 — query-target
    {
        "content": "Prefers Python for anything ML-related; dynamically typed languages keep iteration fast.",
        "tags": ["fact", "preference", "query-target"],
    },
    {
        "content": "On the on-call rotation for the ML platform; median pages per week is 1.3.",
        "tags": ["fact", "oncall"],
    },
    {
        "content": "Reaches for Rust when latency or memory safety matters; has shipped two production Rust services.",
        "tags": ["fact", "language", "rust"],
    },
    {
        "content": "Brings 10 years of backend experience; started career writing PHP for a fintech startup.",
        "tags": ["fact", "career"],
    },
    {
        "content": "Joined Lumos AI during Series B; was the 22nd hire.",
        "tags": ["fact", "tenure"],
    },
    # ── Events (15) ─────────────────────────────────────────────────────────
    {
        "content": "Shipped vector search feature to production on 2026-03-02 after a 6-week sprint.",
        "tags": ["event", "shipped"],
    },
    {
        "content": "Attended Lumos AI company offsite at Lake Tahoe in January 2026; led the platform roadmap session.",
        "tags": ["event", "offsite"],
    },
    {
        "content": "Authored the Pinecone-to-TiDB migration RFC in February 2026; RFC is under review.",
        "tags": ["event", "rfc"],
    },
    {
        "content": "Gave an all-hands talk on vector database trade-offs in March 2026; 120 attendees.",
        "tags": ["event", "talk"],
    },
    # index 14 — query-target
    {
        "content": "Debugged a latency regression in the research pipeline on 2026-04-02 - traced to a missing vector index.",
        "tags": ["event", "incident", "query-target"],
    },
    {
        "content": "Ran an interview loop for a senior backend engineer role in April 2026; wrote the take-home exercise.",
        "tags": ["event", "hiring"],
    },
    {
        "content": "Triaged a stale-embeddings sev-2 incident in March 2026; mean time to restore was 47 minutes.",
        "tags": ["event", "incident", "sev2"],
    },
    {
        "content": "Open-sourced ember-cache, an in-process embedding cache library, in January 2026.",
        "tags": ["event", "open-source"],
    },
    {
        "content": "Attended Google Cloud Next 2026 in April 2026; staffed the mem9 demo booth.",
        "tags": ["event", "conference"],
    },
    {
        "content": "Kicked off the memory-as-a-service initiative at Lumos AI in February 2026.",
        "tags": ["event", "initiative"],
    },
    {
        "content": "Led a Python performance audit of the embedding pipeline in March 2026; cut wall-clock time by 18%.",
        "tags": ["event", "performance"],
    },
    {
        "content": "Mentored two new-grad engineers through their first production deployments in Q1 2026.",
        "tags": ["event", "mentorship"],
    },
    {
        "content": "Rewrote the on-call playbook to v2 in February 2026; reduced mean time-to-acknowledge by 30%.",
        "tags": ["event", "operations"],
    },
    {
        "content": "Led the Q4 2025 incident retro; identified 3 systemic gaps in observability coverage.",
        "tags": ["event", "retro"],
    },
    {
        "content": "Built the first working Lantern prototype in November 2025; demo'd it to the CTO the same week.",
        "tags": ["event", "prototype"],
    },
    # index 25 — query-target
    {
        "content": "Reports to Priya Menon, Director of Platform at Lumos AI.",
        "tags": ["relation", "manager", "query-target"],
    },
    # ── Relations (8) ───────────────────────────────────────────────────────
    {
        "content": "Jordan Vega is a peer staff engineer on the data infrastructure team; they pair on RFC reviews.",
        "tags": ["relation", "peer"],
    },
    {
        "content": "Ana Ruiz is the skip-level VP of Engineering; 1:1 with her happens quarterly.",
        "tags": ["relation", "skip-level"],
    },
    {
        "content": "Daniel Park is a cross-team tech lead on the product search team; collaborates on embedding contracts.",
        "tags": ["relation", "cross-team"],
    },
    {
        "content": "Noa Weiss is the recruiter who handled Sam's hire at Lumos AI; still stays in touch.",
        "tags": ["relation", "recruiter"],
    },
    {
        "content": "Miguel Torres is an external collaborator at a partner lab; co-authored an arXiv pre-print together.",
        "tags": ["relation", "external"],
    },
    {
        "content": "Helen Osei is Sam's long-time mentor; was Sam's tech lead at the previous company.",
        "tags": ["relation", "mentor"],
    },
    {
        "content": "Jess Choi is a direct report; joined the team six months ago and is ramping fast.",
        "tags": ["relation", "direct-report"],
    },
    # ── Preferences (10) ────────────────────────────────────────────────────
    {
        "content": "Hates receiving summary responses; prefers full context and raw detail over polished prose.",
        "tags": ["preference", "communication"],
    },
    {
        "content": "Dislikes heavy use of bullet lists in code reviews; prefers inline prose comments.",
        "tags": ["preference", "code-review"],
    },
    {
        "content": "Protects mornings for deep work; calendar blocks 08:00–11:00 Pacific as focus time.",
        "tags": ["preference", "schedule"],
    },
    {
        "content": "Writes all design docs in Markdown; strongly prefers docs-as-code over Confluence.",
        "tags": ["preference", "tooling"],
    },
    {
        "content": "Does not want AI to ask clarifying questions for instructions that are obviously actionable.",
        "tags": ["preference", "ai-behavior"],
    },
    {
        "content": "Keeps pull requests under 400 lines of diff; splits larger changes into stacked PRs.",
        "tags": ["preference", "workflow"],
    },
    {
        "content": "Likes TDD but thinks 100% line coverage is a smell; meaningful tests over coverage theatre.",
        "tags": ["preference", "testing"],
    },
    {
        "content": "Drinks loose-leaf green tea during focus blocks; avoids coffee after 14:00.",
        "tags": ["preference", "personal"],
    },
    {
        "content": "Closes Slack during 3-hour focus blocks; replies to messages in batches at 11:00 and 16:00.",
        "tags": ["preference", "focus"],
    },
    {
        "content": "Reads The Morning Paper newsletter as part of the daily morning routine.",
        "tags": ["preference", "reading"],
    },
    # ── Projects (7) ────────────────────────────────────────────────────────
    {
        "content": "Leading Lantern, an internal AI memory layer serving 800 Lumos employees; targeting 1 ms p50 recall.",
        "tags": ["project", "lantern"],
    },
    {
        "content": "Driving memory-as-a-service: externalising Lantern as a product API for third-party developers.",
        "tags": ["project", "memory-as-a-service"],
    },
    {
        "content": "Evaluating mem9 (mnemo-server) as a potential drop-in backend for Lantern.",
        "tags": ["project", "mem9", "evaluation"],
    },
    # index 46 — query-target
    {
        "content": "Pipeline latency work continues; p99 is 840 ms, target sub-500 ms by 2026-05-15.",
        "tags": ["project", "latency", "query-target"],
    },
    {
        "content": "Authoring the TiDB migration RFC to replace Pinecone as the vector store for the ML platform.",
        "tags": ["project", "tidb", "migration"],
    },
    {
        "content": "Running a hybrid-search benchmark comparing BM25+vector vs pure-vector recall on internal datasets.",
        "tags": ["project", "benchmark", "search"],
    },
    {
        "content": "Prototyping a multi-hop retrieval chain that resolves entity relationships across stored memories.",
        "tags": ["project", "retrieval", "multi-hop"],
    },
]
