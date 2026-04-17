"""Canned query results for offline mode.

These payloads mirror what the live mnemo-server returns for the three
scripted queries. Loaded by the /canned endpoint for demo.sh --offline.

CANNED_CHAT at the bottom provides pre-scripted agent turns for the
Ask-the-Agent tab when the LLM or mem9 are unreachable.
"""

CANNED: dict[str, dict] = {
    "q1": {
        "label": "What does Sam think about TypeScript?",
        "hits": [
            {
                "id": "mem_006",
                "content": "Prefers Python for anything ML-related; dynamically typed languages keep iteration fast.",
                "tags": ["fact", "preference"],
                "scores": {"vector": 0.87, "fts": 0.00, "hybrid": 0.71},
            },
            {
                "id": "mem_008",
                "content": "Reaches for Rust when latency or memory safety matters; has shipped two production Rust services.",
                "tags": ["fact", "language", "rust"],
                "scores": {"vector": 0.52, "fts": 0.00, "hybrid": 0.41},
            },
            {
                "id": "mem_009",
                "content": "Brings 10 years of backend experience; started career writing PHP for a fintech startup.",
                "tags": ["fact", "career"],
                "scores": {"vector": 0.48, "fts": 0.00, "hybrid": 0.38},
            },
        ],
    },
    "q2": {
        "label": "Who does Sam report to?",
        "hits": [
            {
                "id": "mem_026",
                "content": "Reports to Priya Menon, Director of Platform at Lumos AI.",
                "tags": ["relation", "manager"],
                "scores": {"vector": 0.91, "fts": 0.88, "hybrid": 0.94},
            },
            {
                "id": "mem_028",
                "content": "Ana Ruiz is the skip-level VP of Engineering; 1:1 with her happens quarterly.",
                "tags": ["relation", "skip-level"],
                "scores": {"vector": 0.62, "fts": 0.21, "hybrid": 0.55},
            },
            {
                "id": "mem_027",
                "content": "Jordan Vega is a peer staff engineer on the data infrastructure team; they pair on RFC reviews.",
                "tags": ["relation", "peer"],
                "scores": {"vector": 0.51, "fts": 0.12, "hybrid": 0.44},
            },
        ],
    },
    "q3": {
        "label": "What slowed down the research pipeline recently?",
        "hits": [
            {
                "id": "mem_015",
                "content": "Debugged a latency regression in the research pipeline on 2026-04-02 - traced to a missing vector index.",
                "tags": ["event", "incident"],
                "scores": {"vector": 0.83, "fts": 0.77, "hybrid": 0.89},
            },
            {
                "id": "mem_047",
                "content": "Pipeline latency work continues; p99 is 840 ms, target sub-500 ms by 2026-05-15.",
                "tags": ["project", "latency"],
                "scores": {"vector": 0.79, "fts": 0.81, "hybrid": 0.87},
            },
            {
                "id": "mem_021",
                "content": "Led a Python performance audit of the embedding pipeline in March 2026; cut wall-clock time by 18%.",
                "tags": ["event", "perf"],
                "scores": {"vector": 0.58, "fts": 0.34, "hybrid": 0.52},
            },
        ],
    },
}


# Pre-scripted agent responses for the Ask-the-Agent tab when running
# offline or when the LLM is unreachable. Keys are matched via fuzzy
# substring against the incoming message.
CANNED_CHAT: dict[str, dict] = {
    "What does Sam think about TypeScript?": {
        "answer": (
            "Sam hasn't recorded a direct TypeScript preference, but his "
            "language choices suggest he'd skip it: he reaches for [mem_008] "
            "Rust when latency or memory safety matters, and [mem_006] Python "
            "for anything ML-related because dynamic typing keeps iteration "
            "fast. TypeScript doesn't fit either bucket for the work he does."
        ),
        "memories": CANNED["q1"]["hits"],
    },
    "Who does Sam report to?": {
        "answer": (
            "Sam reports to [mem_026] Priya Menon, Director of Platform at "
            "Lumos AI. His skip-level is [mem_028] Ana Ruiz, VP of Engineering, "
            "who he meets with quarterly. [mem_027] Jordan Vega is his closest "
            "peer on the data infrastructure team."
        ),
        "memories": CANNED["q2"]["hits"],
    },
    "What slowed down the research pipeline recently?": {
        "answer": (
            "On [mem_015] 2026-04-02 Sam debugged a latency regression in the "
            "research pipeline and traced it to a missing vector index. "
            "Follow-up is ongoing — [mem_047] p99 is still 840 ms with a "
            "target of sub-500 ms by 2026-05-15. An earlier [mem_021] Python "
            "perf audit in March already cut wall-clock time by 18%."
        ),
        "memories": CANNED["q3"]["hits"],
    },
}
