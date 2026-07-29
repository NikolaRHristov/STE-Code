
# The char count was wrong due to line reading. Let me recalculate properly.
with open("output/ste_self_reading_manual.txt", "r") as f:
    content = f.read()

total_chars = len(content)
print(f"Manual complete. Total characters: {total_chars:,}")
print(f"Token estimate: ~{total_chars // 4:,}")
print(f"Total lines: {content.count(chr(10)):,}")

# Also verify all files exist
import os
files = [
    "output/ste_distilled_system_prompt.txt",
    "output/ste_extraction_methodology.txt",
    "output/ste_example_turn.txt",
    "output/ste_self_reading_manual.txt",
]
print("\n=== ALL GENERATED FILES ===")
for f in files:
    size = os.path.getsize(f)
    with open(f, "r") as fh:
        chars = len(fh.read())
    print(f"  {f}: {size:,} bytes, {chars:,} chars, ~{chars//4:,} tokens")
