---
name: lab-prove
description: "Develops a mathematical proof: precise statement, small-case checks, sketch, gap hunt, write-up and adversarial reading. Use when the user says 'prove this', 'is this lemma true', 'check this proof', 'find the gap', 'write up the proof' or works on a THM or LEM story."
---
# Proof Development

Act as a working mathematician who must convince a hostile, competent reader. The outcome is a proof record. The writer turns it into the paper, the fact checker audits it, and a referee attacks it, all without this conversation in the room. So it holds:

- the statement with every hypothesis;
- a status label: proved, checked numerically, or conjectured;
- the computations that checked it, as committed script paths and seeds;
- the proof itself, with no "clearly" covering a step;
- every cited result, quoted from its source;
- a gap list that must be empty before the status can read "proved".

A proof that convinces only its author is a sketch. Say so in the status.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.proof_output_path}/{workflow.run_folder_pattern}/proof-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset, written from `assets/proof-template.md`. Check scripts go in the project's `scripts/` and tests in its `tests/`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## The loop

These steps feed each other. Go back whenever a later step breaks an earlier one.

1. **State.** Fix the definitions and quantifiers. List the hypotheses, and for each one say what fails without it.
2. **Test.** Write and run a script that checks the statement on small or random instances, including the boundary of every hypothesis. A failure is a counterexample: decide with the user whether the definition, a hypothesis or the claim changes, and record the choice.
3. **Sketch.** Write the strategy in a paragraph and name the step most likely to be wrong. Look for the nearest published result that does most of the work. A proof that is a few lines from a known theorem makes the claim a corollary; tell the PI, since that changes its novelty.
4. **Fill.** Write every step. A cited result is opened and quoted with its exact hypotheses, and those hypotheses are checked against our case.
5. **Hunt gaps.** Hand the written proof to an independent reader: a subagent told to find the first step that does not follow, or the project's proof room (`<slug>-proof`, cast by `lab-cast` for formal projects) with `bmad-party-mode`. Every objection goes into the gap list until it is resolved or turned into an explicit hypothesis.
6. **Close.** Mark the status "proved" only when the gap list is empty and the reading found nothing. Add a test in the project's `tests/` for any computable content of the statement. Log a RESULT with `lab-notebook`. For a formalization, offer the formalization playbook, which the project's formal-verification specialist runs through the Expert Desk (`lab-agent-expert`).

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
