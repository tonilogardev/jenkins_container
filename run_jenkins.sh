#!/bin/bash
# Script to start Jenkins container

set -e

# Clean up Docker
docker system prune -f --volumes 2>/dev/null || true

# Build and start (logs visible, Ctrl+C stops container)
docker compose build
docker compose up
