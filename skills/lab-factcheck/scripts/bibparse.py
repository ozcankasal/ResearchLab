#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""bibparse: a small, dependency-free BibTeX reader shared by refcheck.py and ledger.py.

Read, do not run. `parse_bib(text)` returns a list of entries {"type", "key", "fields", "line"} with
field names lower-cased and values stripped of their outer braces or quotes. Handles nested braces,
quoted values, bare numbers and `#` concatenation of simple parts; skips @comment, @preamble and
@string blocks (string macros are not expanded).
"""
from __future__ import annotations

import re

ENTRY_START = re.compile(r"@(\w+)\s*([{(])", re.MULTILINE)


def _matching(text: str, start: int, open_char: str) -> int:
    """Index of the bracket closing the one at `start`, honouring nesting."""
    close_char = "}" if open_char == "{" else ")"
    depth = 0
    i = start
    in_quote = False
    while i < len(text):
        c = text[i]
        if c == '"' and open_char == "(" and text[i - 1] != "\\":
            in_quote = not in_quote
        elif not in_quote:
            if c == "{" or (c == open_char and open_char == "("):
                depth += 1
            elif c == "}" or (c == close_char and close_char == ")"):
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    return -1


def _read_value(body: str, i: int) -> tuple[str, int]:
    """Read one field value starting at body[i]; return (value, index after it)."""
    parts: list[str] = []
    while True:
        while i < len(body) and body[i].isspace():
            i += 1
        if i >= len(body):
            break
        c = body[i]
        if c == "{":
            end = _matching(body, i, "{")
            if end < 0:
                raise ValueError("unbalanced braces in a field value")
            parts.append(body[i + 1:end])
            i = end + 1
        elif c == '"':
            j = i + 1
            depth = 0
            while j < len(body):
                if body[j] == "{":
                    depth += 1
                elif body[j] == "}":
                    depth -= 1
                elif body[j] == '"' and depth == 0:
                    break
                j += 1
            parts.append(body[i + 1:j])
            i = j + 1
        else:
            m = re.match(r"[^,#\s}]+", body[i:])
            token = m.group(0) if m else ""
            parts.append(token)
            i += len(token)
        while i < len(body) and body[i].isspace():
            i += 1
        if i < len(body) and body[i] == "#":
            i += 1
            continue
        break
    return "".join(parts).strip(), i


def parse_bib(text: str) -> list[dict]:
    entries: list[dict] = []
    pos = 0
    while True:
        m = ENTRY_START.search(text, pos)
        if not m:
            break
        kind = m.group(1).lower()
        open_index = m.end() - 1
        end = _matching(text, open_index, m.group(2))
        if end < 0:
            raise ValueError(f"unterminated entry at line {text.count(chr(10), 0, m.start()) + 1}")
        pos = end + 1
        if kind in ("comment", "preamble", "string"):
            continue
        body = text[open_index + 1:end]
        key, _, rest = body.partition(",")
        fields: dict[str, str] = {}
        i = 0
        while i < len(rest):
            fm = re.compile(r"\s*([A-Za-z][\w:.+-]*)\s*=\s*").match(rest, i)
            if not fm:
                i += 1
                continue
            name = fm.group(1).lower()
            value, i = _read_value(rest, fm.end())
            fields[name] = re.sub(r"\s+", " ", value)
            while i < len(rest) and rest[i] in ", \n\t\r":
                i += 1
        entries.append({
            "type": kind,
            "key": key.strip(),
            "fields": fields,
            "line": text.count("\n", 0, m.start()) + 1,
        })
    return entries
