#!/usr/bin/env python3
"""Fetch reference docs into ste-code/final/reference/ — ONE FILE PER REFERENCE.

Deterministic, no LLM. Uses hermes_tools.web_extract (clean markdown / raw text).
Each entry is saved as <slug>.md (or .txt for raw word lists) and indexed in
manifest.json (idempotent: skip existing, append new). Large raw corpora
(>~50k words) are stored as manifest POINTERS (url only) to avoid repo bloat.

Driven by the user's full 52-line reference map (coding terminology / controlled
vocabulary), fed to the finalize agent + LLMs.
"""
import json
import time
import sys
from pathlib import Path

# _STE_REPO_ROOT_BOOTSTRAP: locate the repo by marker, not by counting parent hops.
import sys as _sys
from pathlib import Path as _Path
_R = next(p for p in _Path(__file__).resolve().parents
          if (p / ".git").is_dir() or (p / "Makefile").is_file())
_sys.path.insert(0, str(_R / ".agents" / "tools" / "lib"))
from repo_root import repo_root as _repo_root  # noqa: E402

PROJECT = _repo_root(__file__)
REF_DIR = PROJECT / ".agents" / "reference"
REF_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = REF_DIR / "manifest.json"

# (slug, title, url, kind)  kind: page=web_extract markdown, raw=raw text file
ENTRIES = [
    ("microsoft-writing-style-guide", "Microsoft Writing Style Guide",
     "https://learn.microsoft.com/en-us/style-guide/welcome/", "page"),
    ("microsoft-style-guide-github", "MicrosoftDocs/microsoft-style-guide (GitHub source)",
     "https://github.com/MicrosoftDocs/microsoft-style-guide", "page"),
    ("google-style-guides", "Google Style Guides (per-language conventions)",
     "https://google.github.io/styleguide/", "page"),
    ("kong-apiglossary", "Kong/apiglossary — API terms, acronyms, buzzwords",
     "https://github.com/Kong/apiglossary", "page"),
    ("dwyl-technical-glossary", "dwyl/technical-glossary — collaborative coding vocabulary",
     "https://raw.githubusercontent.com/dwyl/technical-glossary/main/README.md", "raw"),
    ("jvalentino-glossary", "jvalentino/glossary — consolidated software engineering terms",
     "https://github.com/jvalentino/glossary", "page"),
    ("github-official-glossary", "GitHub Official Glossary — Git & GitHub canonical terms",
     "https://docs.github.com/en/get-started/learning-about-github/github-glossary", "page"),
    ("devops-style-guide-glossary", "DevOps Style Guide Glossary — DevOps terms + abbreviations",
     "https://tydukes.github.io/coding-style-guide/glossary/", "page"),
    ("ryanwi-software-terms", "ryanwi software-terms.dic — 200+ tech terms dictionary",
     "https://gist.githubusercontent.com/ryanwi/6135845/raw/software-terms.dic", "raw"),
    ("openste", "OpenSTE.org — open-source Simplified Technical English controlled vocabulary",
     "https://openste.org/", "page"),
    ("en-wl-wordlist", "en-wl/wordlist (SCOWL) — multi-size dialects, POS & frequency",
     "https://github.com/en-wl/wordlist", "page"),
    ("michaelwehar-5000-common", "MichaelWehar 5000-more-common — public-domain word list",
     "https://raw.githubusercontent.com/MichaelWehar/Public-Domain-Word-Lists/master/5000-more-common.txt", "raw"),
    ("dwyl-english-words", "dwyl/english-words — ~466k words (POINTER, too large to embed)",
     "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt", "pointer"),
    ("free-dictionary-api-wordlist", "freeDictionaryAPI english.txt — large general+tech list (POINTER)",
     "https://raw.githubusercontent.com/meetDeveloper/freeDictionaryAPI/master/meta/wordList/english.txt", "pointer"),
    ("vale", "Vale — documentation linter (machine-enforceable rules)",
     "https://github.com/errata-ai/vale", "page"),
    ("vale-microsoft", "errata-ai/Microsoft — Microsoft style Vocab (accept/reject.txt)",
     "https://github.com/errata-ai/Microsoft", "page"),
    ("vale-google", "errata-ai/Google — Google developer docs terms",
     "https://github.com/errata-ai/Google", "page"),
    ("vale-write-good", "errata-ai/write-good — weasel words, passive voice, jargon",
     "https://github.com/errata-ai/write-good", "page"),
    ("topic-word-list", "GitHub topic: word-list (living directory)",
     "https://github.com/topics/word-list", "pointer"),
    ("topic-glossary-terms", "GitHub topic: glossary-terms",
     "https://github.com/topics/glossary-terms", "pointer"),
    ("topic-technical-writing", "GitHub topic: technical-writing",
     "https://github.com/topics/technical-writing", "pointer"),
    ("topic-controlled-vocabulary", "GitHub topic: controlled-vocabulary",
     "https://github.com/topics/controlled-vocabulary", "pointer"),
]


def load_manifest():
    if MANIFEST.exists():
        try:
            return json.load(open(MANIFEST))
        except Exception:
            pass
    return {"entries": []}


def save_manifest(m):
    tmp = str(MANIFEST) + ".tmp"
    json.dump(m, open(tmp, "w"), indent=2)
    Path(tmp).replace(MANIFEST)


def main():
    from hermes_tools import web_extract
    m = load_manifest()
    existing = {e["slug"]: e for e in m["entries"]}
    fetched = 0
    pointer = 0
    for slug, title, url, kind in ENTRIES:
        out = REF_DIR / (slug + (".txt" if kind == "raw" else ".md"))
        if kind == "pointer":
            existing[slug] = {"slug": slug, "title": title, "url": url,
                              "local_path": None, "kind": "pointer",
                              "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            pointer += 1
            print(f"  pointer: {slug}")
            continue
        if out.exists() and out.stat().st_size > 200:
            print(f"  skip (exists): {slug}")
            continue
        print(f"  fetch [{kind}]: {slug}")
        try:
            res = web_extract(urls=[url], char_limit=20000)
            content = ""
            for r in res.get("results", []):
                content = r.get("content", "")
                if content:
                    break
            if not content or len(content) < 50:
                print(f"    EMPTY — pointer only {slug}")
                existing[slug] = {"slug": slug, "title": title, "url": url,
                                  "local_path": None, "kind": "pointer",
                                  "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
                pointer += 1
                continue
            header = f"# {title}\n\n> Source: {url}\n> Fetched by finalize reference fetcher.\n\n---\n\n"
            out.write_text(header + content, encoding="utf-8")
            existing[slug] = {"slug": slug, "title": title, "url": url,
                              "local_path": f"ste-code/final/reference/{out.name}",
                              "kind": kind,
                              "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            fetched += 1
            print(f"    OK ({out.stat().st_size} B)")
        except Exception as e:
            print(f"    FAIL {slug}: {e}")
        time.sleep(0.5)
    m["entries"] = list(existing.values())
    save_manifest(m)
    print(f"\nmanifest: {len(m['entries'])} entries | fetched={fetched} pointers={pointer}")


if __name__ == "__main__":
    main()
