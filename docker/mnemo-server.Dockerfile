# Build mnemo-server from source.
# Context: project root (.). Source: ./mem9/server/
# The ./mem9/ directory is created by demo.sh on first run.

FROM golang:1.24-alpine AS build
WORKDIR /src

# Copy module files first for dependency caching
COPY mem9/server/go.mod mem9/server/go.sum ./
RUN go mod download

# Copy the rest of the server source
COPY mem9/server .

# Build the server binary
RUN CGO_ENABLED=0 go build -o /mnemo-server ./cmd/mnemo-server

# --- Runtime image ---
FROM alpine:3.20
RUN apk add --no-cache ca-certificates
COPY --from=build /mnemo-server /mnemo-server
EXPOSE 8080
ENTRYPOINT ["/mnemo-server"]
