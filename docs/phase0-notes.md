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

DELETE only tombstones the tenant row; underlying DB remains. Fleet-timing capture must be disabled by default (SEED_FLEET_TENANTS=0) until upstream is fixed.

Evidence:
- There is **no** `DELETE /v1alpha1/mem9s/{tenantID}` route registered in `server/internal/handler/handler.go`. The only DELETE routes are `DELETE /memories/{id}` (memory-level deletion).
- A search across all of `server/` for `DropDatabase`, `DROP DATABASE`, `deleteDB`, `deleteDatabase` returns **zero results**.
- The only tenant-level DELETE found is in a test helper (`server/internal/repository/tidb/testutil_test.go`): `DELETE FROM tenants` (SQL row deletion only, no DB drop).
- There is no tenant-delete HTTP handler or service method in the codebase.

## 0.5 tenant metadata API

No dedicated metadata endpoint. The "provisioned in Xms" tile uses wall-clock measurement from the seeder (MEM9_PROVISION_MS in .env).

Evidence:
- `server/internal/handler/tenant.go` defines `getTenantInfo` which calls `s.tenant.GetInfo(...)` and returns a `domain.TenantInfo` struct — but **this handler is never registered** in the router (`server/internal/handler/handler.go`). It is dead/unreachable code.
- `domain.TenantInfo` (`server/internal/domain/types.go` line 155) has fields: `tenant_id`, `name`, `status`, `provider`, `memory_count`, `created_at`. There is no `provisioned_at` field.
- No `provisioned_at` column exists in `server/schema.sql` or `server/schema_db9.sql`.
- The `cluster_id` field exists in the tenants schema but is not included in the `TenantInfo` response.
