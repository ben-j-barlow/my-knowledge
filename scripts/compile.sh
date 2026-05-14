#!/usr/bin/env bash
# Print the ingest prompt for a raw source file.
# Usage: ./scripts/compile.sh <topic> <filename>
# Example: ./scripts/compile.sh investing 2026-05-14-buffett-letter.md

set -euo pipefail

TOPIC=${1:-}
FILE=${2:-}

if [[ -z "$TOPIC" || -z "$FILE" ]]; then
  echo "Usage: ./scripts/compile.sh <topic> <filename>"
  echo "Topics: investing, ai-coding, data-engineering"
  exit 1
fi

SOURCE_PATH="raw/$TOPIC/articles/$FILE"

if [[ ! -f "$SOURCE_PATH" ]]; then
  SOURCE_PATH="raw/$TOPIC/papers/$FILE"
fi

if [[ ! -f "$SOURCE_PATH" ]]; then
  echo "File not found in raw/$TOPIC/articles/ or raw/$TOPIC/papers/"
  exit 1
fi

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Paste the following into Claude Code to ingest:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Process $SOURCE_PATH and update the wiki following the ingest workflow in CLAUDE.md.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
