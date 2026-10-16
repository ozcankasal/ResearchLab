#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# ///
"""cast_plan: turn a project's classification into its cast, story types, standards, databases and gates.

Usage:
  cast_plan.py <profile.toml> [--catalogue DIR] [--format json|toml]

The profile (the skill's assets/profile-template.toml) classifies the project by field (OECD Fields of
Science and Technology codes such as "1.1" or "5.2 Economics and business"), subfields, research modes,
outputs, sensitivities and keywords. The catalogue (default: ../catalogue beside this script) holds
rules.toml, methods.toml and packs/*.toml.

The plan names:
  - the lab's fixed core agents and general guests (always present);
  - guardians invited by sensitivities and outputs;
  - method specialists invited by research modes;
  - domain packs whose fields match and whose keywords appear in the profile;
  - generation slots: subfields (or fields) that no selected pack covers, for which the lab-cast skill
    writes new domain experts;
  - story types, reporting standards, search databases and extra gate conditions;
  - project rooms, with their catalogue members and the generated slots each one takes.
--format toml prints the party-mode customization block for the catalogue personas and the rooms.

Exit 0 on a valid profile, 1 when it has errors (unknown mode, output, sensitivity or field code),
2 on a usage error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import tomllib
from pathlib import Path

STORY_ORDER = ["THM", "LEM", "EXP", "STUDY", "DATA", "CODE", "LIT", "FORMAL", "WRITE", "DECIDE"]
CORE = ["lab-agent-pi", "lab-agent-methods", "lab-agent-engineer", "lab-agent-librarian",
        "lab-agent-factchecker", "lab-agent-referee", "lab-agent-editor", "lab-agent-voice"]
GENERAL_GUESTS = ["lab-guest-outsider", "lab-guest-historian", "lab-guest-statistician", "lab-guest-pragmatist"]
DOMAIN_SLOTS = ["core-a", "core-b", "skeptic", "translator"]
PLAYBOOK_DIR = ".agents/skills/lab-cast/playbooks"


def load_catalogue(folder: Path) -> tuple[dict, list[dict], list[dict]]:
    rules = tomllib.loads((folder / "rules.toml").read_text(encoding="utf-8"))
    methods = tomllib.loads((folder / "methods.toml").read_text(encoding="utf-8")).get("persona", [])
    packs = []
    for path in sorted((folder / "packs").glob("*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        packs.append({**data["pack"], "personas": data.get("persona", [])})
    return rules, methods, packs


def field_code(text: str) -> str:
    match = re.match(r"\s*(\d+(?:\.\d+)?)", text)
    return match.group(1) if match else text.strip()


def ordered_union(*lists) -> list:
    seen: dict = {}
    for items in lists:
        for item in items:
            seen.setdefault(item, None)
    return list(seen)


def plan(profile: dict, rules: dict, methods: list[dict], packs: list[dict]) -> dict:
    project = profile.get("project", {})
    cls = profile.get("classification", {})
    slug = project.get("slug") or "project"
    title = project.get("title") or slug
    fields = [field_code(f) for f in cls.get("fields", [])]
    modes = cls.get("modes", [])
    outputs = cls.get("outputs", [])
    sensitivities = cls.get("sensitivities", [])
    subfields = cls.get("subfields", [])
    text = " ".join([title, project.get("summary", ""), *subfields, *cls.get("keywords", [])]).lower()

    errors, warnings = [], []
    for f in fields:
        if f not in rules["fos"]:
            errors.append(f"unknown field code {f!r} (use the OECD Fields of Science codes, for example 1.1 or 5.2)")
    for kind, values, table in (("mode", modes, "modes"), ("output", outputs, "outputs"), ("sensitivity", sensitivities, "sensitivities")):
        for value in values:
            if value not in rules[table]:
                errors.append(f"unknown {kind} {value!r}; known: {', '.join(sorted(rules[table]))}")
    if not fields:
        errors.append("no field given")
    if not modes:
        errors.append("no research mode given")

    known_modes = [m for m in modes if m in rules["modes"]]
    known_outputs = [o for o in outputs if o in rules["outputs"]]
    known_sens = [s for s in sensitivities if s in rules["sensitivities"]]

    stories = ordered_union(["LIT", "DECIDE"], *(rules["modes"][m].get("stories", []) for m in known_modes),
                            *(rules["outputs"][o].get("stories", []) for o in known_outputs),
                            *(rules["sensitivities"][s].get("stories", []) for s in known_sens))
    stories = [s for s in STORY_ORDER if s in stories]
    guardians = ordered_union(*(rules["sensitivities"][s].get("guardians", []) for s in known_sens),
                              *(rules["outputs"][o].get("guardians", []) for o in known_outputs))
    gates = ordered_union(*(rules["sensitivities"][s].get("gates", []) for s in known_sens),
                          *(rules["outputs"][o].get("gates", []) for o in known_outputs))
    reporting = [{"mode": m, "standard": rules["modes"][m]["reporting"]} for m in known_modes]
    search = ordered_union(*(rules["areas"].get(f.split(".")[0], {}).get("search", []) for f in fields),
                           *(rules["fields"].get(f, {}).get("search", []) for f in fields))

    method_personas = [p for p in methods if set(p.get("modes", [])) & set(known_modes)]

    def keyword_hit(pack: dict, haystack: str) -> bool:
        return any(k.lower() in haystack for k in pack.get("keywords", []))

    selected = [p for p in packs if set(p.get("fields", [])) & set(fields) and (not p.get("keywords") or keyword_hit(p, text))]
    generate = []
    if subfields:
        for sub in subfields:
            if not any(p.get("keywords") and keyword_hit(p, sub.lower()) for p in selected):
                generate.append({"for": sub, "slots": list(DOMAIN_SLOTS)})
    else:
        for f in fields:
            if f in rules["fos"] and not any(f in p.get("fields", []) for p in selected):
                generate.append({"for": f"{f} {rules['fos'][f]}", "slots": list(DOMAIN_SLOTS)})
    if "design" in known_modes or {"software", "patent"} & set(known_outputs):
        generate.append({"for": "the people who would use the result", "slots": ["user"]})

    pack_personas = [dict(p, pack=pack["id"]) for pack in selected for p in pack["personas"]]
    groups = {
        "domain": [p["code"] for p in pack_personas if p.get("slot") in ("core", "translator")],
        "skeptics": [p["code"] for p in pack_personas if p.get("slot") == "skeptic"],
        "methods": [p["code"] for p in method_personas],
        "methods-formal": [p["code"] for p in method_personas if "formal" in p.get("modes", [])],
        "guardians": guardians,
    }
    generated_slots = {"domain": ["core-a", "core-b", "translator"], "skeptics": ["skeptic"]}
    rooms = []
    for room_id, spec in rules.get("rooms", {}).items():
        if spec.get("when_modes") and not set(spec["when_modes"]) & set(known_modes):
            continue
        members = ordered_union(spec.get("fixed", []), *(groups.get(g, []) for g in spec.get("take", [])))
        rooms.append({
            "id": f"{slug}-{room_id}",
            "name": spec["name"].replace("{title}", title),
            "scene": spec["scene"],
            "members": members,
            "add_generated": ordered_union(*(generated_slots.get(g, []) for g in spec.get("take", []))) if generate else [],
        })

    return {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "project": {"slug": slug, "title": title},
        "fields": [f"{f} {rules['fos'].get(f, '?')}" for f in fields],
        "core": CORE,
        "general_guests": GENERAL_GUESTS,
        "guardians": guardians,
        "methods": method_personas,
        "packs": [{"id": p["id"], "name": p["name"]} for p in selected],
        "pack_personas": pack_personas,
        "generate": generate,
        "stories": stories,
        "reporting": reporting,
        "search": search,
        "gates": gates,
        "rooms": rooms,
    }


def q(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def party_toml(result: dict) -> str:
    out = [f"# Project cast for {result['project']['title']}, written by lab-cast from scripts/cast_plan.py.\n"
           "# Catalogue personas and rooms; the skill adds the generated domain experts.\n"]
    for persona in [*result["methods"], *result["pack_personas"]]:
        playbooks = persona.get("playbooks", [])
        capabilities = "When spawned, read the project's profile and cast sheet first, and web-search the field's literature before speaking; cite only what you opened."
        if playbooks:
            capabilities += " Playbooks (read the one that fits before acting): " + ", ".join(f"{PLAYBOOK_DIR}/{p}.md" for p in playbooks) + "."
        out.append(
            f"\n[[workflow.party_members]]\ncode = {q(persona['code'])}\nname = {q(persona['name'])}\nicon = {q(persona['icon'])}\n"
            f"title = {q(persona['title'])}\npersona = {q(persona['persona'])}\ncapabilities = {q(capabilities)}\n"
        )
    for room in result["rooms"]:
        members = ", ".join(q(m) for m in room["members"])
        out.append(
            f"\n[[workflow.party_groups]]\nid = {q(room['id'])}\nname = {q(room['name'])}\nscene = {q(room['scene'])}\n"
            f"members = [{members}]\nmemory = true\n"
        )
    return "".join(out)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Turn a project classification into its cast plan.")
    parser.add_argument("profile", type=Path)
    parser.add_argument("--catalogue", type=Path, default=Path(__file__).resolve().parent.parent / "catalogue")
    parser.add_argument("--format", choices=("json", "toml"), default="json")
    args = parser.parse_args(argv)
    if not args.profile.is_file() or not (args.catalogue / "rules.toml").is_file():
        print(f"error: need a profile file and a catalogue with rules.toml ({args.profile}, {args.catalogue})", file=sys.stderr)
        return 2
    try:
        profile = tomllib.loads(args.profile.read_text(encoding="utf-8"))
        rules, methods, packs = load_catalogue(args.catalogue)
    except tomllib.TOMLDecodeError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    result = plan(profile, rules, methods, packs)
    if args.format == "toml":
        print(party_toml(result))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
