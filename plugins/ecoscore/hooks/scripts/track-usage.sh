#!/bin/bash
# track-usage.sh - PostToolUse hook entry point for token tracking
#
# Reads hook input JSON from stdin, extracts transcript path,
# calls extract-tokens.sh to parse token data, and updates session.json
# with cumulative totals.
#
# This script runs after every tool execution and must be fast and silent.
# Error handling: Always exit 0 to never block workflow.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SESSION_DIR="$PLUGIN_ROOT/.ecoscore"
SESSION_FILE="$SESSION_DIR/session.json"

# Read hook input from stdin
HOOK_INPUT=$(cat)

# Extract transcript_path from hook input
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | jq -r '.transcript_path // empty' 2>/dev/null)

# If no transcript path, exit silently
if [[ -z "$TRANSCRIPT_PATH" ]]; then
    exit 0
fi

# Call extract-tokens.sh to parse transcript
TOKEN_DATA=$("$SCRIPT_DIR/extract-tokens.sh" "$TRANSCRIPT_PATH")

# Parse token extraction results
read INPUT_TOKENS OUTPUT_TOKENS MODEL <<< "$TOKEN_DATA"

# If extraction failed, exit silently
if [[ -z "$INPUT_TOKENS" ]] || [[ -z "$OUTPUT_TOKENS" ]]; then
    exit 0
fi

# Create .ecoscore directory if it doesn't exist
mkdir -p "$SESSION_DIR" 2>/dev/null

# Extract session_id from hook input (fallback to "unknown")
SESSION_ID=$(echo "$HOOK_INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null)

# Get current timestamp in ISO 8601 format
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S")

# Initialize or update session state
if [[ ! -f "$SESSION_FILE" ]]; then
    # Initialize new session
    jq -n \
        --arg sid "$SESSION_ID" \
        --arg start "$TIMESTAMP" \
        --argjson input "$INPUT_TOKENS" \
        --argjson output "$OUTPUT_TOKENS" \
        --arg updated "$TIMESTAMP" \
        '{
            session_id: $sid,
            session_start: $start,
            total_input_tokens: $input,
            total_output_tokens: $output,
            total_energy_wh: 0.0,
            total_carbon_g: 0.0,
            api_calls: 1,
            last_updated: $updated,
            tools_used: {},
            models_used: {}
        }' > "$SESSION_FILE" 2>/dev/null
else
    # Update existing session
    jq \
        --argjson input "$INPUT_TOKENS" \
        --argjson output "$OUTPUT_TOKENS" \
        --arg updated "$TIMESTAMP" \
        '.total_input_tokens = $input |
         .total_output_tokens = $output |
         .api_calls += 1 |
         .last_updated = $updated' \
        "$SESSION_FILE" > "$SESSION_FILE.tmp" 2>/dev/null && \
        mv "$SESSION_FILE.tmp" "$SESSION_FILE" 2>/dev/null
fi

# Exit silently (no output)
exit 0
