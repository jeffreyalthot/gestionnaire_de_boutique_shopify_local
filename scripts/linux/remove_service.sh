#!/usr/bin/env bash
sudo systemctl disable --now shopify-alibaba-orchestrator || true
sudo rm -f /etc/systemd/system/shopify-alibaba-orchestrator.service
sudo systemctl daemon-reload
