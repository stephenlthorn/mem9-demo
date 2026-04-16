# Phase 0: Upstream mem9 Verification Notes

## 0.1 HEAD SHA

4d0019f skill: fix install order on onboarding process

## 0.2 docker-compose?

No upstream compose. We will author Dockerfiles for mnemo-server and mem9-dashboard from source in Phase 2.

Dockerfiles found in upstream repo:
- `server/Dockerfile` (mnemo-server Go binary)

## 0.3 EMBED_TEXT model

The canonical model name is `tidbcloud_free/amazon/titan-embed-text-v2`.

Sources:
- `server/schema.sql` line 81 comment: `Set MNEMO_EMBED_AUTO_MODEL=tidbcloud_free/amazon/titan-embed-text-v2 to enable.`
- `server/internal/config/config.go` line 23 example comment: `"tidbcloud_free/amazon/titan-embed-text-v2"`
- `server/internal/service/tenant_test.go` lines 65 and 471: uses `tidbcloud_free/amazon/titan-embed-text-v2` with dims `1024` in test assertions

The db9 schema (`server/schema_db9.sql`) uses the slightly different form `amazon.titan-embed-text-v2:0` (Bedrock ARN format) for db9 backend, but for TiDB Serverless (the booth target) the env value is `tidbcloud_free/amazon/titan-embed-text-v2`.

## 0.4 tenant DELETE semantics

## 0.5 tenant metadata API
