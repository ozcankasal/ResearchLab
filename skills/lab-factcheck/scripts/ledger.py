#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""ledger: map a LaTeX paper's numbered statements and citations to evidence.

Usage:
  ledger.py <main.tex> [--bib references.bib] [--ledger claims.csv] [--audit reference_audit.csv]
            [--with-remarks] [--format json|markdown]

Reads main.tex and every file it pulls in with \\input or \\include. Finds:
  - numbered statements: environments declared with \\newtheorem or \\declaretheorem (definitions,
    examples and remarks only with --with-remarks), with their label, title, file and line;
  - citations: every \\cite-like command, its keys, file and line;
  - overclaim words outside comments and math, for a human to review.
With --bib it reports cited keys missing from the bibliography and entries never cited. With
--ledger (CSV with columns id, kind, evidence, level, checked_on, notes; id is a statement's label)
it reports statements without a row, rows naming no statement, and statements whose level is below
what their environment claims. With --audit (CSV with columns key and status) it lists cited keys whose
status is not verified.

Output: JSON {"ok", "statements", "citations", "findings", "review"} or a Markdown report.
Findings with level "error" make ok false. Exit 0 when ok, 1 otherwise, 2 on a usage error.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # the lab source stays read-only when linked into a project
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bibparse import parse_bib  # noqa: E402

DEFAULT_ENVS = {"theorem", "proposition", "lemma", "corollary", "conjecture", "claim"}
SOFT_ENVS = {"definition", "example", "remark", "observation", "note", "openproblem", "problem", "question"}
PROVED_LEVELS = {"FORMALIZED", "PROVED", "CHECKED", "SUPPORTED"}
OVERCLAIM = [
    r"\bfirst\b", r"\bnovel\b", r"\bunprecedented\b", r"\bbreakthrough\b", r"\boptimal(?:ly)?\b",
    r"\bexponential(?:ly)? (?:speed-?up|faster|advantage)\b", r"\bquantum advantage\b", r"\bquantum supremacy\b",
    r"\balways\b", r"\bnever\b", r"\bguarantee[sd]?\b", r"\bclearly\b", r"\bobviously\b", r"\btrivially\b",
    r"\bproves? that\b", r"\bsolves?\b", r"\bstate[- ]of[- ]the[- ]art\b",
]
CITE_RE = re.compile(r"\\(?:[cC]ite[a-zA-Z]*|[pP]arencite|[tT]extcite|autocite)\*?(?:\[[^\]]*\]){0,2}\{([^}]*)\}")
INPUT_RE = re.compile(r"\\(?:input|include)\{([^}]+)\}")
NEWTHM_RE = re.compile(r"\\newtheorem\*?\{(\w+)\}")
DECLARE_RE = re.compile(r"\\declaretheorem(?:\[([^\]]*)\])?\{(\w+)\}")
BEGIN_RE = re.compile(r"\\begin\{(\w+\*?)\}(?:\[([^\]]*)\])?")
LABEL_RE = re.compile(r"\\label\{([^}]+)\}")


def strip_comments(line: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", line)


def load_sources(main: Path, seen: set[Path] | None = None) -> list[tuple[Path, int, str]]:
    """All lines of main.tex and the files it inputs, in reading order."""
    seen = seen if seen is not None else set()
    main = main.resolve()
    if main in seen or not main.is_file():
        return []
    seen.add(main)
    lines: list[tuple[Path, int, str]] = []
    for number, raw in enumerate(main.read_text(encoding="utf-8").splitlines(), start=1):
        line = strip_comments(raw)
        lines.append((main, number, line))
        for name in INPUT_RE.findall(line):
            child = (main.parent / name)
            if child.suffix != ".tex":
                child = child.with_suffix(".tex")
            lines.extend(load_sources(child, seen))
    return lines


def theorem_envs(lines: list[tuple[Path, int, str]], with_remarks: bool) -> set[str]:
    declared: set[str] = set()
    for _path, _number, line in lines:
        declared.update(NEWTHM_RE.findall(line))
        declared.update(name for _opts, name in DECLARE_RE.findall(line))
    envs = (declared | DEFAULT_ENVS) if declared else set(DEFAULT_ENVS)
    if not with_remarks:
        envs = {e for e in envs if e not in SOFT_ENVS}
    else:
        envs |= SOFT_ENVS & declared
    return envs


def scan(lines: list[tuple[Path, int, str]], envs: set[str], root: Path) -> tuple[list[dict], list[dict], list[dict]]:
    statements: list[dict] = []
    citations: list[dict] = []
    review: list[dict] = []
    current: dict | None = None
    math_depth = 0
    overclaim = re.compile("|".join(OVERCLAIM), re.IGNORECASE)
    for path, number, line in lines:
        where = {"file": str(path.relative_to(root)) if path.is_relative_to(root) else str(path), "line": number}
        for m in BEGIN_RE.finditer(line):
            env = m.group(1).rstrip("*")
            if env in envs and current is None:
                current = {"env": env, "title": m.group(2) or "", "label": None, **where, "text": ""}
            if env in ("equation", "align", "gather", "multline", "eqnarray", "displaymath"):
                math_depth += 1
        if current is not None:
            current["text"] += " " + line.strip()
            if current["label"] is None:
                labels = LABEL_RE.findall(line)
                if labels:
                    current["label"] = labels[0]
            if re.search(r"\\end\{" + re.escape(current["env"]) + r"\*?\}", line):
                current["text"] = re.sub(r"\s+", " ", current["text"]).strip()[:200]
                statements.append(current)
                current = None
        for m in CITE_RE.finditer(line):
            for key in m.group(1).split(","):
                if key.strip():
                    citations.append({"key": key.strip(), **where})
        if re.search(r"\\end\{(equation|align|gather|multline|eqnarray|displaymath)\*?\}", line):
            math_depth = max(0, math_depth - 1)
        if math_depth == 0:
            prose = re.sub(r"\$[^$]*\$|\\\[.*?\\\]|\\\(.*?\\\)", " ", line)
            for m in overclaim.finditer(prose):
                review.append({"word": m.group(0), **where, "context": prose.strip()[:160]})
    return statements, citations, review


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as handle:
        return [{k.strip().lower(): (v or "").strip() for k, v in row.items() if k} for row in csv.DictReader(handle)]


def build(main: Path, bib: Path | None, ledger: Path | None, audit: Path | None, with_remarks: bool) -> dict:
    lines = load_sources(main)
    root = main.resolve().parent
    envs = theorem_envs(lines, with_remarks)
    statements, citations, review = scan(lines, envs, root)
    findings: list[dict] = []
    for s in statements:
        if not s["label"]:
            findings.append({"level": "error", "rule": "unlabelled", "where": f"{s['file']}:{s['line']}", "text": f"{s['env']} without \\label cannot enter the ledger"})
    cited = sorted({c["key"] for c in citations})
    if bib is not None:
        keys = {e["key"] for e in parse_bib(bib.read_text(encoding="utf-8"))}
        for key in cited:
            if key not in keys:
                where = next(f"{c['file']}:{c['line']}" for c in citations if c["key"] == key)
                findings.append({"level": "error", "rule": "missing-bib", "where": where, "text": f"cited key {key} is not in {bib.name}"})
        for key in sorted(keys - set(cited)):
            findings.append({"level": "info", "rule": "uncited", "where": bib.name, "text": f"{key} is never cited"})
    if ledger is not None:
        rows = {r.get("id", ""): r for r in read_csv(ledger)}
        labels = {s["label"] for s in statements if s["label"]}
        for s in statements:
            if not s["label"]:
                continue
            row = rows.get(s["label"])
            if row is None:
                findings.append({"level": "error", "rule": "no-evidence", "where": f"{s['file']}:{s['line']}", "text": f"{s['label']} has no ledger row"})
            elif s["env"] != "conjecture" and row.get("level", "").upper() not in PROVED_LEVELS:
                findings.append({"level": "error", "rule": "level", "where": f"{s['file']}:{s['line']}", "text": f"{s['label']} is stated as a {s['env']} but its evidence level is {row.get('level') or 'empty'}"})
        for rid, row in rows.items():
            if row.get("kind", "statement") == "statement" and rid not in labels:
                findings.append({"level": "warning", "rule": "orphan-row", "where": ledger.name, "text": f"ledger row {rid} names no statement in the paper"})
    if audit is not None:
        statuses = {r.get("key", ""): r.get("status", "") for r in read_csv(audit)}
        for key in cited:
            status = statuses.get(key)
            if status is None:
                findings.append({"level": "error", "rule": "no-audit", "where": audit.name, "text": f"cited key {key} has no audit row"})
            elif not status.lower().startswith("verified"):
                findings.append({"level": "warning", "rule": "audit-status", "where": audit.name, "text": f"{key}: {status}"})
    return {
        "ok": not any(f["level"] == "error" for f in findings),
        "environments": sorted(envs),
        "statements": statements,
        "citations": citations,
        "findings": findings,
        "review": review,
    }


def markdown(result: dict) -> str:
    out = [f"Statements: {len(result['statements'])} · citations: {len(result['citations'])} · findings: {len(result['findings'])} · words to review: {len(result['review'])}", ""]
    out += ["| Statement | Label | Where |", "|---|---|---|"]
    out += [f"| {s['env']} {s['title']} | {s['label'] or '—'} | {s['file']}:{s['line']} |" for s in result["statements"]]
    if result["findings"]:
        out += ["", "## Findings", ""] + [f"- {f['level']} ({f['rule']}) {f['where']}: {f['text']}" for f in result["findings"]]
    if result["review"]:
        out += ["", "## Words to review", ""] + [f"- '{r['word']}' at {r['file']}:{r['line']}: {r['context']}" for r in result["review"]]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Map a LaTeX paper's statements and citations to evidence.")
    parser.add_argument("main", type=Path)
    parser.add_argument("--bib", type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--audit", type=Path)
    parser.add_argument("--with-remarks", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    for path in (args.main, args.bib, args.ledger, args.audit):
        if path is not None and not path.is_file():
            print(f"error: {path} is not a file", file=sys.stderr)
            return 2
    result = build(args.main, args.bib, args.ledger, args.audit, args.with_remarks)
    print(markdown(result) if args.format == "markdown" else json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
