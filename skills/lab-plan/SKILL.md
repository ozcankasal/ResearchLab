---
name: lab-plan
description: "Breaks a research brief into epics and typed stories ordered riskiest first, and shows the story board. Use when the user says 'plan this project', 'break this into stories', 'make epics', 'what is ready', 'show the board' or 'replan after this result'."
---
# Research Plan

You turn the research brief into work that people and agents can pick up one piece at a time. The outcome is a plan and a folder of story files. Each story is a card its owner can execute without this conversation in the room. The owner might be a lab agent, `bmad-build` for a CODE story, or the user. So each card carries:

- its claim and its type;
- what to read first;
- acceptance criteria someone other than the author can check, such as a test name, a script output, an adversarial reading, or a decision in the notebook.

The plan's job is to settle the brief's claims at the lowest cost. Stories that can kill a claim come before stories that polish it.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.plan_output_path}/{workflow.run_folder_pattern}/plan-{slug}.md` with the story files in `stories/` beside it, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

- **Read the brief first.** Planning without a brief whose claims have kill criteria produces busywork. When the brief is missing or a claim has no kill criterion, say so and offer `lab-frame` first.
- **Draft the plan.** Use the story types the project's plan (`cast-*/plan.json` from `lab-cast`) lists, and `assets/plan-template.md`: one epic per claim, plus epics for software, writing and release when the exit needs them. Then write one story per file from `assets/story-template.md`. `references/story-types.md` gives what each type's acceptance criteria look like. Read it when writing the stories.
- **Order by risk.**
  - Put first the story that is cheapest and most likely to kill a claim.
  - Make unknowns into DECIDE spikes with a time box.
  - Keep independent tracks parallel.
  - Put a gate (G3) where a claim's last story closes.
- **Validate after every change.** Run `uv run {skill-root}/scripts/storyboard.py <plan folder> --brief <brief file> --format markdown` and fix every error it reports before handing over. Show the board, the ready list and the first story recommended. A story is assigned to the lab agent who owns its kind of work, and CODE stories go to `bmad-build`.
- **Replan from results, not from a blank page.**
  - Mark stories `dropped` with their reason rather than deleting them.
  - Add the new stories a narrowed or dead claim implies.
  - Log the replan in the notebook (`lab-notebook`).

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
