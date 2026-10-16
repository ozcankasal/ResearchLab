#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""bundle: build a release deposit (paper PDF, LaTeX source, code zip) from a manifest, and check it.

Usage:
  bundle.py <release.toml> [--dry-run] [--verify "<command>"] [--format json|markdown]

The manifest (see the skill's assets/release-template.toml) names the project root, the output folder
(normally outside the repository), the PDF, the LaTeX source files and the code files, each as glob
patterns relative to its root, with exclude patterns. Paths may use ~.

Checks before writing: every include pattern matches at least one file; nothing matched is private
(references/pdf, references/txt), a secret (.env, keys, credentials) or editor clutter (.DS_Store,
__pycache__); no file exceeds 50 MB; LaTeX comments flagged TODO, FIXME or private (arXiv publishes
the source); a .bbl, if shipped, has the main .tex's name.
--dry-run reports what would be written. --verify unpacks the code zip into a fresh temporary folder
and runs the command there (for example "uv run pytest -q"), so the bundle is proven to run from a
clean copy.

Output: JSON {"ok", "out", "artifacts", "findings", "verify"} or a Markdown report. Findings with level
"error" stop the build. Exit 0 when ok, 1 otherwise, 2 on a usage error.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import tomllib
import zipfile
from pathlib import Path

PRIVATE = ("references/pdf/*", "*/references/pdf/*", "references/txt/*", "*/references/txt/*")
SECRETS = (".env", "*.env", "id_rsa*", "*.pem", "*.key", "*credentials*", "*secret*", ".netrc", "*.p12")
CLUTTER = (".DS_Store", "*/.DS_Store", "__pycache__/*", "*/__pycache__/*", "*.pyc", ".pytest_cache/*", "*/.pytest_cache/*")
MAX_BYTES = 50 * 1024 * 1024


def expand(value: str, version: str) -> str:
    return value.replace("{version}", version)


def matches(rel: str, patterns) -> bool:
    return any(fnmatch.fnmatch(rel, p) or fnmatch.fnmatch(Path(rel).name, p) for p in patterns)


def collect(root: Path, include: list[str], exclude: list[str], findings: list[dict], section: str) -> list[Path]:
    files: dict[str, Path] = {}
    for pattern in include:
        hits = [p for p in root.glob(pattern) if p.is_file()]
        if not hits:
            findings.append({"level": "error", "section": section, "text": f"pattern {pattern!r} matches no file"})
        for path in hits:
            rel = path.relative_to(root).as_posix()
            if matches(rel, exclude):
                continue
            files[rel] = path
    for rel, path in sorted(files.items()):
        if matches(rel, PRIVATE):
            findings.append({"level": "error", "section": section, "text": f"{rel} is private (third-party text)"})
        if matches(rel, SECRETS):
            findings.append({"level": "error", "section": section, "text": f"{rel} looks like a secret"})
        if matches(rel, CLUTTER):
            findings.append({"level": "error", "section": section, "text": f"{rel} is editor or cache clutter"})
        if path.stat().st_size > MAX_BYTES:
            findings.append({"level": "error", "section": section, "text": f"{rel} is larger than 50 MB"})
    return [files[k] for k in sorted(files)]


def latex_findings(files: list[Path], root: Path, main: str | None, findings: list[dict]) -> None:
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.suffix == ".tex":
            for number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
                m = re.search(r"(?<!\\)%(.*)", line)
                if m and re.search(r"TODO|FIXME|private|confidential", m.group(1), re.IGNORECASE):
                    findings.append({"level": "warning", "section": "source", "text": f"{rel}:{number} comment will be public: {m.group(1).strip()[:60]}"})
        if path.suffix == ".bbl" and main and path.stem != Path(main).stem:
            findings.append({"level": "error", "section": "source", "text": f"{rel} must be named {Path(main).stem}.bbl for arXiv"})


def build(manifest_path: Path, dry_run: bool, verify: str | None) -> dict:
    manifest = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
    release = manifest.get("release", {})
    version = str(release.get("version", "1.0"))
    base = manifest_path.parent
    root = (base / Path(release.get("root", ".")).expanduser()).resolve()
    out = Path(expand(release["out"], version)).expanduser()
    out = (out if out.is_absolute() else base / out).resolve()
    findings: list[dict] = []
    if out == root or root in out.parents:
        findings.append({"level": "warning", "section": "release", "text": f"output {out} is inside the project; deposits usually live outside it"})
    plan: list[dict] = []

    pdf = manifest.get("pdf")
    if pdf:
        source = root / pdf["source"]
        if not source.is_file():
            findings.append({"level": "error", "section": "pdf", "text": f"{pdf['source']} does not exist"})
        plan.append({"kind": "pdf", "name": expand(pdf["name"], version), "files": [source]})

    src = manifest.get("source")
    if src:
        src_root = root / src.get("root", ".")
        files = collect(src_root, src["files"], src.get("exclude", []), findings, "source")
        latex_findings(files, src_root, src.get("main"), findings)
        plan.append({"kind": "source", "name": expand(src.get("name", "latex-source.tar.gz"), version), "root": src_root, "files": files})

    code = manifest.get("code")
    if code:
        code_root = root / code.get("root", ".")
        files = collect(code_root, code["include"], code.get("exclude", []), findings, "code")
        prefix = expand(code.get("prefix", f"{release.get('name', 'code')}-v{version}"), version)
        plan.append({"kind": "code", "name": expand(code.get("name", f"{prefix}.zip"), version), "root": code_root, "files": files, "prefix": prefix})

    ok = not any(f["level"] == "error" for f in findings)
    artifacts = [{"kind": p["kind"], "name": p["name"], "files": len(p["files"])} for p in plan]
    result = {"ok": ok, "out": str(out), "artifacts": artifacts, "findings": findings, "verify": None}
    if not ok or dry_run:
        return result

    out.mkdir(parents=True, exist_ok=True)
    for p in plan:
        target = out / p["name"]
        if p["kind"] == "pdf":
            shutil.copy2(p["files"][0], target)
        elif p["kind"] == "source":
            with tarfile.open(target, "w:gz") as tar:
                for f in p["files"]:
                    tar.add(f, arcname=f.relative_to(p["root"]).as_posix())
        else:
            with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in p["files"]:
                    zf.write(f, f"{p['prefix']}/{f.relative_to(p['root']).as_posix()}")
        p["path"] = target

    if verify:
        code_plan = next((p for p in plan if p["kind"] == "code"), None)
        if code_plan is None:
            result["verify"] = {"ok": False, "output": "no code artifact to verify"}
        else:
            with tempfile.TemporaryDirectory() as tmp:
                with zipfile.ZipFile(code_plan["path"]) as zf:
                    zf.extractall(tmp)
                run = subprocess.run(verify, shell=True, cwd=Path(tmp) / code_plan["prefix"], capture_output=True, text=True, timeout=3600)
                result["verify"] = {"ok": run.returncode == 0, "command": verify, "output": (run.stdout + run.stderr)[-2000:]}
        result["ok"] = result["ok"] and bool(result["verify"] and result["verify"]["ok"])
    return result


def markdown(result: dict) -> str:
    lines = [f"Output: {result['out']} · {'ok' if result['ok'] else 'NOT OK'}", "", "| Artifact | Kind | Files |", "|---|---|---|"]
    lines += [f"| {a['name']} | {a['kind']} | {a['files']} |" for a in result["artifacts"]]
    if result["findings"]:
        lines += ["", *[f"- {f['level']} ({f['section']}): {f['text']}" for f in result["findings"]]]
    if result["verify"]:
        lines += ["", f"Verify `{result['verify'].get('command')}`: {'passed' if result['verify']['ok'] else 'FAILED'}", "```", result["verify"]["output"].strip(), "```"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build and check a release deposit from a manifest.")
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--verify")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)
    if not args.manifest.is_file():
        print(f"error: {args.manifest} is not a file", file=sys.stderr)
        return 2
    try:
        result = build(args.manifest, args.dry_run, args.verify)
    except (KeyError, tomllib.TOMLDecodeError) as error:
        print(f"error: bad manifest: {error}", file=sys.stderr)
        return 2
    print(markdown(result) if args.format == "markdown" else json.dumps(result, indent=2, ensure_ascii=False, default=str))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
