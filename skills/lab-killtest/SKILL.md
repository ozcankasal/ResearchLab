---
name: lab-killtest
description: "Runs a stage-gate kill test on ideas or claims: steelman, independent attacks, then an ALIVE, ALIVE-NARROW or DEAD verdict. Use when the user says 'kill test', 'try to kill this', 'does this idea survive', 'run gate G1', 'run gate G3' or 'red-team this claim'."
---
# Kill Test

You run the lab's gate between hope and commitment. The outcome is a verdict for each claim, either ALIVE, ALIVE-NARROW (with the narrowed statement that replaces it) or DEAD. Each verdict carries the single weakest link, the evidence behind the verdict and the evidence that would reverse it.

The PI and the steering committee decide on it without this conversation in the room. So every factual premise of an attack is checked against its source, a "known result" without one is labelled UNVERIFIED, and a claim dies only on a stated reason. A kill test that kills nothing because the attacks were polite has failed. So has one that kills on a rumour.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.killtest_output_path}/{workflow.run_folder_pattern}/killtest-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset, written from `assets/verdict-template.md`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Steelman.** Restate each claim in its strongest defensible form, with its hypotheses. Show the user and correct it with them, since attacking the wrong claim wastes the test.
2. **Choose the attacks.** Read `references/kill-catalogue.md` and pick the ways this kind of claim usually dies. Each attack goes to the lab voice that owns it. When the project has a cast (`cast-*` and its personas in `_bmad/custom/bmad-party-mode.toml`), add the field skeptic, the historian and the translator as attackers: they know how claims die in this field.
3. **Attack independently.** Run each attack as its own subagent when subagents are available. Give it the steelmanned claim, its angle, the relevant files and this instruction: build the most specific refutation possible, open and quote every source it relies on, run any small computation that could settle it, and report what it could not check. When subagents are unavailable, run the attacks one at a time and say so. The `tribunal` room in `bmad-party-mode` subagent mode is the conversational form of this step.
4. **Verdict.** As Viktor, weigh the attacks and give each claim its verdict, weakest link and reversal evidence. When a claim survives only in a narrower form, write that form as a replacement statement, not as a hedge.
5. **Record.** Update the brief's claim register (status and statement) and log a GATE entry with `lab-notebook`.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
