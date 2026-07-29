#!/usr/bin/env python3
"""Rails Compliance Checker — Scan all output files against the 8 rails."""

import os, re, sys

ROOT = '/Volumes/CORSAIR/Developer/macOS/Application/Manual'
STE_CODE = os.path.join(ROOT, 'ste-code')

RAILS = {
    'R1-Stage-Isolation': {
        'check': lambda: True,  # Manual check
        'desc': 'Files must be in correct stage directory'
    },
    'R2-Naming': {
        'pattern': r'^(w|r)\d{3}-p\d+-\d+\.md$',
        'desc': 'Files must follow [w|r]NNN-pPPPP-PPPP.md pattern'
    },
    'R5-Headings': {
        'func': lambda content: len(re.findall(r'### [^\n]+\n[^\n#\s|`>-]', content)),
        'desc': 'No glued headings (blank line required after ###)'
    },
    'R5-Blanks': {
        'func': lambda content: 1 if '\n\n\n\n' in content else 0,
        'desc': 'No triple+ blank lines'
    },
    'R5-Boilerplate': {
        'func': lambda content: max(0, content.count('ASD-STE100 Simplified Technical English') - 4),
        'desc': 'Boilerplate header repeated too many times'
    },
    'R5-STE-Format': {
        'func': lambda content: 1 if 'STE:' in content and '**STE:**' not in content and '> **STE:**' not in content else 0,
        'desc': 'STE examples not in proper format'
    },
    'R5-Page-Header': {
        'func': lambda content: 0 if re.match(r'^# Page \d+ of 434', content.split('\n')[0]) else 1,
        'desc': 'Missing # Page N of M header'
    },
    'R4-Fabrication': {
        'func': lambda content: sum(1 for t in ['This page describes', 'The key point', 'In summary', 'React', 'Docker', 'npm', 'Kubernetes'] if t in content),
        'desc': 'Fabrication signals detected'
    },
    'R6-Facts': {
        'func': lambda content: 1 if '22 categor' in content and 'not 22' not in content.lower() else 0,
        'desc': 'Claims 22 categories (should be 19)'
    },
}

def check_all():
    issues = []
    stats = {'files': 0, 'passed': 0, 'issues': 0}
    
    for stage_dir in ['extracted', 'refined']:
        d = os.path.join(STE_CODE, stage_dir)
        if not os.path.isdir(d):
            continue
        
        for fname in sorted(os.listdir(d)):
            if not fname.endswith('.md'):
                continue
            fpath = os.path.join(d, fname)
            stats['files'] += 1
            file_ok = True
            
            # R2: Naming
            if not re.match(RAILS['R2-Naming']['pattern'], fname):
                issues.append(f'🔴 {stage_dir}/{fname}: R2 — bad naming')
                file_ok = False
            
            try:
                with open(fpath) as f:
                    content = f.read()
            except:
                continue
            
            # Content checks
            for rail_name, rail in RAILS.items():
                if 'func' not in rail:
                    continue
                count = rail['func'](content)
                if count > 0:
                    issues.append(f'🟡 {stage_dir}/{fname}: {rail_name} — {rail["desc"]} ({count}x)')
                    stats['issues'] += 1
                    file_ok = False
            
            if file_ok:
                stats['passed'] += 1
    
    # Print results
    print(f"Files checked: {stats['files']}")
    print(f"Clean: {stats['passed']}")
    print(f"Issues: {stats['issues']}")
    print()
    
    if issues:
        print("=== Issues Found ===")
        for issue in issues:
            print(f"  {issue}")
        print(f"\n⚠️  {len(issues)} issues need attention.")
    else:
        print("✅ All files pass rails compliance.")
    
    return len(issues)

if __name__ == '__main__':
    sys.exit(check_all())
