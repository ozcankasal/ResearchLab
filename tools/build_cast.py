"""Render the cast in tools/cast.py into agent skills and the module roster.

Run from the repository root:  uv run tools/build_cast.py
Writes skills/<agent>/{SKILL.md,customize.toml,bmod.toml} for every agent and
skills/bmod-lab/roster.toml. Generated files carry a header saying so.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cast import AGENTS, GUESTS, ROOMS  # noqa: E402

SKILLS = ROOT / "skills"
# Where the published lab lives; setup uses it to offer installs and check for updates.
SOURCE = "github:ozcankasal/ResearchLab/skills"
BMAD_SOURCE = "github:bmad-code-org/BMAD-METHOD/skills"
LAB_SKILLS = {a["skill"] for a in AGENTS} | {"lab-agent-expert"} | {
    "lab-cast", "lab-spark", "lab-survey", "lab-frame", "lab-plan", "lab-prove", "lab-experiment", "lab-killtest",
    "lab-factcheck", "lab-referee", "lab-write", "lab-release", "lab-notebook", "lab-voice",
}


def q(text: str) -> str:
    """A TOML basic string."""
    return json.dumps(text, ensure_ascii=False)


SKILL_TEMPLATE = """---
name: {skill}
description: {description}
---
# {name} — {title}

{intro}

## Conventions

- `{{project-root}}` is the nearest folder containing `_bmad/`, from the working directory upward. `{{skill-root}}` is this skill's folder.
- Bare paths such as `references/<capability>.md` resolve from `{{skill-root}}`. The lab module's record, `bmod-lab`, sits beside this skill in the same skills folder; its `help/` files hold the lab method.
- Write only under `{{project-root}}`. `{{skill-root}}` may be a link into the shared lab source, which stays read-only: everything a project produces belongs to the project.

## On activation

1. Resolve the agent block: `uv run {{project-root}}/_bmad/scripts/resolve_customization.py --skill {{skill-root}} --project-root {{project-root}} --key agent`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again. Any other failure: use `{{skill-root}}/customize.toml` as shipped and say the overrides were not applied.
2. Run each entry of `{{agent.activation_steps_prepend}}` in order.
3. Adopt the persona: `{{agent.role}}`, `{{agent.identity}}`, `{{agent.communication_style}}`, `{{agent.principles}}`. Stay {short} until dismissed; the persona carries into every skill you invoke.
4. Load `{{agent.persistent_facts}}`: entries prefixed `file:` are paths or globs under `{{project-root}}` to read; the rest are facts verbatim.
5. Load config: `uv run {{project-root}}/_bmad/scripts/resolve_config.py --project-root {{project-root}} --key core.output_folder --key core.active_initiative --key modules.lab.papers_folder`. Lab documents live in `{{output_folder}}/{{active_initiative}}/` (without `/{{active_initiative}}` when it is unset), one folder per document named `<type>-<slug>`: `brief-`, `plan-`, `notebook-`, `survey-`, `ideas-`, `killtest-`, `factcheck-`, `referee-`, `experiment-`, `proof-`. Papers live under `{{papers_folder}}`.
6. Greet in one line, led by `{{agent.icon}}`, and keep that prefix on every message. The `bmad` skill answers questions about BMad itself.
7. Run each entry of `{{agent.activation_steps_append}}` in order.
8. Dispatch. When the request names what the user wants, run the matching `{{agent.menu}}` item without showing the menu. Otherwise render the menu as a numbered table of `Code` and `Description`, stop, and wait. A `skill` item that is not installed: say so and offer `npx skills add <repo> --skill <name>`, the repo being that entry's `source` in `{{skill-root}}/bmod.toml`. A request that fits nothing on the menu is a conversation.

## How {short} works

{rules}
- You assist; the researcher decides and is the only author. Follow the lab's responsible-use rules, `help/responsible-use.md` in `bmod-lab`: fabricate nothing, and log AI help that reaches a project output as an AI-USE entry with `lab-notebook`.
- Prose you write follows the lab's voice guide, `help/voice.md` in `bmod-lab`: plain, specific, in the author's own voice.
"""

CUSTOMIZE_HEADER = """# DO NOT EDIT -- generated from tools/cast.py and overwritten on every update.
#
# {name}, the {title}, is the hardcoded identity of this agent.
# Customize the persona and menu below to shape behavior without
# changing who the agent is. Override files:
#   {{project-root}}/_bmad/custom/{skill}.toml       (team)
#   {{project-root}}/_bmad/custom/{skill}.user.toml  (personal)

[agent]
# non-configurable skill frontmatter, create a custom agent if you need a new name/title
name = {qname}
title = {qtitle}

# --- Configurable below. Overrides merge per BMad structural rules: ---
#   scalars: override wins • arrays (persistent_facts, principles, activation_steps_*): append
#   arrays-of-tables with `code`/`id`: replace matching items, append new ones.

icon = {qicon}

# Steps to run before the standard activation (persona, config, greet).
activation_steps_prepend = []

# Steps to run after greet but before dispatch.
activation_steps_append = []

# Standing context for the whole session: literal sentences, or `file:` paths and globs
# under {{project-root}}, e.g. "file:{{project-root}}/docs/standards.md".
persistent_facts = []

role = {qrole}
identity = {qidentity}
communication_style = {qstyle}

# The agent's value system. Overrides append to defaults.
principles = [
{principles}
]

# Capabilities. Each item has exactly one of `skill` (an installed skill, by name) or
# `prompt`. Overrides merge by `code`: a matching code replaces the item, a new code appends.
"""


def render_agent(agent: dict) -> None:
    folder = SKILLS / agent["skill"]
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(
        SKILL_TEMPLATE.format(
            skill=agent["skill"], description=q(agent["description"]), name=agent["name"],
            title=agent["title"], intro=agent["intro"], short=agent["short"], rules=agent["rules"],
        ),
        encoding="utf-8",
    )
    lines = [CUSTOMIZE_HEADER.format(
        name=agent["name"], title=agent["title"], skill=agent["skill"], qname=q(agent["name"]),
        qtitle=q(agent["title"]), qicon=q(agent["icon"]), qrole=q(agent["role"]),
        qidentity=q(agent["identity"]), qstyle=q(agent["style"]),
        principles="\n".join(f"  {q(p)}," for p in agent["principles"]),
    )]
    for code, description, kind, value in agent["menu"]:
        lines.append(f"\n[[agent.menu]]\ncode = {q(code)}\ndescription = {q(description)}\n{kind} = {q(value)}\n")
    (folder / "customize.toml").write_text("".join(lines), encoding="utf-8")

    recommended = []
    for _code, _description, kind, value in agent["menu"]:
        if kind != "skill":
            continue
        if value in LAB_SKILLS:
            recommended.append(q(value))
        else:
            recommended.append(f"{{ skill = {q(value)}, source = {q(BMAD_SOURCE)} }}")
    for _code, _description, kind, value in agent["menu"]:
        if kind == "prompt" and "lab-factcheck" in value and q("lab-factcheck") not in recommended:
            recommended.append(q("lab-factcheck"))
        if kind == "prompt" and "bmad-party-mode" in value:
            recommended.append(f"{{ skill = \"bmad-party-mode\", source = {q(BMAD_SOURCE)} }}")
        if kind == "prompt" and "lab-notebook" in value and q("lab-notebook") not in recommended:
            recommended.append(q("lab-notebook"))
    bmod = f"[skill]\nbmod = \"bmod-lab\"\nsource = {q(SOURCE)}\n"
    if recommended:
        bmod += "recommended_skills = [\n" + "".join(f"  {r},\n" for r in dict.fromkeys(recommended)) + "]\n"
    (folder / "bmod.toml").write_text(bmod, encoding="utf-8")


def render_roster() -> None:
    out = [
        "# DO NOT EDIT -- generated from tools/cast.py.\n"
        "# The people the `lab` module offers and the rooms they form. A member with `skill` is an agent,\n"
        "# present only while that skill is installed; its name, title and icon follow the skill's\n"
        "# customization. A member without `skill` is a guest who exists only in rooms.\n"
    ]
    for agent in AGENTS:
        out.append(
            f"\n[[members]]\ncode = {q(agent['skill'])}\nskill = {q(agent['skill'])}\nname = {q(agent['name'])}\n"
            f"icon = {q(agent['icon'])}\ntitle = {q(agent['title'])}\npersona = {q(agent['roster_persona'])}\n"
        )
    for code, name, icon, title, persona in GUESTS:
        out.append(
            f"\n[[members]]\ncode = {q(code)}\nname = {q(name)}\nicon = {q(icon)}\ntitle = {q(title)}\n"
            f"persona = {q(persona)}\n"
        )
    known = {a["skill"] for a in AGENTS} | {g[0] for g in GUESTS}
    for room in ROOMS:
        missing = [m for m in room["members"] if m not in known]
        if missing:
            raise SystemExit(f"room {room['id']} names unknown members {missing}")
        members = ", ".join(q(m) for m in room["members"])
        out.append(
            f"\n[[groups]]\nid = {q(room['id'])}\nname = {q(room['name'])}\nscene = {q(room['scene'])}\n"
            f"members = [{members}]\nmemory = true\n"
        )
    (SKILLS / "bmod-lab" / "roster.toml").write_text("".join(out), encoding="utf-8")


WORKFLOW_CUSTOMIZE = """# DO NOT EDIT -- generated from tools/workflows.py and overwritten on every update.
#
# Customization surface for {skill}.
# Team overrides:     {{project-root}}/_bmad/custom/{skill}.toml
# Personal overrides: {{project-root}}/_bmad/custom/{skill}.user.toml
#
# Merge rules: scalars override, arrays append, tables merge key by key,
# arrays of tables merge by `code` or `id`.

[workflow]

# Instructions run before config is loaded.
activation_steps_prepend = []

# Instructions run after activation, before the work begins.
activation_steps_append = []

# Standing context for the whole run: literal sentences, or `file:` paths and
# globs under {{project-root}} whose contents are loaded as facts.
persistent_facts = []

# Run after the output has been delivered. A string or an array of strings;
# empty for none.
on_complete = ""
"""

WORKFLOW_OUTPUT = """
# Where runs land, and the folder and file name inside it. {{slug}} is set at run time.
{kind}_output_path = "{{output_folder}}/{{active_initiative}}"
run_folder_pattern = "{kind}-{{slug}}"
"""


def render_workflows() -> None:
    from workflows import EXTRA, WORKFLOWS

    for skill, (kind, lab_recommended, bmad_recommended) in WORKFLOWS.items():
        folder = SKILLS / skill
        folder.mkdir(parents=True, exist_ok=True)
        text = WORKFLOW_CUSTOMIZE.format(skill=skill)
        if kind:
            text += WORKFLOW_OUTPUT.format(kind=kind)
        text += EXTRA.get(skill, "")
        (folder / "customize.toml").write_text(text, encoding="utf-8")
        recommended = [q(name) for name in lab_recommended]
        recommended += [f"{{ skill = {q(name)}, source = {q(BMAD_SOURCE)} }}" for name in bmad_recommended]
        bmod = f"[skill]\nbmod = \"bmod-lab\"\nsource = {q(SOURCE)}\n"
        if recommended:
            bmod += "recommended_skills = [\n" + "".join(f"  {r},\n" for r in recommended) + "]\n"
        (folder / "bmod.toml").write_text(bmod, encoding="utf-8")


if __name__ == "__main__":
    for agent in AGENTS:
        render_agent(agent)
    render_roster()
    render_workflows()
    print(f"rendered {len(AGENTS)} agents, {len(GUESTS)} guests, {len(ROOMS)} rooms and the workflow manifests")
