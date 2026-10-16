---
name: lab-notebook
description: "Keeps the project's lab notebook of decisions, results, dead ends, status and weekly digests. Use when the user says 'log this', 'note this decision', 'record this dead end', 'where does the project stand', 'weekly digest' or 'what did we decide about'."
---
# Lab Notebook

You keep the project's lab notebook: its memory across sessions and people. A future session, the user months from now, or a referee asking "why did you drop X?" reads it without this conversation in the room. So every entry is dated, typed, linked to the claim and story IDs it concerns, and says *why*, not only *what*. A dead end without its reason is lost work; a decision without the condition that would reopen it is a rumour.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. The notebook is `{workflow.notebook_output_path}/{workflow.run_folder_pattern}/notebook-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset; `{slug}` is the project's slug. One notebook per project: find it before creating one, and start a new one from `assets/notebook-template.md`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## What it does

- **Log.** Append an entry in the format of `assets/notebook-template.md`. Types: DECISION, RESULT, DEAD-END, GATE, IDEA, QUESTION, CORRECTION and AI-USE. An AI-USE entry records AI assistance that reached something leaving the project (text, code, figures, analyses, translations): what was done, by which skill, and what the author kept, rewrote or discarded. `lab-release` builds the disclosure statement from these entries. The notebook is append-only, as a paper lab notebook is. A past entry is never edited; a correction is a new CORRECTION entry that names the one it corrects. A GATE entry carries the verdict, owner, date and reopen condition. A DEAD-END carries what was tried and the reason it failed.
- **Status.** Read the brief's claim register, the plan's board and the recent entries. Run `uv run {skill-root}/../lab-plan/scripts/storyboard.py <plan folder>` when a plan exists. Report:
  - each claim's status;
  - what is in progress and what is blocked;
  - the last gate;
  - the single next step that tests the riskiest open claim.
- **Digest.** For the week, or a span the user names, report:
  - what changed;
  - what was decided and what died, with reasons;
  - which claims moved, and in which direction;
  - open questions and risks;
  - the plan for the next span.

  Append it as a DIGEST entry.
- **Search.** Answer "what did we decide about X" from the entries, quoting them with their dates. When the notebook does not say, report that instead of reconstructing an answer.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry in this notebook.

Run `{workflow.on_complete}` last.
