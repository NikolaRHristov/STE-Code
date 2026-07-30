import sys

with open('.agents/agent/agent-2-refiner.md', 'r') as f:
    lines = f.readlines()

issues = []

# 1. Check for missing blank lines before headings
for i, line in enumerate(lines):
    stripped = line.strip()
    if (stripped.startswith('##') or stripped.startswith('###') or stripped.startswith('####')):
        if i > 0 and lines[i-1].strip() != '':
            issues.append(f'Line {i+1}: No blank line before heading: [{stripped[:60]}]')

# 2. Check for trailing whitespace
for i, line in enumerate(lines):
    if line.rstrip('\n\r') != line.rstrip():
        issues.append(f'Line {i+1}: Trailing whitespace')

# 3. Check heading space after #
for i, line in enumerate(lines):
    if line.startswith('#'):
        stripped = line.lstrip()
        # Check that after all # chars, there's a space
        j = 0
        while j < len(stripped) and stripped[j] == '#':
            j += 1
        if j < len(stripped) and stripped[j] != ' ':
            issues.append(f'Line {i+1}: No space after #: [{stripped[:60]}]')

# 4. Check pipe tables for consistent column counts
in_table = False
header_cols = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith('|') and stripped.endswith('|'):
        if not in_table:
            in_table = True
            header_cols = stripped.count('|') - 1
        else:
            cols = stripped.count('|') - 1
            if '|---' not in stripped.replace(' ', '') and cols != header_cols:
                issues.append(f'Line {i+1}: Table column mismatch: expected {header_cols}, got {cols}')
    else:
        if in_table:
            in_table = False

if issues:
    for iss in issues:
        print(iss)
else:
    print('No issues found.')
