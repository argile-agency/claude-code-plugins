#!/bin/bash
# Analyze dependencies for environmental impact
# Usage: bash analyze-dependencies.sh [project-dir]

PROJECT_DIR="${1:-.}"

echo "=== EcoScore Dependency Analysis ==="
echo ""

# Check for Node.js projects
if [ -f "$PROJECT_DIR/package.json" ]; then
    echo "## Node.js Dependencies"
    echo ""

    # List heavy packages to check for
    HEAVY_PACKAGES="moment lodash underscore axios request jquery bootstrap material-ui antd"

    echo "### Checking for heavy packages..."
    for pkg in $HEAVY_PACKAGES; do
        if grep -q "\"$pkg\"" "$PROJECT_DIR/package.json" 2>/dev/null; then
            echo "- FOUND: $pkg (consider lighter alternative)"
        fi
    done
    echo ""

    # Count total dependencies
    if command -v node &> /dev/null; then
        DEPS=$(node -e "const p=require('$PROJECT_DIR/package.json'); console.log(Object.keys(p.dependencies||{}).length)")
        DEV_DEPS=$(node -e "const p=require('$PROJECT_DIR/package.json'); console.log(Object.keys(p.devDependencies||{}).length)")
        echo "### Dependency counts:"
        echo "- Production dependencies: $DEPS"
        echo "- Dev dependencies: $DEV_DEPS"
        echo "- Total: $((DEPS + DEV_DEPS))"

        if [ "$DEPS" -gt 50 ]; then
            echo "- WARNING: High dependency count may indicate bloat"
        fi
    fi
    echo ""
fi

# Check for Python projects
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    echo "## Python Dependencies"
    echo ""

    HEAVY_PYTHON="pandas numpy tensorflow torch keras scipy"

    echo "### Checking for heavy packages..."
    for pkg in $HEAVY_PYTHON; do
        if grep -qi "^$pkg" "$PROJECT_DIR/requirements.txt" 2>/dev/null; then
            echo "- FOUND: $pkg (large package, verify necessity)"
        fi
    done
    echo ""

    # Count dependencies
    DEP_COUNT=$(grep -c "^[^#]" "$PROJECT_DIR/requirements.txt" 2>/dev/null || echo "0")
    echo "### Dependency count: $DEP_COUNT"
    echo ""
fi

# Check for Go projects
if [ -f "$PROJECT_DIR/go.mod" ]; then
    echo "## Go Dependencies"
    echo ""
    DEP_COUNT=$(grep -c "^\t" "$PROJECT_DIR/go.mod" 2>/dev/null || echo "0")
    echo "### Direct dependencies: $DEP_COUNT"
    echo ""
fi

echo "=== Analysis Complete ==="
