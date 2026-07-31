#!/usr/bin/env python3
with open('ste-code/adapted/a-categories.md', 'r') as f:
    lines = f.readlines()

issues = []

# 1. Check trailing whitespace
for i, line in enumerate(lines, 1):
    if line.rstrip('\n\r') != line.rstrip():
        issues.append(f'Line {i}: trailing whitespace: {repr(line[-10:])}')

# 2. Check headings without space
for i, line in enumerate(lines, 1):
    s = line.strip()
    if s.startswith('#'):
        # Find where hashes end
        j = 0
        while j < len(s) and s[j] == '#':
            j += 1
        if j > 0 and j < len(s) and s[j] != ' ':
            issues.append(f'Line {i}: heading without space after #: "{s[:40]}"')

# 3. Check missing blank lines before headings
for i, line in enumerate(lines, 1):
    s = line.strip()
    if (s.startswith('## ') or s.startswith('### ') or s.startswith('#### ')):
        if i > 1:
            prev = lines[i-2].strip()
            if prev and prev != '---':
                issues.append(f'Line {i}: missing blank line before heading (prev non-empty: "{prev[:40]}")')

# 4. Check pipe tables for column consistency
in_table = False
header_cols = 0
table_start = 0
for i, line in enumerate(lines, 1):
    s = line.strip()
    cols = [c.strip() for c in s.split('|')]
    # Remove empty strings at start/end
    if cols and cols[0] == '':
        cols = cols[1:]
    if cols and cols[-1] == '':
        cols = cols[:-1]
    
    if s.startswith('|'):
        if not in_table:
            in_table = True
            header_cols = len(cols)
            table_start = i
        elif s.startswith('|---') or s.startswith('|:--'):
            # separator row - check it matches header
            if len(cols) != header_cols:
                issues.append(f'Line {i}: separator column count ({len(cols)}) != header ({header_cols})')
        else:
            if len(cols) != header_cols:
                issues.append(f'Line {i}: row column count ({len(cols)}) != header ({header_cols}) at table starting line {table_start}')
    else:
        if in_table:
            in_table = False

if issues:
    for issue in issues:
        print(issue)
else:
    print('No markdown formatting issues found')
