#!/usr/bin/env python3
"""
Batch orchestrator: extract all pages from a PDF to individual markdown files.
Usage: python3 extract_pdf.py <pdf_path> <output_dir>

Creates: output_dir/page-0001.md, page-0002.md, ...

NOTE: For issue-09-2025, the combined markdown (issue-09-2025.md) is the
preferred source. Use split_spec.py to split it into spec-page-id files
(e.g., page-HI-1.md, page-1-1-1.md) in the page-dir/ subdirectory.
The old page-NNNN.md sequential naming is deprecated.
"""

import sys
import os
import subprocess
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def extract_all(pdf_path, output_dir):
    """Extract all pages from a PDF."""
    from extract_page import extract_page_to_markdown

    os.makedirs(output_dir, exist_ok=True)

    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    start_time = time.time()

    # Get page count
    import pdfplumber
    pdf = pdfplumber.open(pdf_path)
    total_pages = len(pdf.pages)
    pdf.close()

    print(f"PDF: {pdf_name} — {total_pages} pages")
    print(f"Output: {output_dir}/")

    success = 0
    errors = 0
    total_chars = 0

    for page_num in range(1, total_pages + 1):
        try:
            markdown, raw = extract_page_to_markdown(pdf_path, page_num)

            if markdown is None:
                print(f"  Page {page_num:04d}: SKIP (no content)")
                continue

            out_path = os.path.join(output_dir, f"page-{page_num:04d}.md")
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(markdown)

            success += 1
            total_chars += len(markdown)

            if page_num % 50 == 0:
                elapsed = time.time() - start_time
                rate = page_num / elapsed
                remaining = (total_pages - page_num) / rate
                print(f"  ... {page_num}/{total_pages} pages ({rate:.0f} pgs/s, ~{remaining:.0f}s remaining)")

        except Exception as e:
            errors += 1
            print(f"  Page {page_num:04d}: ERROR — {e}")

    elapsed = time.time() - start_time
    print(f"\nComplete: {success} pages extracted, {errors} errors")
    print(f"Time: {elapsed:.1f}s ({success/elapsed:.1f} pgs/s)")
    print(f"Total output: {total_chars:,} chars (~{total_chars//4:,} tokens)")

    return success, errors


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: extract_pdf.py <pdf_path> <output_dir>")
        sys.exit(1)

    extract_all(sys.argv[1], sys.argv[2])
