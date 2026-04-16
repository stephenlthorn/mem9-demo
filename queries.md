# Booth Queries - Operator Cue Card

Read the **italic** lines aloud. Do not narrate the score numbers - let the bars speak.

## Q1. "What does Sam think about TypeScript?"

- Expected top hit: `#6 - Prefers Python for anything ML-related`
- Expected scores (approx): vector ~0.87, FTS 0.00, hybrid ~0.71
- Narration: *"The word TypeScript never appears in this memory - but mem9 returns Sam's Python preference anyway, because the vector index understands meaning. A keyword-only store would come up empty."*
- What the diagram should show: vector lane glows, FTS lane stays cold, merge glyph weights toward vector.

## Q2. "Who does Sam report to?"

- Expected top hit: `#26 - Reports to Priya Menon`
- Expected scores: vector ~0.91, FTS ~0.88, hybrid ~0.94
- Narration: *"Baseline sanity - both retrieval paths agree. One SQL query, not three APIs."*
- Diagram: all three lanes light up, merge glyph high.

## Q3. "What slowed down the research pipeline recently?"

- Expected top hits: `#15 - latency regression on 2026-04-02`, `#47 - ongoing p99 work`
- Expected scores: vector ~0.83, FTS ~0.77, hybrid ~0.89 (for #15)
- Narration: *"FTS locks onto 'pipeline'. Vector pulls 'latency regression' from the event. Merged, you get both right hits - no keyword-only store does this in one call."*
- Diagram: emphasize merge glyph; spend two beats on the hybrid lane.

## Bonus. "What's Sam drinking?"

- Expected top hit: `#41 - tea, not coffee`
- Use when linger time exists. Keeps the booth charming.

## If the numbers are off

Scores drift by ±0.05 between embedding runs. If any query's **top hit** is wrong:

1. Check the booth dashboard's top-strip tenant ID matches the .env.
2. Re-run `./demo.sh --reset && ./demo.sh`.
3. Fall back: `./demo.sh --offline` plays canned results; the diagram still animates.
4. Last resort: `./demo.sh --replay` plays the MP4.
