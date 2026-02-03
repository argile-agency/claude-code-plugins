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

# Parse transcript with Python (more universally available than jq on Windows)
RESULT=$(python3 -c '
import json
import sys

transcript_path = sys.argv[1]
input_tokens = 0
output_tokens = 0
model = "unknown"

try:
    with open(transcript_path, "r") as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if data.get("type") == "message" and data.get("usage"):
                    usage = data["usage"]
                    input_tokens += usage.get("input_tokens", 0)
                    output_tokens += usage.get("output_tokens", 0)
                    if "model" in data:
                        model = data["model"]
            except json.JSONDecodeError:
                continue

    print(f"{input_tokens} {output_tokens} {model}")
except Exception:
    print("0 0 unknown")
' "$TRANSCRIPT_PATH" 2>/dev/null)

# Output result or fallback to zeros
if [[ -z "$RESULT" ]]; then
    echo "0 0 unknown"
else
    echo "$RESULT"
fi
