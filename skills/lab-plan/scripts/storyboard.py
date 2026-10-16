#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""storyboard: check a lab plan's story files and print the board.

Usage:
  storyboard.py <plan-folder> [--brief <brief.md>] [--format json|markdown]

<plan-folder> holds `stories/*.md` (or is the stories folder itself). Each story file starts with a
front-matter block between `---` lines of `key: value` pairs; lists are written `[A, B]`; text after
`#` is a comment. Required keys: id, type, title, claim, owner, depends_on, status, size.

Checks: required keys; the id equals the file name and starts with its type; type, status and size
are known; dependencies exist and form no cycle; ids are unique; a story has an `## Acceptance
criteria` section with at least one bullet; with --brief, each story's claim (or `-` for none) is a
claim ID in the brief.

Output: one JSON object (default) with ok, counts, ready, blocked, order, findings and a Mermaid
graph; or a Markdown board with --format markdown. Findings with level "error" make ok false.
Exit 0 when ok, 1 when there are errors, 2 on a usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TYPES = ("THM", "LEM", "EXP", "STUDY", "DATA", "CODE", "LIT", "FORMAL", "WRITE", "DECIDE")
STATUSES = ("todo", "doing", "review", "done", "dropped")
SIZES = ("S", "M", "L")
REQUIRED = ("id", "type", "title", "claim", "owner", "depends_on", "status", "size")
CLAIM_RE = re.compile(r"\bC\d+\b")


def parse_front_matter(text: str) -> dict[str, object] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    fields: dict[str, object] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return fields
        line = line.split("#", 1)[0].rstrip()
        if not line.strip() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            fields[key.strip()] = [item.strip() for item in value[1:-1].split(",") if item.strip()]
        else:
            fields[key.strip()] = value
    return None


def has_acceptance_criteria(text: str) -> bool:
    match = re.search(r"^##\s+Acceptance criteria\s*$(.*?)(?=^##\s|\Z)", text, re.MULTILINE | re.DOTALL | re.IGNORECASE)
    return bool(match and re.search(r"^\s*[-*]\s+\S", match.group(1), re.MULTILINE))


def load_stories(folder: Path) -> tuple[dict[str, dict], list[dict]]:
    stories_dir = folder / "stories" if (folder / "stories").is_dir() else folder
    stories: dict[str, dict] = {}
    findings: list[dict] = []
    for path in sorted(stories_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        fields = parse_front_matter(text)
        if fields is None:
            findings.append({"level": "error", "story": path.stem, "rule": "front-matter", "text": f"{path.name} has no closed front-matter block"})
            continue
        missing = [key for key in REQUIRED if key not in fields]
        if missing:
            findings.append({"level": "error", "story": path.stem, "rule": "required", "text": f"missing {', '.join(missing)}"})
        story_id = str(fields.get("id", path.stem))
        if story_id != path.stem:
            findings.append({"level": "error", "story": story_id, "rule": "id-file", "text": f"id {story_id} differs from file name {path.name}"})
        if story_id in stories:
            findings.append({"level": "error", "story": story_id, "rule": "duplicate", "text": "duplicate id"})
        kind = str(fields.get("type", ""))
        if kind not in TYPES:
            findings.append({"level": "error", "story": story_id, "rule": "type", "text": f"unknown type {kind!r}"})
        elif not story_id.startswith(kind + "-"):
            findings.append({"level": "error", "story": story_id, "rule": "id-type", "text": f"id should start with {kind}-"})
        if str(fields.get("status", "")) not in STATUSES:
            findings.append({"level": "error", "story": story_id, "rule": "status", "text": f"unknown status {fields.get('status')!r}"})
        if str(fields.get("size", "")) not in SIZES:
            findings.append({"level": "warning", "story": story_id, "rule": "size", "text": f"unknown size {fields.get('size')!r}"})
        depends = fields.get("depends_on", [])
        if isinstance(depends, str):
            depends = [] if depends in ("", "-") else [depends]
        fields["depends_on"] = depends
        if not has_acceptance_criteria(text):
            findings.append({"level": "error", "story": story_id, "rule": "acceptance", "text": "no '## Acceptance criteria' section with a bullet"})
        stories[story_id] = fields
    return stories, findings


def topological_order(stories: dict[str, dict]) -> tuple[list[str], list[str]]:
    """Kahn's algorithm in id order; returns (order, ids on a cycle or depending on one)."""
    remaining = {sid: {d for d in s["depends_on"] if d in stories} for sid, s in stories.items()}
    order: list[str] = []
    while True:
        free = sorted(sid for sid, deps in remaining.items() if not deps)
        if not free:
            break
        for sid in free:
            order.append(sid)
            del remaining[sid]
        for deps in remaining.values():
            deps.difference_update(free)
    return order, sorted(remaining)


def board(folder: Path, brief: Path | None) -> dict:
    stories, findings = load_stories(folder)
    for sid, story in stories.items():
        for dep in story["depends_on"]:
            if dep not in stories:
                findings.append({"level": "error", "story": sid, "rule": "dependency", "text": f"unknown dependency {dep}"})
    order, cyclic = topological_order(stories)
    if cyclic:
        findings.append({"level": "error", "story": ",".join(cyclic), "rule": "cycle", "text": "dependency cycle"})
    if brief is not None:
        claims = set(CLAIM_RE.findall(brief.read_text(encoding="utf-8")))
        for sid, story in stories.items():
            claim = str(story.get("claim", ""))
            if claim not in ("-", "") and claim not in claims:
                findings.append({"level": "error", "story": sid, "rule": "claim", "text": f"claim {claim} is not in the brief"})
    done = {sid for sid, s in stories.items() if s.get("status") in ("done", "dropped")}
    ready = [sid for sid in order if stories[sid].get("status") == "todo" and set(stories[sid]["depends_on"]) <= done]
    blocked = [sid for sid in order if stories[sid].get("status") == "todo" and sid not in ready]
    for sid, story in stories.items():
        if story.get("status") == "done" and not set(story["depends_on"]) <= done:
            findings.append({"level": "warning", "story": sid, "rule": "done-early", "text": "done while a dependency is not"})
    counts = {status: sum(1 for s in stories.values() if s.get("status") == status) for status in STATUSES}
    mermaid = ["graph TD"]
    for sid in order + cyclic:
        label = str(stories[sid].get("title", sid)).replace('"', "'")
        mermaid.append(f'  {sid.replace("-", "_")}["{sid}: {label} ({stories[sid].get("status")})"]')
        for dep in stories[sid]["depends_on"]:
            if dep in stories:
                mermaid.append(f"  {dep.replace('-', '_')} --> {sid.replace('-', '_')}")
    return {
        "ok": not any(f["level"] == "error" for f in findings),
        "stories": len(stories),
        "counts": counts,
        "ready": ready,
        "blocked": blocked,
        "order": order,
        "findings": findings,
        "mermaid": "\n".join(mermaid),
        "_stories": stories,
    }


def markdown(result: dict) -> str:
    stories = result["_stories"]
    lines = [f"Stories: {result['stories']} · " + " · ".join(f"{k} {v}" for k, v in result["counts"].items() if v)]
    lines.append("")
    lines.append("| Story | Type | Claim | Owner | Status | Size | Depends on |")
    lines.append("|---|---|---|---|---|---|---|")
    for sid in result["order"]:
        s = stories[sid]
        lines.append(f"| {sid}: {s.get('title')} | {s.get('type')} | {s.get('claim')} | {s.get('owner')} | {s.get('status')} | {s.get('size')} | {', '.join(s['depends_on']) or '-'} |")
    lines.append("")
    lines.append("Ready: " + (", ".join(result["ready"]) or "none"))
    lines.append("Blocked: " + (", ".join(result["blocked"]) or "none"))
    if result["findings"]:
        lines.append("")
        lines.extend(f"- {f['level']}: {f['story']}: {f['text']}" for f in result["findings"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Check a lab plan's story files and print the board.")
    parser.add_argument("plan", type=Path)
    parser.add_argument("--brief", type=Path)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    if not args.plan.is_dir():
        print(f"error: {args.plan} is not a folder", file=sys.stderr)
        return 2
    if args.brief is not None and not args.brief.is_file():
        print(f"error: {args.brief} is not a file", file=sys.stderr)
        return 2
    result = board(args.plan, args.brief)
    if args.format == "markdown":
        print(markdown(result))
    else:
        print(json.dumps({k: v for k, v in result.items() if not k.startswith("_")}, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
