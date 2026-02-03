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

# Extract transcript_path from hook input using Python
TRANSCRIPT_PATH=$(echo "$HOOK_INPUT" | python3 -c "import json, sys; data = json.load(sys.stdin); print(data.get('transcript_path', ''))" 2>/dev/null)

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
SESSION_ID=$(echo "$HOOK_INPUT" | python3 -c "import json, sys; data = json.load(sys.stdin); print(data.get('session_id', 'unknown'))" 2>/dev/null)

# Get current timestamp in ISO 8601 format
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u +"%Y-%m-%dT%H:%M:%S")

# Initialize or update session state using Python
python3 -c "
import json
import sys
from pathlib import Path

session_file = Path('$SESSION_FILE')
session_id = '$SESSION_ID'
timestamp = '$TIMESTAMP'
input_tokens = int('$INPUT_TOKENS')
output_tokens = int('$OUTPUT_TOKENS')

try:
    if session_file.exists():
        # Update existing session
        with open(session_file, 'r') as f:
            data = json.load(f)
        data['total_input_tokens'] = input_tokens
        data['total_output_tokens'] = output_tokens
        data['api_calls'] = data.get('api_calls', 0) + 1
        data['last_updated'] = timestamp
    else:
        # Initialize new session
        data = {
            'session_id': session_id,
            'session_start': timestamp,
            'total_input_tokens': input_tokens,
            'total_output_tokens': output_tokens,
            'total_energy_wh': 0.0,
            'total_carbon_g': 0.0,
            'api_calls': 1,
            'last_updated': timestamp,
            'tools_used': {},
            'models_used': {}
        }

    with open(session_file, 'w') as f:
        json.dump(data, f, indent=2)
except Exception:
    pass
" 2>/dev/null

# Exit silently (no output)
exit 0
