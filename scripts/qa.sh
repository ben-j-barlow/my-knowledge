#!/usr/bin/env bash
# Print a Q&A prompt for Claude Code.
# Usage: ./scripts/qa.sh "your question" [topic]
# Example: ./scripts/qa.sh "Compare DCF and comps valuation" investing
# Example: ./scripts/qa.sh "What RAG approaches are in the wiki?"

set -euo pipefail

QUESTION=${1:-}
TOPIC=${2:-}

if [[ -z "$QUESTION" ]]; then
  echo "Usage: ./scripts/qa.sh \"your question\" [topic]"
  echo "Topics (optional): investing, ai-coding, data-engineering"
  exit 1
fi

if [[ -n "$TOPIC" ]]; then
  SCOPE="Scope your search to pages tagged '$TOPIC'."
else
  SCOPE="Search across all topics."
fi

cat <<EOF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Paste the following into Claude Code:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Answer the following question using the wiki. Follow the query workflow in CLAUDE.md. $SCOPE

Question: $QUESTION

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EOF
