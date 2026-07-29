#!/usr/bin/env python3
"""Generate refinement worker prompts for all extracted files."""
import os

EXTRACTED_DIR = '/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/extracted'
PROMPTS_DIR = '/Volumes/CORSAIR/Developer/macOS/Application/Manual/ste-code/prompts-refine'

def generate_prompts():
    # Get all w###-p*-*.md files, sorted numerically
    files = sorted(
        [f for f in os.listdir(EXTRACTED_DIR) if f.startswith('w') and f.endswith('.md') and 'sec' not in f],
        key=lambda x: int(x.split('-')[0][1:])
    )
    
    count = 0
    for f in files:
        if f.startswith('w') and '-p' in f:
            # Parse wNNN-pPPPP-PPPP.md
            base = f.replace('.md', '')
            parts = base.split('-p')
            worker_num = parts[0][1:]  # remove 'w' prefix, get '001'
            pages = parts[1]  # '1-4'
            start_page, end_page = pages.split('-')
            
            r_num = worker_num  # rNNN matches wNNN
            r_file = f'r{r_num}-p{pages}.md'
            in_file = f
            
            prompt = f"""TASK: Reformat the extracted spec file into clean, standardized markdown following ALL 9 refinement rules below.

INPUT: ste-code/extracted/{in_file}
OUTPUT: ste-code/refined/{r_file}

RULES (apply in order, do not skip any):

1. PRESERVE ALL CONTENT. Never delete a single word, number, example, or table cell.

2. HEADINGS: Use # for page header, ## for sections, ### for rules, #### for dictionary entries. Remove ### from proper names like ASD-STE100.

3. TABLES: Convert all tables to clean markdown format. Align columns. Add missing headers. Merge cells split by PDF extraction.

4. STE/NON-STE: Format ALL example pairs as:
   > **STE:** [text]
   > **Non-STE:** [text]
   Separate merged examples into individual pairs.

5. CODE: Wrap code snippets in ```language fences.

6. DICTIONARY: Format each entry with - list under #### heading. Separate APPROVED from UNAPPROVED entries clearly.

7. METADATA: Replace repetitive page headers with a single metadata block:
   > **Source:** ASD-STE100 Issue 9, January 2025
   > **Pages:** {start_page}–{end_page} of 434

8. LISTS: Standardize indentation. Use 1. 2. 3. for numbered, - for bullets.

9. SPACING: One blank line between sections. No triple blanks. No trailing spaces.

Output ONLY the refined markdown file. No explanations, no commentary.
"""
            prompt_path = os.path.join(PROMPTS_DIR, f'r{worker_num}-prompt.txt')
            with open(prompt_path, 'w') as pf:
                pf.write(prompt)
            count += 1
    
    print(f'Generated {count} refinement prompts in {PROMPTS_DIR}')

if __name__ == '__main__':
    generate_prompts()
