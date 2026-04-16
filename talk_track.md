# 2-Minute Booth Talk Track

Scaled for a mixed exec + technical audience at Google Cloud Next 2026.
Five beats. Stage directions in square brackets. *Italics* = verbatim.

## Beat 1 - Hook (0:00-0:15)

[Hand on laptop, eye contact.]

*"Every agent you saw at this conference forgets you. Here's what fixes that - and why the storage choice decides whether your agent scales to one user or ten million."*

## Beat 2 - Live demo (0:15-0:50)

[Turn laptop toward visitor. Point at counter on screen 1.]

*"Fifty memories just seeded into a brand-new TiDB database - provisioned in under a second. Watch."*

[Click Q1.]

*"TypeScript - notice the word isn't in this memory, but mem9 finds Sam's Python preference anyway. That's semantic retrieval. A keyword store comes up empty here."*

[Click Q3.]

*"Pipeline regression. Hybrid ranking - vector and full-text merge in a single SQL query."*

[Point at the ghosted strip below the diagram.]

*"Without TiDB, that's three services talking to each other through brittle sync glue."*

## Beat 3 - Scale wall (0:50-1:20)

[Tap "Fleet" tab. Click "Spawn 100".]

*"Each dot is a real dedicated database. I measured five of them - under a second each. Manus in production runs ten million of these."*

[Click "Simulate Manus-scale".]

*"Pinterest runs 1.3 million QPS on TiDB. Flipkart consolidated 700 DBs down to one cluster. Dify.AI went from 500,000 containers to one."*

## Beat 4 - Unified engine + ACID (1:20-1:40)

[Swivel to screen 2 - raw memory browser.]

*"Same storage engine, no ETL. And when your agent writes across multiple rows - TiDB gives you distributed ACID out of the box."*

[If technical visitor: swivel to screen 3 - Claude Code + mem9 plugin.]

*"This is Claude Code, same tenant - the agent writes to and reads from the exact same database."*

## Beat 5 - Close (1:40-2:00)

*"Zero dollars idle, 30-day free trial, no credit card. Scan the QR code - you'll have your own in fifteen seconds."*

## Variant stings (3-5s walk-bys)

- **Exec fly-by:** *"We give you persistent agent memory on one database that scales to ten million tenants - no ETL, no credit card."*
- **Tech fly-by:** *"Vector + FTS + metadata in a single SQL query. ACID across rows. Open source, Apache-2.0."*
- **Bored-looking walk-by:** [play animation only] *"That's agent memory in one SQL query - want to see the scale story?"*

## Top 5 objections

1. **"We already use Postgres."** *"Keep it. Point mem9 at Postgres for day one - switch the backend flag when you need hybrid search or the Cloud Zero multi-tenant story."*
2. **"Pinecone is fine for us."** *"For one store and small scale, yes. The moment you add full-text or metadata filters, you're running three systems. We're one."*
3. **"Vertex Vector Search?"** *"Vector-only, and no ACID across memory writes. Mem9's hybrid + transactions matter once the agent mutates state."*
4. **"AlloyDB / pgvector?"** *"Pgvector is great for < 100K rows per tenant. Above that, TiDB's columnar + FTS beats single-node pgvector on both cost and tail latency."*
5. **"We'd self-host an OSS vector DB."** *"That's engineering time you're not spending on the agent. Cloud Zero is a free tier - we're not charging you to start."*

## Cue-card version (no stage directions)

- Hook: every agent forgets you; storage decides one user or ten million.
- Q1: TypeScript/Python - vector wins, FTS misses.
- Q3: pipeline - hybrid merge wins.
- Ghost strip: three services without TiDB.
- Fleet tab: 5 measured, Manus 10M, Pinterest 1.3M QPS, Flipkart 700->1.
- One engine, ACID across rows.
- Scan the QR, 15 seconds to your own.
