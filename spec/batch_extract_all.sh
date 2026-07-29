#!/bin/bash
# Batch extraction: convert all PDFs in spec/ to individual page markdown files.
# Uses extract_pdf.py for each PDF.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$SCRIPT_DIR/../.venv/bin/activate"
SPEC_DIR="$SCRIPT_DIR"

source "$VENV"

# Clean up old extracted dirs
rm -rf "$SPEC_DIR/issue-09-2025" "$SPEC_DIR/issue-07-2017" \
       "$SPEC_DIR/presentation-ata-s1000d-2022" \
       "$SPEC_DIR/paper-ceur-vol3427" "$SPEC_DIR/paper-ceur-vol3990" \
       "$SPEC_DIR/test-output"

echo "=== Extracting all PDFs to individual page markdown files ==="
echo ""

for pdf in "$SPEC_DIR"/*.pdf; do
    name=$(basename "$pdf" .pdf)
    outdir="$SPEC_DIR/$name"
    echo "--- $name ---"
    python3 "$SCRIPT_DIR/extract_pdf.py" "$pdf" "$outdir"
    echo ""
done

echo "=== ALL DONE ==="
echo ""
echo "Output directories:"
for d in "$SPEC_DIR"/*/; do
    count=$(ls "$d"/*.md 2>/dev/null | wc -l | tr -d ' ')
    if [ "$count" -gt 0 ]; then
        echo "  $(basename "$d")/ — $count pages"
    fi
done
