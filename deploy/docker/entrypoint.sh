#!/usr/bin/env sh
set -eu
python scripts/initialize_database.py
exec python main.py --no-dashboard
