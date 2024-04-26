# syntax=docker/dockerfile:1.7.0
FROM postgres:16.2-alpine

HEALTHCHECK --start-period=30s --start-interval=1s --interval=30s --timeout=5s --retries=5 \
  CMD pg_isready -q -d $POSTGRES_DB -U $POSTGRES_USER || exit 1
