#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
sed "s|__PROJECT_ROOT__|$ROOT|g" "$ROOT/deploy/systemd/shopify-alibaba-orchestrator.service" | sudo tee /etc/systemd/system/shopify-alibaba-orchestrator.service >/dev/null
sudo systemctl daemon-reload
sudo systemctl enable --now shopify-alibaba-orchestrator
