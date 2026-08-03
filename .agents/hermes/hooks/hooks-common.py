#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Optimized pre/post llm/tool hook pipeline.

All hooks share a single cache directory. Non-blocking by design.
"""
import json, os, re, subprocess, sys, time, hashlib
from pathlib import Path

HERMES_HOME = Path(os.path.expanduser("~/.hermes"))
CACHE = HERMES_HOME / "cache" / "hot-context"
CACHE.mkdir(parents=True, exist_ok=True)

STOP = frozenset({
    'the','and','for','you','this','that','with','from','have','not','but',
    'what','let','find','add','need','want','check','run','make','just',
    'will','would','should','could','does','did','also','then','them','than',
    'when','where','which','while','about','into','over','after','your','some',
    'more','each','only','used','been','all','any','are','has','how','its',
    'may','out','put','set','way','see','too','now','new','old','one','get',
    'try','was','were','can','do','go','are','has','her','our','their','like',
    'also','just','really','very','much','many','hermes','agent','session',
    'task','chat','command','request','please','help','show','tell','list',
})

def kw(prompt):
    """Extract keywords from prompt."""
    w = re.findall(r'[a-z]{4,}', prompt.lower())
    return list(dict.fromkeys(w for w in w if w not in STOP))[:10]

def sig(keys, tag=""):
    return hashlib.md5(f"{tag}{'|'.join(sorted(keys[:6]))}".encode()).hexdigest()[:12]

def read(p):
    try:
        d = json.loads(CACHE.joinpath(p).read_text())
        return d if time.time() - d.get("t", 0) < 1800 else None
    except:
        return None

def write(p, v):
    v["t"] = time.time()
    CACHE.joinpath(p).write_text(json.dumps(v))

def spawn_bg(args, inp=None):
    try:
        p = subprocess.Popen(args, stdin=subprocess.PIPE if inp else None,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                        start_new_session=True, cwd=str(HERMES_HOME),
                        env={**os.environ, "HERMES_ACCEPT_HOOKS": "0"})
        if inp and p.stdin:
            p.stdin.write(inp.encode())
            p.stdin.close()
        return True
    except:
        return False

LIBRARIAN_PROMPT = """You are a librarian agent. The user just asked: "{prompt}"

Search {home} for prior work: sessions, skills, memory, reference files.
Return a concise briefing (max 300 words) of relevant patterns, decisions,
and files to reference. Use plain ASCII only. If nothing relevant, say "none"."""

QA_PROMPT = """QA check the assistant response to: "{user_msg}"

Response: {resp}

Return JSON: {{"issues":["..."], "ai_tells":false, "promises_kept":true}}
Check: AI tells (em dashes, curly quotes, "as an AI"), code issues, kept promises.
Max 3 issues. If clean: {"issues":[], "ai_tells":false, "promises_kept":true}"""
