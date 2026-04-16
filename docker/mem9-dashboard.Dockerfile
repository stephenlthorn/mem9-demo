# mem9-dashboard — Vite + React SPA
# Build context: project root (.)
# Source: ./mem9/dashboard/app/ (cloned upstream at demo.sh run time)
#
# The upstream dashboard is a Vite SPA served as static files.
# We build with pnpm and serve via `vite preview` on port 4173.
# docker-compose.yml maps host:3000 → container:4173.

FROM node:20-alpine AS build
WORKDIR /app

# Copy lockfile and manifest first for layer-cache efficiency
COPY mem9/dashboard/app/package.json mem9/dashboard/app/pnpm-lock.yaml ./

# Install pnpm via corepack, then install deps
RUN corepack enable && corepack prepare pnpm@latest --activate \
    && pnpm install --frozen-lockfile

# Copy the rest of the app source
COPY mem9/dashboard/app .

# Build the static bundle
RUN pnpm build

# ---- runtime stage ----
FROM node:20-alpine
WORKDIR /app

# Install pnpm in the runtime image too (needed for `pnpm preview`)
RUN corepack enable && corepack prepare pnpm@latest --activate

COPY --from=build /app .

EXPOSE 4173

# vite preview serves the dist/ folder on 0.0.0.0:4173
CMD ["pnpm", "preview", "--host", "0.0.0.0", "--port", "4173"]
