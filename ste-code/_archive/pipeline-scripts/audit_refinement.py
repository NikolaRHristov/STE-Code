#!/usr/bin/env python3
"""Refinement Quality Auditor — verify all 109 refined files meet standards before cascade."""
import re, os, sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

REFINED = Path("ste-code/refined")

@dataclass
class QualityReport:
    file: str
    has_page_header: bool = False
    has_source_block: bool = False  
    has_approved_tags: int = 0
    has_unapproved_tags: int = 0
    missing_tags: int = 0
    triple_blanks: int = 0
    double_blanks: int = 0
    trailing_whitespace: int = 0
    unnaproved_typo: int = 0
    heading_level_issues: int = 0
    raw_tables: int = 0
    truncated_examples: int = 0
    line_count: int = 0
    char_count: int = 0
    score: float = 0.0
    
    def calculate_score(self):
        score = 100.0
        if not self.has_page_header: score -= 15
        if not self.has_source_block: score -= 10
        if self.missing_tags > 0: score -= min(20, self.missing_tags * 2)
        if self.triple_blanks > 0: score -= 5
        if self.double_blanks > 5: score -= 3
        if self.trailing_whitespace > 0: score -= 5
        if self.unnaproved_typo > 0: score -= 10
        if self.heading_level_issues > 0: score -= 10
        if self.raw_tables > 0: score -= 10
        if self.truncated_examples > 0: score -= 15
        if self.line_count < 20: score -= 20
        self.score = max(0, score)

def audit_file(filepath: Path) -> QualityReport:
    text = filepath.read_text(encoding='utf-8')
    lines = text.split('\n')
    r = QualityReport(file=str(filepath.name))
    r.line_count = len(lines)
    r.char_count = len(text)
    
    # Check page header
    r.has_page_header = bool(re.match(r'^# Page \d+ of 434$', lines[0].strip()))
    
    # Check source block
    for i in range(min(5, len(lines))):
        if 'Source:' in lines[i] and 'ASD-STE100' in lines[i]:
            r.has_source_block = True
            break
    
    # Count tags
    for line in lines:
        s = line.strip()
        if s.endswith('— APPROVED'):
            r.has_approved_tags += 1
        elif s.endswith('— UNAPPROVED'):
            r.has_unapproved_tags += 1
    
    # Find dictionary entries without tags
    for line in lines:
        s = line.strip()
        if re.match(r'^#### \w+ \([^)]+\)$', s) and '—' not in s:
            r.missing_tags += 1
    
    # Count spacing issues
    for i in range(len(lines) - 2):
        if lines[i].strip() == '' and lines[i+1].strip() == '' and lines[i+2].strip() == '':
            r.triple_blanks += 1
    
    blank_count = 0
    for line in lines:
        if line.strip() == '':
            blank_count += 1
            if blank_count > 1:
                r.double_blanks += 1
        else:
            blank_count = 0
    
    # Trailing whitespace
    r.trailing_whitespace = sum(1 for l in lines if l != l.rstrip())
    
    # UNNAPROVED typos
    r.unnaproved_typo = sum(1 for l in lines if 'UNNAPROVED' in l)
    
    # Heading level issues: ## Rule should be ### Rule
    r.heading_level_issues = len(re.findall(r'^## Rule \d+\.\d+', text, re.MULTILINE))
    
    # Raw tables: | Word | Meaning | without proper #### format
    r.raw_tables = len(re.findall(r'^\| \*\*[a-z].*— (?:UN)?APPROVED', text, re.MULTILINE))
    
    # Truncated examples
    r.truncated_examples = len(re.findall(r'> \*\*(?:STE|Non-STE):\*\* .*\.\.\.(?!")', text))
    
    r.calculate_score()
    return r

def audit_all() -> tuple[list[QualityReport], dict]:
    def sort_key(p):
        m = re.search(r'r(\d+)', p.name)
        return int(m.group(1)) if m else 0
    files = sorted(REFINED.glob("r*-p*.md"), key=sort_key)
    reports = [audit_file(f) for f in files]
    
    summary = {
        "total": len(reports),
        "avg_score": sum(r.score for r in reports) / len(reports) if reports else 0,
        "perfect": sum(1 for r in reports if r.score >= 99),
        "good": sum(1 for r in reports if 80 <= r.score < 99),
        "needs_work": sum(1 for r in reports if r.score < 80),
        "total_approved": sum(r.has_approved_tags for r in reports),
        "total_unapproved": sum(r.has_unapproved_tags for r in reports),
        "missing_tags": sum(r.missing_tags for r in reports),
        "unnaproved_typos": sum(r.unnaproved_typo for r in reports),
        "raw_tables": sum(r.raw_tables for r in reports),
        "truncated": sum(r.truncated_examples for r in reports),
        "total_lines": sum(r.line_count for r in reports),
        "total_chars": sum(r.char_count for r in reports),
    }
    
    return reports, summary

if __name__ == '__main__':
    reports, summary = audit_all()
    
    print("=" * 60)
    print("REFINEMENT QUALITY AUDIT")
    print("=" * 60)
    print(f"Files: {summary['total']}")
    print(f"Average score: {summary['avg_score']:.1f}/100")
    print(f"Perfect (99+): {summary['perfect']} | Good (80-98): {summary['good']} | Needs work (<80): {summary['needs_work']}")
    print()
    print(f"APPROVED tags: {summary['total_approved']} | UNAPPROVED: {summary['total_unapproved']} | Missing: {summary['missing_tags']}")
    print(f"UNNAPROVED typos: {summary['unnaproved_typos']}")
    print(f"Raw tables: {summary['raw_tables']}")
    print(f"Truncated examples: {summary['truncated']}")
    print(f"Total: {summary['total_lines']:,} lines, {summary['total_chars']:,} chars")
    print()
    
    if summary['needs_work'] > 0:
        print("FILES NEEDING WORK:")
        for r in reports:
            if r.score < 80:
                issues = []
                if not r.has_page_header: issues.append("no header")
                if not r.has_source_block: issues.append("no source")
                if r.missing_tags: issues.append(f"{r.missing_tags} missing tags")
                if r.unnaproved_typo: issues.append("UNNAPROVED typo")
                if r.raw_tables: issues.append(f"{r.raw_tables} raw tables")
                if r.truncated_examples: issues.append("truncated")
                print(f"  {r.file}: {r.score:.0f}/100 — {', '.join(issues)}")
    
    # Exit code: fail if any file needs work
    sys.exit(0 if summary['needs_work'] == 0 else 1)
