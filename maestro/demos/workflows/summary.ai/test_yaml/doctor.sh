#!/bin/bash

echo "🔍 Checking environment..."

if command -v maestro &> /dev/null; then
    echo "✅ Maestro CLI is installed: $(which maestro)"
else
    echo "❌ Maestro CLI not found! Please install it using:"
    echo "   cd maestro && poetry install"
    exit 1
fi

echo "✅ Environment check passed!"