#!/usr/bin/env bash
set -euo pipefail

SRC="${1:-src/code.py}"

DEST="$(find /mnt -maxdepth 3 -type d -name CIRCUITPY 2>/dev/null | head -n 1)"

if [ -z "$DEST" ]; then
  echo "CIRCUITPY not found"
  exit 1
fi

cp "$SRC" "$DEST/code.py"

circup --path $DEST install --auto

sync

echo "deployed $SRC -> $DEST/code.py"
