#!/usr/bin/env python3
"""pre_llm_call hook: fast memory/context injection from .hermes.

Runs in <30ms. Pure filesystem grep on session names, skills, memory.
Returns {"context": "..."} which Hermes injects into the user message.

Optimizations:
- Only reads session file headers (first 300 bytes), not full JSON
- Skills snapshot is a single file read (no directory walk)
- Cache key from sorted keywords avoids rescanning same prompt
- Silent exit for simple/chatty prompts (no I/O at all)
- No subprocess, no network, no LLM
"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

HERMES = Path(os.path.expanduser("~/.hermes"))
CTX_CACHE = HERMES / "cache" / "ctx" / "last"
_CTX_TTL = 1800  # 30 minutes

_STOP = frozenset(
    {
        "the",
        "and",
        "for",
        "you",
        "this",
        "that",
        "with",
        "from",
        "have",
        "not",
        "but",
        "what",
        "just",
        "will",
        "would",
        "could",
        "been",
        "does",
        "also",
        "then",
        "them",
        "when",
        "where",
        "which",
        "while",
        "about",
        "into",
        "over",
        "after",
        "your",
        "more",
        "each",
        "only",
        "used",
        "all",
        "any",
        "are",
        "has",
        "how",
        "its",
        "may",
        "out",
        "put",
        "set",
        "way",
        "see",
        "too",
        "now",
        "new",
        "old",
        "one",
        "get",
        "try",
        "was",
        "were",
        "can",
        "like",
        "much",
        "many",
        "hermes",
        "agent",
        "session",
        "task",
        "please",
        "help",
        "show",
        "tell",
        "list",
        "here",
        "want",
        "need",
        "find",
        "add",
        "make",
        "check",
        "run",
    }
)

_SKIP = (
    r"^thank",
    r"^ok\b",
    r"^sure",
    r"^yes\b",
    r"^no\b",
    r"^hello",
    r"^hi\b",
    r"^hey",
    r"^/\w+",
)


def main():
    raw = sys.stdin.read(4096)
    if not raw:
        return
    try:
        payload = json.loads(raw)
    except ValueError:
        return

    prompt = payload.get("prompt", "")
    if len(prompt) < 15:
        return
    plow = prompt[:200].lower()

    # Skip chatty/simple prompts immediately
    for pat in _SKIP:
        if re.match(pat, plow):
            return

    # Extract keywords (4+ chars, no stopwords, top 6)
    words = [w for w in re.findall(r"[a-z]{4,}", plow) if w not in _STOP]
    keys = list(dict.fromkeys(words))[:6]
    if len(keys) < 2:
        return

    # Dedup cache check -- skip all I/O if same keywords recently scanned
    cache_key = hashlib.md5("|".join(sorted(keys)).encode()).hexdigest()[:12]
    cache_dir = CTX_CACHE.parent
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_file = CTX_CACHE
    if cache_file.exists():
        try:
            cd = json.loads(cache_file.read_text())
            if cd.get("k") == cache_key and time.time() - cd.get("t", 0) < _CTX_TTL:
                print(json.dumps({"context": cd["c"]}))
                return
        except Exception:
            pass

    parts = []

    # 1. Recent sessions - grep first 400 bytes only
    sd = HERMES / "sessions"
    if sd.is_dir():
        sessions = sorted(sd.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True)[
            :25
        ]
        for sf in sessions:
            if not sf.name.startswith("session_"):
                continue
            try:
                blob = sf.read_bytes()[:400].decode("utf-8", errors="ignore").lower()
                hits = [k for k in keys if k in blob]
                if len(hits) >= 2:
                    # Extract a short title snippet
                    idx = blob.find('"content"')
                    snippet = (
                        blob[idx : idx + 80].replace("\n", " ").strip('"\\ ')
                        if idx >= 0
                        else "..."
                    )
                    parts.append(f"Session ({', '.join(hits[:2])}): {snippet}")
                    if len(parts) >= 3:
                        break
            except Exception:
                continue

    # 2. Skills from snapshot file (single read)
    snap = HERMES / ".skills_prompt_snapshot.json"
    if snap.exists():
        try:
            sd = json.loads(snap.read_text())
            skills = sd if isinstance(sd, list) else sd.get("skills", [])
            for sk in skills[:10]:
                if isinstance(sk, dict):
                    name = sk.get("name", "")
                    desc = sk.get("description", "")
                    blob = f"{name} {desc}".lower()
                    hits = [k for k in keys if k in blob]
                    if hits:
                        parts.append(f"Skill: {name} - {desc[:100]}")
        except Exception:
            pass

    # 3. Memory file
    mem = HERMES / "memory"
    if mem.exists():
        try:
            content = mem.read_text(errors="ignore").lower()
            hits = [k for k in keys if k in content]
            if hits:
                matching = [
                    l.strip()
                    for l in mem.read_text(errors="ignore").split("\n")
                    if any(k in l.lower() for k in hits) and l.strip()
                ][:3]
                if matching:
                    parts.append("Memory:\n" + "\n".join(f"  {l}" for l in matching))
        except Exception:
            pass

    # 4. Previous QA check (fast AI-tell feedback for last response)
    qa = HERMES / "cache" / "self-qa" / "last-qa-check.json"
    if qa.exists():
        try:
            qd = json.loads(qa.read_text())
            if time.time() - qd.get("timestamp", 0) < 300:
                issues = qd.get("issues", [])
                if issues:
                    parts.append(
                        "AI-tell check (last response):\n"
                        + "\n".join(f"  - {i}" for i in issues[:3])
                    )
        except Exception:
            pass

    if not parts:
        return

    ctx = "PRIOR CONTEXT (auto-injected):\n" + "\n".join(parts)

    # Cache result for next turn with same keywords
    try:
        json.dump({"k": cache_key, "c": ctx, "t": time.time()}, cache_file.open("w"))
    except Exception:
        pass

    print(json.dumps({"context": ctx}))


if __name__ == "__main__":
    main()
