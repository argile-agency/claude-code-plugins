#!/bin/bash
# extract-tokens.sh - Parse Claude Code transcript to extract token usage
#
# Usage: extract-tokens.sh <transcript_path>
# Output: "INPUT_TOKENS OUTPUT_TOKENS MODEL" (space-separated)
#
# Parsing logic:
# 1. Read JSONL transcript file (one JSON object per line)
# 2. Filter for messages with .type == "message" and .usage != null
# 3. Extract input_tokens, output_tokens from .usage field
# 4. Sum tokens across all API responses in the session
# 5. Extract model family from .model field (opus/sonnet/haiku)
# 6. Handle missing/corrupt transcript gracefully: output "0 0 unknown"

TRANSCRIPT_PATH="$1"

# Check if transcript exists and is readable
if [[ ! -f "$TRANSCRIPT_PATH" ]] || [[ ! -r "$TRANSCRIPT_PATH" ]]; then
    echo "0 0 unknown"
    exit 0
fi

# Parse transcript with jq
# - Filter for message events with usage data
# - Extract input_tokens, output_tokens, and model
# - Sum tokens and get last model used
RESULT=$(jq -r --slurp '
  map(select(.type == "message" and .usage != null)) |
  if length == 0 then
    "0 0 unknown"
  else
    {
      input_tokens: (map(.usage.input_tokens // 0) | add),
      output_tokens: (map(.usage.output_tokens // 0) | add),
      model: (map(.model // "unknown") | last)
    } |
    "\(.input_tokens) \(.output_tokens) \(.model)"
  end
' "$TRANSCRIPT_PATH" 2>/dev/null)

# If jq fails or returns empty, output zeros
if [[ -z "$RESULT" ]]; then
    echo "0 0 unknown"
else
    echo "$RESULT"
fi
