#!/usr/bin/env bash
set -euo pipefail

poetry run python bridge_sim/internal/cli.py "$@"
