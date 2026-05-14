#!/usr/bin/env bash
# Print a lint/health-check prompt for Claude Code.
# Usage: ./scripts/health_check.sh [topic]
# Example: ./scripts/health_check.sh investing
# Example: ./scripts/health_check.sh       (lints all topics)

set -euo pipefail

TOPIC=${1:-}

if [[ -n "$TOPIC" ]]; then
  SCOPE="Focus on pages tagged '$TOPIC', but also flag any cross-topic issues that involve it."
else
  SCOPE="Check the entire wiki across all topics."
fi

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Paste the following into Claude Code:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run a health check on the wiki following the lint workflow in CLAUDE.md. $SCOPE

Write findings to outputs/ and append to wiki/log.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
