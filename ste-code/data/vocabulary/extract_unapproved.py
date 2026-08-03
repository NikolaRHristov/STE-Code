#!/usr/bin/env python3
"""
Final extraction v3: Quality-focused. Filters phrases, fixes examples.
"""

import re
import json
import os
from pathlib import Path

def _repo_root(start):
    """Walk up from `start` to the checkout root (holds `ste-code/`)."""
    path = Path(start).resolve()
    for parent in path.parents:
        if (parent / "ste-code").is_dir():
            return str(parent)
    return str(path.parents[3])


BASE = _repo_root(__file__)
ADAPTED_DICT = os.path.join(BASE, "ste-code/adapted/a-dictionary.md")
RULES_DIR = os.path.join(BASE, "ste-code/adapted")
OUTPUT_PATH = os.path.join(BASE, "ste-code/data/vocabulary/unapproved-entries.json")

POS_MAP = {
    "v": "verb", "n": "noun", "adj": "adjective", "adv": "adverb",
    "prep": "preposition", "conj": "conjunction", "pron": "pronoun", "art": "article",
}

CANONICAL_SYNONYMS = [
    ("utilize", "use", "v"), ("utilise", "use", "v"), ("leverage", "use", "v"), ("employ", "use", "v"),
    ("initiate", "start", "v"), ("commence", "start", "v"), ("bootstrap", "start", "v"),
    ("terminate", "stop", "v"), ("halt", "stop", "v"), ("kill", "stop", "v"),
    ("display", "show", "v"), ("render", "show", "v"), ("present", "show", "v"),
    ("create", "make", "v"), ("generate", "make", "v"), ("produce", "make", "v"),
    ("retrieve", "get", "v"), ("fetch", "get", "v"), ("obtain", "get", "v"),
    ("configure", "set", "v"), ("assign", "set", "v"), ("establish", "set", "v"),
    ("verify", "check", "v"), ("validate", "check", "v"), ("ensure", "check", "v"),
    ("perform", "do", "v"), ("execute", "do", "v"),
    ("transmit", "send", "v"), ("dispatch", "send", "v"), ("forward", "send", "v"),
    ("delete", "remove", "v"), ("eliminate", "remove", "v"), ("purge", "remove", "v"),
    ("retain", "keep", "v"), ("preserve", "keep", "v"), ("maintain", "keep", "v"),
]

# Fake words / phrases to filter out
FILTER_OUT = {
    # Morphological errors (not vocabulary)
    "applyed", "beginned", "builded", "burnt", "catched", "choosed", "countted",
    "feched", "finded", "freement", "getted", "gived", "keeped", "loosed", "maked",
    "putted", "runned", "sended", "setted", "taked", "teared", "writed",
    "added", "adding", "do", "give", "compiling", "configuring", "containing",
    "crashing", "evicted", "handlers", "invalidating", "is leveraging",
    "is provisioning", "is returning", "responding", "returning",
    "deallocating", "outputting",
    # Multi-word phrases (not single vocabulary items)
    "are increasing", "are resulting", "will be generating", "will be transpiling",
    "will be utilizing", "wasn't responding", "is verifying", "is accepting",
    "is iterating", "is ordering", "is grouping", "is ensuring", "is becoming",
    "is preventing", "is not running", "is throwing", "is rendering",
    "was set", "was seen", "base allocation", "base monad", "base service",
    "abstract away", "allocated timeframe",
    # Duplicate/nonsense corrections
    "cut", "set", "do",
}

def parse_adapted_dictionary(filepath):
    entries = {}
    with open(filepath, 'r') as f:
        content = f.read()

    pattern = r'## ([A-Za-z-]+) \(([a-z]+)\) - UNNAPROVED\n(.*?)(?=\n## |\n---\n|\Z)'

    for match in re.finditer(pattern, content, re.DOTALL):
        word = match.group(1).lower()
        pos = match.group(2)
        body = match.group(3)

        approved = []

        cd_match = re.search(r'\*\*Code-domain:\*\*\s*(.*?)(?:\n>|\n\*Ref|\n$)', body)
        if cd_match:
            alt_text = cd_match.group(1)
            alt_words = re.findall(r'([A-Z][A-Z\s/-]+?)\s*\(([a-z]+)\)', alt_text)
            for w, p in alt_words:
                w_clean = w.strip().lower()
                if w_clean and w_clean not in approved:
                    approved.append(w_clean)
            alt_upper = re.findall(r'([A-Z]{2,}(?:\s+[A-Z]{2,})*)', alt_text)
            for w in alt_upper:
                w_clean = w.strip().lower()
                if w_clean and w_clean not in approved and len(w_clean) > 1:
                    approved.append(w_clean)

        # Examples
        examples = re.findall(
            r'> \*\*STE:\*\*\s*(.*?)\n> \*\*Non-STE:\*\*\s*(.*?)(?=\n>|\n\n|\n\*|\Z)',
            body, re.DOTALL
        )
        if not examples:
            examples = re.findall(
                r'> \*\*STE:\*\*\s*(.*?)\n>\s*\n> \*\*Non-STE:\*\*\s*(.*?)(?=\n>|\n\n|\n\*|\Z)',
                body, re.DOTALL
            )

        non_ste = examples[0][1].strip() if examples else ""
        ste = examples[0][0].strip() if examples else ""

        reason = "Not an approved word in the STE-Code controlled terminology."
        if approved:
            reason += f" Use: {', '.join(a.upper() for a in approved)}."
        elif 'Technical verb (TV)' in body:
            reason += " Permitted as a code-domain technical verb under Rule 1.12."

        key = f"{word}_{pos}"
        entries[key] = {
            "unapproved": word,
            "approved": approved,
            "pos": POS_MAP.get(pos, pos),
            "reason": reason,
            "example_non_ste": non_ste,
            "example_ste": ste,
            "source": "a-dictionary.md"
        }

    return entries


def extract_rule_examples(rules_dir):
    """Extract correction pairs with context from rule files."""
    entries = {}
    rule_files = sorted(Path(rules_dir).glob("a-sec*-rule*.md"))

    for rf in rule_files:
        with open(rf, 'r') as f:
            content = f.read()

        # Split into major sections
        sections = re.split(r'\n(?=### Example \d|## Edge Cases|## Cross-References|\n---\n)', content)

        for section in sections:
            # Find all Non-STE/STE pairs in this section
            pairs = re.findall(
                r'> \*\*Non-STE:\*\*\s*(.*?)\n>\s*\n> \*\*STE:\*\*\s*(.*?)(?=\n>|\n\n|\n\*|\Z)',
                section, re.DOTALL
            )
            if not pairs:
                pairs = re.findall(
                    r'> \*\*Non-STE:\*\*\s*(.*?)\n>\s*\*\*STE:\*\*\s*(.*?)(?=\n>|\n\n|\n\*|\Z)',
                    section, re.DOTALL
                )

            if not pairs:
                continue

            # Find correction annotations in this section
            corrections = re.findall(
                r'["\u201c]([a-z][a-z ]+?)["\u201d]\s*→\s*["\u201c]([a-z][a-z ]+?)["\u201d]',
                section
            )

            if not corrections:
                continue

            # Use the first pair as context for all corrections in this section
            non_ste = pairs[0][1].strip()
            ste = pairs[0][0].strip()

            for unapp, app in corrections:
                unapp = unapp.lower().strip()
                app = app.lower().strip()

                if len(unapp) <= 1:
                    continue
                if unapp in FILTER_OUT:
                    continue
                if unapp == app:
                    continue
                # Skip multi-word phrases (keep only single words)
                if ' ' in unapp:
                    continue

                pos = "v"
                if unapp.endswith("ly"):
                    pos = "adv"
                elif unapp.endswith("tion") or unapp.endswith("ment") or unapp.endswith("ness") or unapp.endswith("ity"):
                    pos = "n"

                reason = f"Not an approved word in the STE-Code controlled terminology. Use '{app}' instead."

                key = f"{unapp}_{pos}"
                if key not in entries:
                    entries[key] = {
                        "unapproved": unapp,
                        "approved": [app],
                        "pos": POS_MAP.get(pos, "verb"),
                        "reason": reason,
                        "example_non_ste": non_ste[:400],
                        "example_ste": ste[:400],
                        "source": f"rule-files/{rf.name}"
                    }
                else:
                    if app not in entries[key]["approved"]:
                        entries[key]["approved"].append(app)
                    # Keep shorter example
                    if len(non_ste) < len(entries[key]["example_non_ste"]):
                        entries[key]["example_non_ste"] = non_ste[:400]
                        entries[key]["example_ste"] = ste[:400]

    return entries


def main():
    print("=== Final Quality Extraction v3 ===\n")

    dict_entries = parse_adapted_dictionary(ADAPTED_DICT)
    print(f"1. Dictionary entries: {len(dict_entries)}")

    rule_entries = extract_rule_examples(RULES_DIR)
    print(f"2. Rule file entries: {len(rule_entries)}")

    # Merge
    merged = {}
    for key, entry in dict_entries.items():
        merged[key] = entry

    for key, entry in rule_entries.items():
        if key not in merged:
            merged[key] = entry
        else:
            if not merged[key]["example_non_ste"] and entry["example_non_ste"]:
                merged[key]["example_non_ste"] = entry["example_non_ste"]
                merged[key]["example_ste"] = entry["example_ste"]
            for a in entry["approved"]:
                if a not in merged[key]["approved"]:
                    merged[key]["approved"].append(a)

    # Add all canonical synonyms with examples
    canon_examples = {
        "utilize": ("Utilize the build tool to generate the artifact.",
                     "Use the build tool to make the binary."),
        "utilise": ("Utilise the build tool to generate the artifact.",
                     "Use the build tool to make the binary."),
        "leverage": ("The application leverages machine learning algorithms.",
                      "The application uses machine learning."),
        "employ": ("Employ a caching layer for performance.",
                    "Use a caching layer for performance."),
        "initiate": ("Initiate the deployment process.",
                      "Start the deployment process."),
        "commence": ("The build will commence after tests pass.",
                      "The build will start after tests pass."),
        "bootstrap": ("Execute the script to bootstrap the application.",
                       "Run the script to start the application."),
        "terminate": ("Terminate the process with SIGTERM.",
                       "Stop the process with SIGTERM."),
        "halt": ("Halt the deployment if errors occur.",
                  "Stop the deployment if errors occur."),
        "kill": ("Kill the process to free the port.",
                  "Stop the process to free the port."),
        "display": ("The command displays the configuration.",
                     "The command shows the configuration."),
        "render": ("The template renders the user data in HTML.",
                    "The template shows the user data in HTML."),
        "present": ("The dashboard presents the metrics in a chart.",
                     "The dashboard shows the metrics in a chart."),
        "create": ("Create a new file in the directory.",
                    "Make a new file in the directory."),
        "generate": ("Generate the API documentation from source comments.",
                      "Make the API documentation from source comments."),
        "produce": ("The factory produces instances of the class.",
                     "The factory makes instances of the class."),
        "retrieve": ("Retrieve the user profile from the database.",
                      "Get the user profile from the database."),
        "fetch": ("Fetch the remote data before rendering the page.",
                   "Get the remote data before rendering the page."),
        "obtain": ("Obtain a lock on the shared resource.",
                    "Get a lock on the shared resource."),
        "configure": ("Configure the server to use port 8080.",
                       "Set the server to use port 8080."),
        "assign": ("Assign the return value to a variable.",
                    "Set the return value to a variable."),
        "establish": ("Establish a connection to the database.",
                       "Set a connection to the database."),
        "verify": ("Verify the input before processing.",
                    "Check the input before processing."),
        "validate": ("Validate the configuration against the schema.",
                      "Check the configuration against the schema."),
        "ensure": ("Ensure the connection is established before sending data.",
                    "Make sure the connection is established before you send data."),
        "perform": ("The function performs the data transformation.",
                     "The function does the data transformation."),
        "execute": ("Execute the command in the terminal.",
                     "Run the command in the terminal."),
        "transmit": ("Transmit the data packet to the remote server.",
                      "Send the data packet to the remote server."),
        "dispatch": ("Dispatch the event to all registered listeners.",
                      "Send the event to all registered listeners."),
        "forward": ("Forward the request to the upstream service.",
                     "Send the request to the upstream service."),
        "delete": ("Delete the temporary files after the build completes.",
                    "Remove the temporary files after the build completes."),
        "eliminate": ("Eliminate duplicate code from the module.",
                       "Remove duplicate code from the module."),
        "purge": ("Purge the cache before deploying the new version.",
                   "Remove all data from the cache before you deploy the new version."),
        "retain": ("Retain the original file permissions after the update.",
                    "Keep the original file permissions after the update."),
        "preserve": ("Preserve the order of elements during sorting.",
                      "Keep the order of elements during sorting."),
        "maintain": ("The service maintains a pool of database connections.",
                      "The service keeps a pool of database connections."),
    }

    for unapp, app, pos in CANONICAL_SYNONYMS:
        key = f"{unapp}_{pos}"
        if key not in merged:
            ex = canon_examples.get(unapp, ("", ""))
            reason = f"Not an approved word in the STE-Code controlled terminology. The canonical synonym table gives '{app}' as the approved alternative (Principle P1)."
            merged[key] = {
                "unapproved": unapp,
                "approved": [app],
                "pos": POS_MAP.get(pos, "verb"),
                "reason": reason,
                "example_non_ste": ex[0],
                "example_ste": ex[1],
                "source": "canonical-synonym-table"
            }
        elif not merged[key]["example_non_ste"]:
            ex = canon_examples.get(unapp, ("", ""))
            if ex[0]:
                merged[key]["example_non_ste"] = ex[0]
                merged[key]["example_ste"] = ex[1]

    # Convert to list, sort, deduplicate by word
    result = sorted(merged.values(), key=lambda x: x["unapproved"])

    seen = {}
    unique = []
    for entry in result:
        uw = entry["unapproved"]
        if uw in seen:
            existing = seen[uw]
            for a in entry["approved"]:
                if a not in existing["approved"]:
                    existing["approved"].append(a)
            if not existing["example_non_ste"] and entry["example_non_ste"]:
                existing["example_non_ste"] = entry["example_non_ste"]
                existing["example_ste"] = entry["example_ste"]
            if entry["source"] not in existing["source"]:
                existing["source"] += " + " + entry["source"]
        else:
            seen[uw] = entry
            unique.append(entry)

    with_ex = sum(1 for e in unique if e["example_non_ste"])
    with_alt = sum(1 for e in unique if e["approved"])
    no_alt = [e for e in unique if not e["approved"]]
    no_ex = [e for e in unique if not e["example_non_ste"]]

    print(f"\n3. Final unique entries: {len(unique)}")
    print(f"   With alternatives: {with_alt}")
    print(f"   With examples: {with_ex}")
    print(f"   Without alternatives: {len(no_alt)}")
    print(f"   Without examples: {len(no_ex)}")

    if no_alt:
        print(f"\n   No alternatives: {', '.join(e['unapproved'] for e in no_alt)}")
    if no_ex:
        print(f"   No examples: {', '.join(e['unapproved'] for e in no_ex)}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(unique, f, indent=2, ensure_ascii=False)

    print(f"\nWrote {len(unique)} entries to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
