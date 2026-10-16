#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""install_lab: set up the Research Lab in a project folder, leaving this repository untouched.

Usage:
  uv run <ResearchLab>/tools/install_lab.py <project-folder> [--author NAME] [--affiliation TEXT]
      [--orcid ID] [--papers-folder PATH] [--copy] [--no-build-standards] [--skip-bmad] [--dry-run]

Steps, all writing only inside <project-folder>:
  1. BMad: unless --skip-bmad or already present, install the bmad skill and the core-tools and method
     modules from bmad-code-org/BMAD-METHOD with `npx skills add ... -y`.
  2. The lab: link (or with --copy, copy) skills/bmod-lab and every skills/lab-* folder into the project's
     .agents/skills/, the shared skills folder, and into every other assistant's skills folder in the project
     that already holds BMad (BMad's installer makes one for each assistant it finds). Links keep every
     project on the current version of the lab.
  3. Setup: run BMad's setup.py so `_bmad/` exists and the `lab` module is registered, passing the
     author, affiliation, ORCID and papers folder as answers to the lab questions still open (a rerun
     keeps the earlier answers). Links this installer made to skills the lab has since renamed or
     removed are deleted; other copies of retired skills are reported, not touched.
  4. Standards: unless --no-build-standards, write `_bmad/custom/bmad-build.toml` so bmad-build loads
     the lab's research-software standards (an existing file is left alone and reported).

Refuses a project folder that is this repository or lies inside it.
Prints a JSON summary. Exit 0 on success, 1 when a step fails, 2 on a usage error.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parent.parent
SKILLS = LAB / "skills"
BMAD_REPO = "bmad-code-org/BMAD-METHOD"
CORE = ["bmad", "bmod-core-tools", "bmad-advanced-elicitation", "bmad-brainstorming", "bmad-customize",
        "bmad-deep-recon", "bmad-forge-idea", "bmad-party-mode", "bmad-review"]
METHOD = ["bmod-method", "bmad-agent-analyst", "bmad-agent-architect", "bmad-agent-dev", "bmad-agent-pm",
          "bmad-agent-ux-designer", "bmad-architecture", "bmad-build", "bmad-build-auto", "bmad-code-review",
          "bmad-correct-course", "bmad-prd", "bmad-prfaq", "bmad-product-brief", "bmad-project-context",
          "bmad-qa-generate-e2e-tests", "bmad-retrospective", "bmad-spec", "bmad-ticket", "bmad-ux",
          "bmad-walkthrough"]
BUILD_OVERRIDE = """# Team override written by the Research Lab installer: bmad-build loads the lab's
# research-software standards. Change it with the bmad-customize skill.
[workflow]
persistent_facts = ["file:{project-root}/.agents/skills/bmod-lab/help/research-software.md"]
"""


def lab_folders() -> list[Path]:
    return [SKILLS / "bmod-lab", *sorted(p for p in SKILLS.glob("lab-*") if p.is_dir())]


def run(cmd: list[str], cwd: Path, dry: bool, log: list[dict]) -> bool:
    entry = {"cmd": " ".join(cmd), "cwd": str(cwd)}
    if dry:
        entry["dry_run"] = True
        log.append(entry)
        return True
    done = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    entry["returncode"] = done.returncode
    if done.returncode != 0:
        entry["output"] = (done.stdout + done.stderr)[-1500:]
    log.append(entry)
    return done.returncode == 0


def skill_roots(project: Path) -> list[Path]:
    """The shared .agents/skills, then each assistant's own skills folder (.<name>/skills) that holds BMad."""
    shared = project / ".agents" / "skills"
    others = [f for f in sorted(project.glob(".*/skills")) if f != shared and (f / "bmad").exists()]
    return [shared, *others]


def bmad_skill(project: Path) -> Path | None:
    for root in skill_roots(project):
        candidate = root / "bmad"
        if (candidate / "scripts" / "setup.py").is_file():
            return candidate
    return None


def place(source: Path, target: Path, copy: bool, dry: bool) -> str:
    if target.is_symlink() or target.exists():
        if target.is_symlink() and target.resolve() == source.resolve():
            return "present"
        if not target.is_symlink():
            return "kept (a real folder is there; remove it to link the lab)"
        if not dry:
            target.unlink()
    if dry:
        return "would " + ("copy" if copy else "link")
    target.parent.mkdir(parents=True, exist_ok=True)
    if copy:
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "tests"))
        return "copied"
    try:
        target.symlink_to(source, target_is_directory=True)
    except OSError:
        # Windows allows links only with Developer Mode or admin rights; a copy works everywhere.
        shutil.copytree(source, target, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "tests"))
        return "copied (this system does not allow links; run the installer again after updating the lab)"
    return "linked"


def setup_json(base: list[str], extra: list[str], cwd: Path) -> object | None:
    done = subprocess.run([*base, *extra], cwd=cwd, capture_output=True, text=True)
    if done.returncode != 0:
        return None
    try:
        return json.loads(done.stdout)
    except json.JSONDecodeError:
        return None


def open_lab_questions(base: list[str], project: Path) -> set[str] | None:
    """Keys of the lab questions setup still asks, or None when setup cannot list them yet."""
    listing = setup_json(base, ["--list-config-questions"], project)
    if not isinstance(listing, list):
        return None
    return {q["key"] for q in listing if isinstance(q, dict) and q.get("module") in ("lab", "bmod-lab")}


def retired_lab_links(base: list[str], project: Path) -> tuple[list[str], list[str]]:
    """Retired lab skills whose every copy is a link into this repository, and the other retired ones."""
    status = setup_json(base, ["--status"], project)
    links, others = [], []
    for entry in (status or {}).get("retired_skills", []):
        if entry.get("module") != "lab":
            continue
        paths = [project / p for p in entry.get("paths", [])]
        ours = paths and all(p.is_symlink() and (LAB == Path(p.readlink()) or LAB in Path(p.readlink()).parents) for p in paths)
        (links if ours else others).append(entry["skill"])
    return links, others


def toml_string(text: str) -> str:
    return json.dumps(text, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Set up the Research Lab in a project folder.")
    parser.add_argument("project", type=Path)
    parser.add_argument("--author", default="")
    parser.add_argument("--affiliation", default="")
    parser.add_argument("--orcid", default="")
    parser.add_argument("--papers-folder", default="{project-root}/papers")
    parser.add_argument("--copy", action="store_true")
    parser.add_argument("--no-build-standards", action="store_true")
    parser.add_argument("--skip-bmad", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    project = args.project.expanduser().resolve()
    if project == LAB or LAB in project.parents:
        print(f"error: {project} is the lab's own repository or inside it; projects live elsewhere", file=sys.stderr)
        return 2
    summary: dict = {"lab": str(LAB), "project": str(project), "commands": [], "skills": {}, "ok": True}
    if not args.dry_run:
        project.mkdir(parents=True, exist_ok=True)

    # 1. BMad
    if not args.skip_bmad:
        if bmad_skill(project) is None:
            summary["ok"] &= run(["npx", "-y", "skills", "add", BMAD_REPO, "--skill", *CORE, "-y"], project, args.dry_run, summary["commands"])
        if not any((root / "bmod-method").exists() for root in skill_roots(project)):
            summary["ok"] &= run(["npx", "-y", "skills", "add", BMAD_REPO, "--skill", *METHOD, "-y"], project, args.dry_run, summary["commands"])

    # 2. The lab
    for folder in lab_folders():
        states = [place(folder, root / folder.name, args.copy, args.dry_run) for root in skill_roots(project)]
        summary["skills"][folder.name] = states[0] if len(set(states)) == 1 else states

    # 3. Setup with the lab's answers
    bmad = bmad_skill(project)
    if bmad is None and not args.dry_run:
        summary["ok"] = False
        summary["error"] = "no bmad skill in the project; install BMad first or drop --skip-bmad"
    else:
        setup = ["uv", "run", "--no-cache", str((bmad or Path("bmad")) / "scripts" / "setup.py"), "--project-root", str(project),
                 "--skill", str(bmad or "bmad"), *[arg for root in skill_roots(project) for arg in ("--root", str(root))]]
        values = {"author": args.author, "affiliation": args.affiliation, "orcid": args.orcid, "papers_folder": args.papers_folder}
        open_keys = None if args.dry_run else open_lab_questions(setup, project)
        if open_keys is not None:
            values = {k: v for k, v in values.items() if k in open_keys}
        answers = project / ".bmad-help-setup-modules.toml"
        if values:
            if not args.dry_run:
                answers.write_text("[modules.\"lab\"]\n" + "".join(f"\"{k}\" = {toml_string(v)}\n" for k, v in values.items()), encoding="utf-8")
            summary["ok"] &= run([*setup, "--module-answers", str(answers)], project, args.dry_run, summary["commands"])
            if not args.dry_run and answers.exists():
                answers.unlink()
        else:
            summary["ok"] &= run(setup, project, args.dry_run, summary["commands"])
            summary["answers"] = "kept the project's earlier answers; change them with the bmad skill"
        if not args.dry_run and summary["ok"]:
            links, others = retired_lab_links(setup, project)
            if links:
                summary["ok"] &= run([*setup, "--module", "lab", "--remove-retired", *links], project, False, summary["commands"])
                summary["retired_removed"] = links
            if others:
                summary["retired_kept"] = {"skills": others, "remove_with": " ".join([*setup, "--module", "lab", "--remove-retired", *others])}

    # 4. Research-software standards for bmad-build
    if not args.no_build_standards:
        override = project / "_bmad" / "custom" / "bmad-build.toml"
        if override.exists():
            summary["build_standards"] = f"kept the existing {override}; add the lab standards with bmad-customize if wanted"
        elif args.dry_run:
            summary["build_standards"] = f"would write {override}"
        else:
            override.parent.mkdir(parents=True, exist_ok=True)
            override.write_text(BUILD_OVERRIDE, encoding="utf-8")
            summary["build_standards"] = f"wrote {override}"

    summary["next"] = [
        "Open the project in your agent and say: talk to Nadia (the PI).",
        "Set an initiative per research project with the bmad skill, so each project's documents stay together.",
        "Nadia runs lab-cast first, so the project gets its own domain experts.",
    ]
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
