#!/usr/bin/env python3
"""
Level 5 MAX System Prompt — robust extraction from all 51 deepened rule files.
Walks each file line-by-line to correctly extract Non-STE/STE pairs regardless of format.
"""

import os, re, glob

ADAPTED = "/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/adapted"
OUTPUT  = "/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/artifacts/ste-code-level5-max.txt"

def read(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def sentences(text, n=3):
    s = re.split(r'(?<=[.!?])\s+', text.strip())
    return ' '.join(s[:n])

def extract_pairs_line_by_line(text):
    """
    Walk through the file line by line. Collect all contiguous Non-STE/STE blocks.
    A block starts with a line matching > **Non-STE:** (possibly with inline text)
    and ends when we see the next > **Non-STE:** or a ### marker.
    """
    pairs = []
    lines = text.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect start of a Non-STE block
        m = re.match(r'> \*\*Non-STE:\*\*\s*(.*)', line)
        if m:
            non_ste_parts = []
            ste_parts = []
            meta_parts = []
            state = 'nonste'
            
            # If there's inline text after the marker, capture it
            inline = m.group(1).strip()
            if inline:
                non_ste_parts.append(inline)
            
            i += 1
            while i < len(lines):
                ls = lines[i].strip()
                
                # Stop conditions: next Non-STE marker or a section header
                if re.match(r'> \*\*Non-STE:\*\*', ls):
                    break
                if re.match(r'^#{1,4}\s', ls):
                    break
                
                # STE marker
                if re.match(r'> \*\*STE:\*\*', ls):
                    state = 'ste'
                    content = re.sub(r'^>\s*\*\*STE:\*\*\s*', '', ls).strip()
                    if content:
                        ste_parts.append(content)
                    i += 1
                    continue
                
                if state == 'nonste':
                    if ls.startswith('>'):
                        content = re.sub(r'^>\s?', '', ls).strip()
                        if content and not content.startswith('**'):
                            non_ste_parts.append(content)
                    elif ls and not ls.startswith('#'):
                        non_ste_parts.append(ls)
                elif state == 'ste':
                    if ls.startswith('>'):
                        content = re.sub(r'^>\s?', '', ls).strip()
                        if content and not re.match(r'\*\*(?:Non-STE|STE):', content):
                            ste_parts.append(content)
                        elif content:
                            state = 'meta'
                            meta_parts.append(content)
                    elif ls and not ls.startswith('#'):
                        state = 'meta'
                        if not re.match(r'\*\*(?:Non-STE|STE):', ls):
                            meta_parts.append(ls)
                elif state == 'meta':
                    if ls.startswith('>'):
                        content = re.sub(r'^>\s?', '', ls).strip()
                        if content:
                            meta_parts.append(content)
                    elif ls:
                        meta_parts.append(ls)
                
                i += 1
            
            ns = ' '.join(non_ste_parts).strip()
            st = ' '.join(ste_parts).strip()
            meta = ' '.join(meta_parts).strip()
            
            # Filter out section headers from meta
            meta = re.sub(r'^#{1,4}\s+.+$', '', meta, flags=re.MULTILINE).strip()
            
            if ns or st:
                pairs.append({'non_ste': ns, 'ste': st, 'meta': meta})
        else:
            i += 1
    
    return pairs

def extract(text):
    d = {}

    # Title
    m = re.search(r'^# (.+)$', text, re.MULTILINE)
    d['title'] = m.group(1).strip() if m else ''

    # Summary: first sentences from Original Rule
    m = re.search(r'## Original Rule\n\n(.*?)(?=\n## STE-Code)', text, re.DOTALL)
    if m:
        d['summary'] = sentences(m.group(1), 3)
    else:
        d['summary'] = ''

    # Adaptation: STE-Code Adaptation section
    m = re.search(r'## STE-Code Adaptation\n\n(.*?)(?=\n## (?:Code-Domain|Grammar|Cross-Ref|Paradigm|Extended|Edge))', text, re.DOTALL)
    if m:
        adapt = m.group(1).strip()
        adapt = re.sub(r'\n### Examples?\n.*?(?=\n(?:##|---|\Z))', '', adapt, flags=re.DOTALL)
        d['adaptation'] = adapt
    else:
        d['adaptation'] = ''

    # All Non-STE/STE pairs
    all_pairs = extract_pairs_line_by_line(text)

    # Position-based filtering: keep pairs after Extended Examples or Code-Domain Explanation
    ext_pos = text.find('Extended Examples')
    code_pos = text.find('Code-Domain Explanation')
    if ext_pos >= 0 and code_pos >= 0:
        start_pos = min(ext_pos, code_pos)
    elif ext_pos >= 0:
        start_pos = ext_pos
    elif code_pos >= 0:
        start_pos = code_pos
    else:
        start_pos = 0

    filtered = []
    for pair in all_pairs:
        # Find position in text
        search = pair['non_ste'][:40] if pair['non_ste'] else pair['ste'][:40]
        pos = text.find(search) if search else -1
        if pos >= start_pos:
            filtered.append(pair)
    
    if not filtered and all_pairs:
        filtered = all_pairs

    d['pairs'] = filtered[:3]

    # Principles
    found = set()
    for m in re.finditer(r'P(\d+)', text):
        num = int(m.group(1))
        if 1 <= num <= 14:
            found.add(f"P{num}")
    d['principles'] = sorted(found, key=lambda x: int(x[1:]))

    return d

def build_output(rules):
    out = []
    out.append("# STE-Code Level 5 MAX — System Prompt")
    out.append("")
    out.append("You are STE-Code, a documentation system that applies ASD-STE100 Simplified Technical")
    out.append("English principles to code documentation. You produce clear, unambiguous,")
    out.append("internationally readable documentation for software projects.")
    out.append("")
    out.append("## Core Principles Applied (P1-P14)")
    out.append("")
    for p, desc in [
        ("P1",  "Use approved words from the controlled terminology"),
        ("P2",  "Use approved words only as the specified part of speech"),
        ("P3",  "Use approved words only with their approved meanings"),
        ("P4",  "Use only approved verb and adjective forms"),
        ("P5",  "Use code-domain technical nouns from the 22 categories"),
        ("P6",  "Use non-approved words only when they are technical nouns"),
        ("P7",  "Do not use technical nouns as verbs"),
        ("P8",  "Use standard, well-known technical nouns"),
        ("P9",  "Prefer short, clear technical nouns"),
        ("P10", "No slang, jargon, or regional terms"),
        ("P11", "One term per concept"),
        ("P12", "Technical verbs are allowed"),
        ("P13", "Do not use technical verbs as nouns"),
        ("P14", "Use American English spelling"),
    ]:
        out.append(f"{p}: {desc}")
    out.append("")
    out.append("---")
    out.append("")

    total_examples = 0

    for rule in rules:
        title = rule.get('title', 'Rule')
        out.append(f"## {title}")
        out.append("")

        if rule.get('summary'):
            out.append(rule['summary'])
            out.append("")

        if rule.get('adaptation'):
            out.append(rule['adaptation'])
            out.append("")

        if rule.get('pairs'):
            for pair in rule['pairs']:
                ns = pair['non_ste'].replace('\n', ' ').strip()
                st = pair['ste'].replace('\n', ' ').strip()
                meta = pair.get('meta', '').replace('\n', ' ').strip()
                # Clean meta of markdown headers and example sub-headers
                meta = re.sub(r'#{1,4}\s+[^#]+', '', meta).strip()
                meta = re.sub(r'\*\*Example\s+\d+[^*]*\*\*', '', meta).strip()
                meta = re.sub(r'\s{2,}', ' ', meta).strip()

                if not ns and not st:
                    continue
                total_examples += 1

                out.append(f"> **Non-STE:** {ns}")
                out.append(f">")
                out.append(f"> **STE:** {st}")
                if meta:
                    out.append(f">")
                    out.append(f"> {meta}")
                out.append("")

        if rule.get('principles'):
            out.append(f"Key principles: {', '.join(rule['principles'])}")
            out.append("")

        out.append("---")
        out.append("")

    # ---- SYNONYM TABLE ----
    out.append("## Approved Synonym Table (Key Entries)")
    out.append("")
    out.append("| Non-STE Word | STE-Code Approved Alternative |")
    out.append("|-------------|------------------------------|")
    synonyms = [
        ("execute", "run"),
        ("utilize / leverage", "use"),
        ("generate", "make"),
        ("configure", "set"),
        ("retrieve / fetch", "get"),
        ("transmit", "send"),
        ("delete / purge", "remove"),
        ("validate / verify", "check"),
        ("perform", "do"),
        ("construct / instantiate", "make"),
        ("persist", "keep"),
        ("terminate", "stop"),
        ("commence / initiate", "start"),
        ("obtain / acquire", "get"),
        ("demonstrate", "show"),
        ("necessitate", "need"),
        ("require", "must (procedural)"),
        ("provide / furnish", "give"),
        ("modify / alter", "change"),
        ("implement", "add / make"),
        ("optimize / enhance", "make faster"),
        ("ensure", "make sure"),
        ("indicate", "show"),
        ("possess", "have"),
        ("reside", "stay"),
        ("sufficient", "enough"),
        ("additional", "more / new"),
        ("numerous / multiple", "many"),
        ("invalid / malformed", "not correct"),
        ("unable to", "cannot"),
        ("prior to", "before"),
        ("subsequent to", "after"),
        ("in order to", "to"),
        ("as a result of", "because of"),
        ("in the event that", "if"),
        ("with regard to", "about"),
        ("allocate", "make / assign"),
        ("deallocate", "free (technical verb)"),
        ("orchestrate", "control / manage (technical verb)"),
        ("provision", "make / set up"),
        ("bootstrap", "start"),
        ("abstract away", "hide"),
        ("reject (promise)", "give an error"),
        ("resolve (promise)", "complete"),
        ("deduplicate", "remove duplicates"),
    ]
    for ns, ste in synonyms:
        out.append(f"| {ns} | {ste} |")
    out.append("")

    # ---- ATTRIBUTION ----
    out.append("---")
    out.append("")
    out.append("## Attribution")
    out.append("")
    out.append("This document adapts rules from ASD-STE100 Issue 9, the international specification")
    out.append("for Simplified Technical English. ASD-STE100 is copyright by the Aerospace and Defence")
    out.append("Industries Association of Europe (ASD). STE-Code applies STE principles to the domain")
    out.append("of software code documentation.")
    out.append("")

    # ---- STATS ----
    out.append("## Statistics")
    out.append(f"Total rules: {len(rules)}")
    out.append(f"Total Non-STE/STE example pairs: {total_examples}")
    out.append("")

    return '\n'.join(out)

def main():
    files = sorted(glob.glob(os.path.join(ADAPTED, "a-sec*-rule*.md")))
    print(f"Found {len(files)} rule files")

    rules = []
    for f in files:
        text = read(f)
        info = extract(text)
        info['filename'] = os.path.basename(f)
        rules.append(info)

    output = build_output(rules)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as fh:
        fh.write(output)

    total_examples = sum(len(r.get('pairs', [])) for r in rules)
    words = len(output.split())
    est_tokens = int(words * 1.3)
    zero_ex = [r['filename'] for r in rules if not r.get('pairs')]

    print(f"Done!")
    print(f"Total rules:          {len(rules)}")
    print(f"Total example pairs:  {total_examples}")
    print(f"Estimated tokens:     {est_tokens}")
    print(f"Characters:           {len(output)}")
    if zero_ex:
        print(f"Files with 0 pairs:   {zero_ex}")
    print(f"Output: {OUTPUT}")

if __name__ == '__main__':
    main()
