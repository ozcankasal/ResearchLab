#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""tells: count the habits of machine-written prose in a text, Markdown or LaTeX file, in any language.

Usage:
  tells.py <file> [--packs DIR] [--lang auto|none|CODE] [--format json|markdown] [--max-density N]
  tells.py --check-pack <pack.toml>

The script holds no vocabulary of its own. Built in are only the checks that work in every language:
em dashes, emoji, bold lead-ins on bullets, Title Case headings (for scripts with letter case), and the
spread of sentence lengths. Everything that depends on a language lives in a pack, one TOML file per
language in --packs, named <code>.toml. A pack holds that language's vocabulary and structures of
machine-written prose, the common words that identify the language, its sentence and word rules, and
examples that must and must not trigger it (format: the skill's assets/pack-template.toml).

--lang auto (the default) picks the pack whose common words cover the text best; --lang CODE forces
one; --lang none runs the neutral checks only. When no pack fits, the scan still runs the neutral checks
and reports "language": null with a "profile" of the text (dominant Unicode script, most frequent
words, letters outside ASCII), so that a pack can be written for it; the exit code is then 3.

--check-pack validates a pack: it parses, every pattern compiles, the detection list is not empty, there
are at least three positive and three negative examples, every positive example triggers a finding
and no negative example does.

LaTeX comments, math, citations and commands are stripped before counting; Markdown code is skipped.
Counts are evidence for an editor, not a verdict on authorship: people write these habits too.

Exit 0 after a scan with a pack, 3 when no pack fits, 1 when --max-density is exceeded or a pack check
fails, 2 on a usage error.
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import statistics
import sys
import tomllib
import unicodedata
from pathlib import Path

EMOJI = re.compile("[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]")
CASED_SCRIPTS = {"LATIN", "CYRILLIC", "GREEK", "ARMENIAN", "GEORGIAN", "COPTIC", "GLAGOLITIC"}
MATH_ENVS = r"equation|align|gather|multline|eqnarray|displaymath|tikzpicture|verbatim"
DEFAULT_END = "[.!?]"


# ---------- reading ----------

def clean_latex_line(text: str) -> str:
    text = re.sub(r"(?<!\\)%.*", "", text)
    text = re.sub(r"\$\$.*?\$\$|\\\[.*?\\\]|\$[^$]*\$|\\\(.*?\\\)", " ", text)
    text = re.sub(r"\\(?:cite\w*|ref|cref|Cref|eqref|label|url|href)\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", text)
    text = re.sub(r"\\(?:emph|textbf|textit|section|subsection|paragraph|caption)\*?\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", text)
    return re.sub(r"[{}~]", " ", text)


def prose_lines(path: Path) -> list[tuple[int, str]]:
    raw = path.read_text(encoding="utf-8")
    if path.suffix == ".tex":
        blanked = re.sub(rf"\\begin\{{({MATH_ENVS})\*?\}}.*?\\end\{{\1\*?\}}",
                         lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.DOTALL)
        return [(i, clean_latex_line(line)) for i, line in enumerate(blanked.splitlines(), start=1)]
    lines, in_code = [], False
    for i, line in enumerate(raw.splitlines(), start=1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        lines.append((i, "" if in_code else re.sub(r"`[^`]*`", " ", line)))
    return lines


# ---------- packs ----------

def load_pack(path: Path) -> dict:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    meta = data.get("pack", {})
    text_rules = data.get("text", {})
    pack = {
        "path": str(path),
        "code": meta.get("code") or path.stem,
        "language": meta.get("language", path.stem),
        "has_case": bool(meta.get("has_case", True)),
        "reviewed": bool(meta.get("reviewed", False)),
        "detect": [w.lower() for w in data.get("detect", {}).get("words", [])],
        "end": text_rules.get("sentence_end", DEFAULT_END),
        "unit": text_rules.get("unit", "word"),
        "categories": {},
        "examples": data.get("examples", {}),
    }
    for name, spec in data.get("categories", {}).items():
        flags = 0 if spec.get("case_sensitive", False) else re.IGNORECASE
        compiled = []
        for pattern in spec.get("patterns", []):
            if spec.get("sentence_initial", False):
                pattern = rf"(?:^|(?<={pack['end']}\s)|(?<={pack['end']})){pattern}"
            compiled.append(re.compile(pattern, flags))
        pack["categories"][name] = {"patterns": compiled, "advice": spec.get("advice", "")}
    return pack


def load_packs(folder: Path | None) -> list[dict]:
    if folder is None or not folder.is_dir():
        return []
    return [load_pack(p) for p in sorted(folder.glob("*.toml"))]


def tokens(text: str) -> list[str]:
    return [t.lower() for t in re.findall(r"\w+", text)]


def coverage(text: str, pack: dict) -> float:
    if not pack["detect"]:
        return 0.0
    if pack["unit"] == "char":
        letters = sum(1 for c in text if c.isalpha())
        return sum(text.count(w) for w in pack["detect"]) / max(1, letters)
    words = tokens(text)
    detect = set(pack["detect"])
    return sum(1 for t in words if t in detect) / max(1, len(words))


def choose_pack(text: str, packs: list[dict], lang: str) -> tuple[dict | None, dict[str, float]]:
    scores = {p["code"]: round(coverage(text, p), 3) for p in packs}
    if lang == "none":
        return None, scores
    if lang != "auto":
        return next((p for p in packs if p["code"] == lang), None), scores
    best = max(packs, key=lambda p: scores[p["code"]], default=None)
    if best is None:
        return None, scores
    # function words make up a quarter or more of running text in a language; a stray shared word does not
    threshold = 0.05 if best["unit"] == "char" else 0.15
    return (best if scores[best["code"]] >= threshold else None), scores


def profile(text: str) -> dict:
    scripts = collections.Counter(unicodedata.name(c, "UNKNOWN").split(" ")[0] for c in text if c.isalpha())
    words = collections.Counter(tokens(text))
    return {
        "scripts": dict(scripts.most_common(3)),
        "frequent_words": [w for w, _ in words.most_common(30)],
        "non_ascii_letters": sorted({c for c in text if c.isalpha() and ord(c) > 127})[:40],
    }


# ---------- scanning ----------

def scan_lines(lines: list[tuple[int, str]], pack: dict | None, markdown: bool) -> dict:
    text = "\n".join(line for _, line in lines)
    end = pack["end"] if pack else DEFAULT_END
    unit = pack["unit"] if pack else "word"
    script_counts = collections.Counter(unicodedata.name(c, "UNKNOWN").split(" ")[0] for c in text if c.isalpha())
    dominant = script_counts.most_common(1)[0][0] if script_counts else "LATIN"
    has_case = pack["has_case"] if pack else dominant in CASED_SCRIPTS
    findings: list[dict] = []
    for number, line in lines:
        if pack:
            for category, spec in pack["categories"].items():
                for regex in spec["patterns"]:
                    for m in regex.finditer(line):
                        findings.append({"line": number, "category": category, "text": m.group(0).strip(" ,"),
                                         "context": line.strip()[:160], "advice": spec["advice"]})
        if markdown:
            if re.match(r"\s*[-*]\s+\*\*[^*]+\*\*", line):
                findings.append({"line": number, "category": "bold-lead", "text": line.strip()[:60], "context": "", "advice": ""})
            heading = re.match(r"\s*#{1,6}\s+(.*)", line)
            if heading and has_case:
                words = re.findall(r"[^\W\d_][\w'-]*", heading.group(1))
                content = [w for w in words[1:] if len(w) > 3]
                if len(content) >= 2 and all(w[0].isupper() for w in content):
                    findings.append({"line": number, "category": "title-case", "text": heading.group(1)[:60], "context": "", "advice": ""})
        for m in EMOJI.finditer(line):
            findings.append({"line": number, "category": "emoji", "text": m.group(0), "context": line.strip()[:80], "advice": ""})
        for _ in re.finditer("—", re.sub(r"\|\s*—\s*(?=\|)", "|", line)):  # an em dash alone in a table cell is an empty cell
            findings.append({"line": number, "category": "em-dash", "text": "—", "context": line.strip()[:80], "advice": ""})
    prose = re.sub(r"^\s*([-*+]|\d+\.|#{1,6}|\|).*$", "", text, flags=re.MULTILINE)
    splitter = rf"(?<={end})\s*" if unit == "char" else rf"(?<={end})\s+"
    sentences = [s.strip() for s in re.split(splitter, re.sub(r"\s+", " ", prose)) if s.strip()]
    if unit == "char":
        lengths = [sum(1 for c in s if c.isalpha()) for s in sentences]
        size = sum(1 for c in text if c.isalpha())
    else:
        lengths = [len(tokens(s)) for s in sentences]
        size = len(tokens(text))
    lengths = [n for n in lengths if n >= (6 if unit == "char" else 3)]
    cadence = {
        "unit": unit,
        "mean": round(statistics.mean(lengths), 1) if lengths else 0,
        "stdev": round(statistics.pstdev(lengths), 1) if lengths else 0,
        "cv": round(statistics.pstdev(lengths) / statistics.mean(lengths), 2) if len(lengths) > 1 else None,
    }
    cadence["uniform"] = cadence["cv"] is not None and len(lengths) >= 8 and cadence["cv"] < 0.35
    per = 1000 / size if size else 0
    density: dict[str, float] = {}
    for f in findings:
        density[f["category"]] = density.get(f["category"], 0) + per
    density = {k: round(v, 2) for k, v in sorted(density.items())}
    density["total"] = round(sum(density.values()), 2)
    return {"size": size, "sentences": len(lengths), "cadence": cadence, "density_per_1000": density, "findings": findings}


def scan(path: Path, packs: list[dict], lang: str = "auto") -> dict:
    lines = prose_lines(path)
    text = "\n".join(line for _, line in lines)
    pack, scores = choose_pack(text, packs, lang)
    result = scan_lines(lines, pack, markdown=path.suffix != ".tex")
    result.update({
        "file": str(path),
        "language": pack["code"] if pack else None,
        "pack": {"path": pack["path"], "language": pack["language"], "reviewed": pack["reviewed"]} if pack else None,
        "pack_scores": scores,
    })
    if pack is None and lang != "none":
        result["profile"] = profile(text)
    return result


def check_pack(path: Path) -> dict:
    errors: list[str] = []
    try:
        pack = load_pack(path)
    except (tomllib.TOMLDecodeError, re.error, OSError) as error:
        return {"ok": False, "pack": str(path), "errors": [f"cannot load: {error}"]}
    if not pack["detect"]:
        errors.append("[detect].words is empty")
    if not pack["categories"]:
        errors.append("no [categories] defined")
    for name, spec in pack["categories"].items():
        if not spec["patterns"]:
            errors.append(f"category {name} has no patterns")
    positive = pack["examples"].get("positive", [])
    negative = pack["examples"].get("negative", [])
    if len(positive) < 3 or len(negative) < 3:
        errors.append("need at least three positive and three negative examples")
    for example in positive:
        found = [f for f in scan_lines([(1, example)], pack, markdown=False)["findings"] if f["category"] in pack["categories"]]
        if not found:
            errors.append(f"positive example triggers nothing: {example[:80]}")
    for example in negative:
        found = [f for f in scan_lines([(1, example)], pack, markdown=False)["findings"] if f["category"] in pack["categories"]]
        if found:
            errors.append(f"negative example triggers {found[0]['category']} ('{found[0]['text']}'): {example[:80]}")
    return {"ok": not errors, "pack": str(path), "code": pack["code"], "categories": sorted(pack["categories"]), "errors": errors}


# ---------- output ----------

def markdown(result: dict) -> str:
    c = result["cadence"]
    lang = result["language"] or "no pack"
    reviewed = "" if not result["pack"] else ("" if result["pack"]["reviewed"] else ", pack not yet reviewed")
    out = [f"{result['file']} ({lang}{reviewed}): {result['size']} {c['unit']}s, {result['sentences']} sentences, "
           f"sentence length {c['mean']} ± {c['stdev']} (cv {c['cv']}){'; uniform cadence' if c['uniform'] else ''}", "",
           "| Habit | Per 1000 |", "|---|---|"]
    out += [f"| {k} | {v} |" for k, v in result["density_per_1000"].items()]
    if result["findings"]:
        out += ["", "| Line | Habit | Found | Context |", "|---|---|---|---|"]
        out += [f"| {f['line']} | {f['category']} | {f['text']} | {f['context'].replace('|', '/')} |" for f in result["findings"]]
    if result.get("profile"):
        p = result["profile"]
        out += ["", f"No pack fits this text. Scripts: {p['scripts']}. Frequent words: {', '.join(p['frequent_words'][:20])}."]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Count the habits of machine-written prose, using language packs.")
    parser.add_argument("file", type=Path, nargs="?")
    parser.add_argument("--packs", type=Path)
    parser.add_argument("--lang", default="auto")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--max-density", type=float)
    parser.add_argument("--check-pack", type=Path)
    args = parser.parse_args(argv)
    if args.check_pack:
        if not args.check_pack.is_file():
            print(f"error: {args.check_pack} is not a file", file=sys.stderr)
            return 2
        report = check_pack(args.check_pack)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["ok"] else 1
    if args.file is None or not args.file.is_file():
        print(f"error: {args.file} is not a file", file=sys.stderr)
        return 2
    try:
        packs = load_packs(args.packs)
    except (tomllib.TOMLDecodeError, re.error) as error:
        print(f"error: a pack in {args.packs} does not load: {error}", file=sys.stderr)
        return 2
    if args.lang not in ("auto", "none") and not any(p["code"] == args.lang for p in packs):
        print(f"error: no pack {args.lang}.toml in {args.packs}", file=sys.stderr)
        return 2
    result = scan(args.file, packs, args.lang)
    print(markdown(result) if args.format == "markdown" else json.dumps(result, indent=2, ensure_ascii=False))
    if args.max_density is not None and result["density_per_1000"]["total"] > args.max_density:
        return 1
    return 3 if result["language"] is None and args.lang != "none" else 0


if __name__ == "__main__":
    sys.exit(main())
